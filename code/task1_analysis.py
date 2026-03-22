# ============================================================
# Quantium Virtual Internship — Task 1: Customer Analytics
# Tool: Python | Author: Quantium Analytics Team
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── 1. Load Data ──────────────────────────────────────────────────────────────
transactions = pd.read_excel("QVI_transaction_data.xlsx")
customers    = pd.read_csv("QVI_purchase_behaviour.csv")

print("Transactions shape:", transactions.shape)
print("Customers shape:", customers.shape)

# ── 2. Clean Transactions ─────────────────────────────────────────────────────

# Fix date format (Excel integer origin)
transactions['DATE'] = pd.to_datetime(transactions['DATE'], origin='1899-12-30', unit='D')

# Remove salsa products (not chips)
transactions = transactions[~transactions['PROD_NAME'].str.contains('salsa', case=False, na=False)]
print(f"After removing salsa: {len(transactions)} rows")

# Remove outlier customer (card #226000 — bought 200 packs, likely commercial)
transactions = transactions[transactions['LYLTY_CARD_NBR'] != 226000]
print(f"After removing outlier: {len(transactions)} rows")

# Extract PACK_SIZE from product name
transactions['PACK_SIZE'] = transactions['PROD_NAME'].str.extract(r'(\d+)').astype(float)

# Extract BRAND from first word of product name
transactions['BRAND'] = transactions['PROD_NAME'].str.split().str[0].str.upper()

# Standardise brand aliases
brand_map = {
    'RED':'RRD', 'SNBTS':'SUNBITES', 'INFZNS':'INFUZIONS',
    'WW':'WOOLWORTHS', 'SMITH':'SMITHS', 'NCC':'NATURAL',
    'DORITO':'DORITOS', 'GRAIN':'GRNWVES'
}
transactions['BRAND'] = transactions['BRAND'].replace(brand_map)

print("\nBrands:", sorted(transactions['BRAND'].unique()))
print("Pack sizes:", sorted(transactions['PACK_SIZE'].unique()))

# ── 3. Clean Customer Data ────────────────────────────────────────────────────
print("\nCustomer nulls:", customers.isnull().sum().to_dict())
print("Lifestages:", customers['LIFESTAGE'].unique())
print("Premium tiers:", customers['PREMIUM_CUSTOMER'].unique())

# ── 4. Merge ──────────────────────────────────────────────────────────────────
data = transactions.merge(customers, on='LYLTY_CARD_NBR', how='left')
print(f"\nMerged shape: {data.shape}")
print(f"Nulls after merge: {data.isnull().sum().sum()}")
data.to_csv("QVI_data.csv", index=False)
print("Saved: QVI_data.csv")

# ── 5. Analysis ───────────────────────────────────────────────────────────────

# Total sales by segment
sales = data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['TOT_SALES'].sum().reset_index()
print("\nTop 5 segments by sales:")
print(sales.sort_values('TOT_SALES', ascending=False).head(5).to_string(index=False))

# Customer counts
cust_counts = data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR'].nunique().reset_index()

# Avg units per customer
avg_units = data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER']).apply(
    lambda x: x['PROD_QTY'].sum() / x['LYLTY_CARD_NBR'].nunique()
).reset_index(name='AvgUnits')

# Avg price per unit
data['PRICE_PER_UNIT'] = data['TOT_SALES'] / data['PROD_QTY']
avg_price = data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['PRICE_PER_UNIT'].mean().reset_index()

# T-test: Mainstream vs others for young & midage singles/couples
target_ls = ['YOUNG SINGLES/COUPLES','MIDAGE SINGLES/COUPLES']
mainstream = data[(data['LIFESTAGE'].isin(target_ls)) & (data['PREMIUM_CUSTOMER']=='Mainstream')]['PRICE_PER_UNIT']
others     = data[(data['LIFESTAGE'].isin(target_ls)) & (data['PREMIUM_CUSTOMER'].isin(['Budget','Premium']))]['PRICE_PER_UNIT']
t_stat, p_val = stats.ttest_ind(mainstream, others)
print(f"\nT-test (Mainstream vs others, young/midage singles/couples):")
print(f"  t={t_stat:.4f}, p={p_val:.6e} — {'SIGNIFICANT' if p_val < 0.05 else 'NOT SIGNIFICANT'}")

# ── 6. Brand & Pack Affinity (Mainstream Young Singles/Couples) ───────────────
target = data[(data['LIFESTAGE']=='YOUNG SINGLES/COUPLES') & (data['PREMIUM_CUSTOMER']=='Mainstream')]
rest   = data[~((data['LIFESTAGE']=='YOUNG SINGLES/COUPLES') & (data['PREMIUM_CUSTOMER']=='Mainstream'))]

seg_brand  = target.groupby('BRAND')['TXN_ID'].count() / len(target)
rest_brand = rest.groupby('BRAND')['TXN_ID'].count() / len(rest)
affinity   = (seg_brand / rest_brand).dropna().sort_values(ascending=False)

print("\nTop 5 brands (Mainstream Young Singles/Couples):")
print(affinity.head(5))

seg_pack  = target.groupby('PACK_SIZE')['TXN_ID'].count() / len(target)
rest_pack = rest.groupby('PACK_SIZE')['TXN_ID'].count() / len(rest)
pack_aff  = (seg_pack / rest_pack).dropna().sort_values(ascending=False)

print("\nTop 5 pack sizes (Mainstream Young Singles/Couples):")
print(pack_aff.head(5))

print("\n✓ Task 1 complete!")
