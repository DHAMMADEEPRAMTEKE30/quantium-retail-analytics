# ============================================================
# Quantium Virtual Internship — Task 2: Trial Store Analysis
# Tool: Python | Author: Quantium Analytics Team
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── 1. Load Data ──────────────────────────────────────────────────────────────
data = pd.read_csv("QVI_data.csv", parse_dates=['DATE'])
data['YEARMONTH'] = data['DATE'].dt.year * 100 + data['DATE'].dt.month

# ── 2. Build Monthly Measures ─────────────────────────────────────────────────
measures = data.groupby(['STORE_NBR','YEARMONTH']).agg(
    totSales=('TOT_SALES','sum'),
    nCustomers=('LYLTY_CARD_NBR','nunique'),
    nTxns=('TXN_ID','nunique'),
    nChips=('PROD_QTY','sum')
).reset_index()
measures['nTxnPerCust']     = measures['nTxns'] / measures['nCustomers']
measures['nChipsPerTxn']    = measures['nChips'] / measures['nTxns']
measures['avgPricePerUnit'] = measures['totSales'] / measures['nChips']

# Filter to stores with full 7-month pre-trial observation (Jul 2018 – Jan 2019)
pre = measures[measures['YEARMONTH'] < 201902]
full_stores = pre.groupby('STORE_NBR')['YEARMONTH'].count()
full_stores = full_stores[full_stores == 7].index
preTrialMeasures = pre[pre['STORE_NBR'].isin(full_stores)].copy()
print(f"Stores with full pre-trial data: {len(full_stores)}")

# ── 3. Correlation & Magnitude Functions ──────────────────────────────────────
def calcCorr(table, metricCol, trialStore):
    """Pearson correlation between trial store and each control candidate"""
    trial = table[table['STORE_NBR']==trialStore][['YEARMONTH',metricCol]].rename(columns={metricCol:'trial'})
    rows = []
    for s in table['STORE_NBR'].unique():
        ctrl = table[table['STORE_NBR']==s][['YEARMONTH',metricCol]].rename(columns={metricCol:'ctrl'})
        m = trial.merge(ctrl, on='YEARMONTH')
        c = stats.pearsonr(m['trial'], m['ctrl'])[0] if len(m) >= 2 else 0
        rows.append({'Store1':trialStore,'Store2':s,'corr_measure':c})
    return pd.DataFrame(rows)

def calcMag(table, metricCol, trialStore):
    """Normalised magnitude distance between trial store and each control candidate"""
    trial = table[table['STORE_NBR']==trialStore][['YEARMONTH',metricCol]].rename(columns={metricCol:'trial'})
    rows = []
    for s in table['STORE_NBR'].unique():
        ctrl = table[table['STORE_NBR']==s][['YEARMONTH',metricCol]].rename(columns={metricCol:'ctrl'})
        m = trial.merge(ctrl, on='YEARMONTH')
        for _, r in m.iterrows():
            rows.append({'Store1':trialStore,'Store2':s,'YEARMONTH':r['YEARMONTH'],
                         'measure':abs(r['trial']-r['ctrl'])})
    dist = pd.DataFrame(rows)
    mm = dist.groupby(['Store1','YEARMONTH'])['measure'].agg(minDist='min',maxDist='max').reset_index()
    dist = dist.merge(mm, on=['Store1','YEARMONTH'])
    denom = dist['maxDist'] - dist['minDist']
    dist['mag'] = np.where(denom==0, 1, 1-(dist['measure']-dist['minDist'])/denom)
    return dist.groupby(['Store1','Store2'])['mag'].mean().reset_index().rename(columns={'mag':'mag_measure'})

def findControl(trialStore):
    """Find best matching control store using composite score"""
    cs = calcCorr(preTrialMeasures,'totSales',trialStore)
    cc = calcCorr(preTrialMeasures,'nCustomers',trialStore)
    ms = calcMag(preTrialMeasures,'totSales',trialStore)
    mc = calcMag(preTrialMeasures,'nCustomers',trialStore)
    ss = cs.merge(ms,on=['Store1','Store2'])
    ss['scoreS'] = 0.5*ss['corr_measure']+0.5*ss['mag_measure']
    sc = cc.merge(mc,on=['Store1','Store2'])
    sc['scoreC'] = 0.5*sc['corr_measure']+0.5*sc['mag_measure']
    combined = ss[['Store1','Store2','scoreS']].merge(sc[['Store1','Store2','scoreC']],on=['Store1','Store2'])
    combined['final'] = 0.5*combined['scoreS']+0.5*combined['scoreC']
    best = combined[combined['Store2']!=trialStore].sort_values('final',ascending=False).iloc[0]
    return int(best['Store2'])

