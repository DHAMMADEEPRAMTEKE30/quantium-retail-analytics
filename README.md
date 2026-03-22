# Quantium Data Analytics Virtual Experience Program

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

## Overview

End-to-end retail analytics project completed as part of the
**Quantium Data Analytics Virtual Experience Program** hosted on Forage.

The project simulates the work of a Quantium analyst advising a
supermarket **Category Manager (Julia)** on chip purchasing behaviour
and the performance of a new in-store trial layout.

---

## Project Structure

```
quantium-retail-analytics/
│
├── README.md
├── requirements.txt
├── data/
│   └── QVI_data.csv               # Cleaned & merged dataset
│
├── code/
│   ├── task1_analysis.py          # Customer analytics script
│   └── task2_analysis.py          # Trial store analysis script
│
├── task1_customer_analytics/
│   ├── QVI_Task1_Analysis.pdf     # Full Task 1 report
│   └── charts/                    # All Task 1 visualisations
│
├── task2_trial_analysis/
│   ├── QVI_Task2_Analysis.pdf     # Full Task 2 report
│   └── charts/                    # All Task 2 visualisations
│
└── task3_presentation/
    ├── QVI_Task3_Presentation.pptx  # PowerPoint deck
    └── QVI_Task3_Presentation.pdf   # PDF version
```

---

## Tasks Completed

### Task 1 — Customer Analytics
- Cleaned 264,836 transaction records (removed salsa products, outlier customers, fixed date formats)
- Extracted `PACK_SIZE` and `BRAND` features from product names
- Merged transaction data with customer segmentation data (72,637 customers)
- Analysed total sales, customer counts, average units and average price by `LIFESTAGE` × `PREMIUM_CUSTOMER` segment
- Ran independent t-test to confirm Mainstream Young Singles/Couples pay significantly more per unit (t=37.83, p<0.001)
- Calculated brand and pack size affinity scores for the top segment

**Key Finding:** Budget - Older Families ($156,864) and Mainstream - Young Singles/Couples ($147,582) are the top revenue segments. Mainstream Young Singles/Couples are 23% more likely to purchase Tyrrells chips.

---

### Task 2 — Experimentation & Uplift Testing
- Built Pearson Correlation and Magnitude Distance scoring functions to match trial stores to control stores
- Selected control stores: Store 233 (Trial 77), Store 155 (Trial 86), Store 237 (Trial 88)
- Applied pre-trial scaling factors and calculated percentage differences during the trial period (Feb–Apr 2019)
- Used one-sided t-test (df=7, 95% CI, critical t=1.895) to assess statistical significance

**Key Finding:** Trial stores 77 and 88 showed significant uplift in both sales and customers in 2/3 trial months. Store 86 showed strong customer growth (3/3 months) but mixed sales — recommend investigating potential in-store discounting.

---

### Task 3 — Strategic Presentation
- Built a 17-slide Quantium-branded PowerPoint deck using the Pyramid Principle framework
- Included executive summary, data visualisations, key callouts and actionable recommendations
- Delivered a strategic recommendation to roll out the new chip layout

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Python 3 | Core analysis language |
| pandas | Data loading, cleaning, merging, aggregation |
| matplotlib / seaborn | Charts and visualisations |
| scipy | Pearson correlation, t-tests |
| reportlab | PDF report generation |
| python-pptx | PowerPoint presentation generation |

---

## How to Run

```bash
# Install dependencies
pip install pandas matplotlib seaborn scipy openpyxl reportlab python-pptx

# Run Task 1 (requires QVI_transaction_data.xlsx and QVI_purchase_behaviour.csv)
python code/task1_analysis.py

# Run Task 2 (requires QVI_data.csv from Task 1 output)
python code/task2_analysis.py
```

---

## Key Results Summary

| Store | Control | Sales Uplift | Customer Uplift | Recommendation |
|-------|---------|-------------|-----------------|----------------|
| 77 | 233 | 2/3 months significant | 2/3 months significant | ✅ Roll Out |
| 86 | 155 | 2/3 months significant | 3/3 months significant | ⚠️ Investigate pricing |
| 88 | 237 | 2/3 months significant | 2/3 months significant | ✅ Roll Out |

---

## Certificate

**Program:** Quantium Data Analytics Virtual Experience  
**Platform:** Forage  
**Completed:** 2024  

---

## Disclaimer

This project was completed as part of a virtual experience program.
The data is provided by Quantium/Forage for educational purposes.