# ── 4. Find Control Stores ────────────────────────────────────────────────────
ctrl77 = findControl(77)
ctrl86 = findControl(86)
ctrl88 = findControl(88)
print(f"Trial 77  → Control {ctrl77}")
print(f"Trial 86  → Control {ctrl86}")
print(f"Trial 88  → Control {ctrl88}")

# ── 5. Trial Assessment ───────────────────────────────────────────────────────
def assessTrial(trialStore, controlStore, metric, label, fname):
    full = measures.copy()
    full['TransactionMonth'] = pd.to_datetime(full['YEARMONTH'].astype(str), format='%Y%m')
    TRIAL_START = 201902

    # Scaling factor
    pre_t = full[(full['STORE_NBR']==trialStore)  & (full['YEARMONTH']<TRIAL_START)][metric].sum()
    pre_c = full[(full['STORE_NBR']==controlStore) & (full['YEARMONTH']<TRIAL_START)][metric].sum()
    sf = pre_t / pre_c

    ctrl_scaled = full[full['STORE_NBR']==controlStore].copy()
    ctrl_scaled['scaled'] = ctrl_scaled[metric] * sf

    pct = ctrl_scaled[['YEARMONTH','scaled']].merge(
          full[full['STORE_NBR']==trialStore][['YEARMONTH',metric]], on='YEARMONTH')
    pct['pctDiff'] = abs(pct['scaled'] - pct[metric]) / pct['scaled']

    stdDev = pct[pct['YEARMONTH'] < TRIAL_START]['pctDiff'].std()
    t95    = stats.t.ppf(0.95, 7)

    # T-values for trial months
    trial_months = pct[pct['YEARMONTH'].between(201902, 201904)].copy()
    trial_months['tVal'] = trial_months['pctDiff'] / stdDev
    sig = (trial_months['tVal'] > t95).sum()

    print(f"\nStore {trialStore} vs {controlStore} | {label}")
    print(f"  t95={t95:.3f} | Significant months: {sig}/3")
    print(trial_months[['YEARMONTH','pctDiff','tVal']].to_string(index=False))

    # Plot
    trial_d = full[full['STORE_NBR']==trialStore][['TransactionMonth',metric]].copy()
    trial_d.columns = ['TransactionMonth','value']
    trial_d['Store_type'] = 'Trial'

    ctrl_d = ctrl_scaled[['TransactionMonth','scaled']].copy()
    ctrl_d.columns = ['TransactionMonth','value']
    ctrl_d['Store_type'] = 'Control'

    ctrl95 = ctrl_d.copy(); ctrl95['value'] *= (1+stdDev*2); ctrl95['Store_type'] = 'Control 95th %ile'
    ctrl5  = ctrl_d.copy(); ctrl5['value']  *= (1-stdDev*2); ctrl5['Store_type'] = 'Control 5th %ile'

    plot_df = pd.concat([trial_d, ctrl_d, ctrl95, ctrl5])
    colors = {'Trial':'#1f4e79','Control':'#ed7d31',
              'Control 95th %ile':'#a9c4e0','Control 5th %ile':'#a9c4e0'}

    fig, ax = plt.subplots(figsize=(12,5))
    ax.axvspan(pd.to_datetime('2019-02-01'), pd.to_datetime('2019-04-30'),
               alpha=0.12, color='grey', label='Trial period')
    for stype, grp in plot_df.groupby('Store_type'):
        ax.plot(grp['TransactionMonth'], grp['value'],
                color=colors.get(stype,'grey'),
                linestyle='--' if '%ile' in stype else '-',
                linewidth=1.2 if '%ile' in stype else 2, label=stype)
    ax.set_title(f'Store {trialStore} vs Control {controlStore} — {label}',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Month'); ax.set_ylabel(label)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close()
    return sig

# Run all assessments
assessTrial(77, ctrl77, 'totSales',   'Total Sales ($)',      'charts/fig_77_sales.png')
assessTrial(77, ctrl77, 'nCustomers', 'Number of Customers', 'charts/fig_77_custs.png')
assessTrial(86, ctrl86, 'totSales',   'Total Sales ($)',      'charts/fig_86_sales.png')
assessTrial(86, ctrl86, 'nCustomers', 'Number of Customers', 'charts/fig_86_custs.png')
assessTrial(88, ctrl88, 'totSales',   'Total Sales ($)',      'charts/fig_88_sales.png')
assessTrial(88, ctrl88, 'nCustomers', 'Number of Customers', 'charts/fig_88_custs.png')

print("\n✓ Task 2 complete!")
