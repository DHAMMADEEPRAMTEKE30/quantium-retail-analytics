# Quantium Data Analytics Virtual Experience Program

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)
![Platform](https://img.shields.io/badge/Platform-Forage-orange.svg)

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Project Objective](#2-project-objective)
3. [Data Understanding](#3-data-understanding)
4. [Data Cleaning Process](#4-data-cleaning-process)
5. [Analysis & Methodology](#5-analysis--methodology)
6. [Key Findings & Insights](#6-key-findings--insights)
7. [Recommendations](#7-recommendations)
8. [Skills Demonstrated](#8-skills-demonstrated)
9. [Files in This Repository](#9-files-in-this-repository)
10. [How to Run](#10-how-to-run)

---

## 1. Problem Statement

A supermarket chain wants to better understand **who is buying chips** and **whether a new in-store chip layout actually works**.

The Category Manager (Julia) needs answers to two questions:

- Which customer segments are driving chip sales, and what are their preferences?
- Did the new chip aisle layout, tested in three trial stores, lead to a real increase in sales and customers?

Without this analysis, decisions about shelf placement, promotions, and store rollouts are made without evidence.

---

## 2. Project Objective

This project simulates the work of a retail analyst at Quantium, completing three tasks:

| Task | Goal |
|------|------|
| **Task 1** | Analyse customer purchasing behaviour across all segments |
| **Task 2** | Measure the impact of a new in-store layout tested in 3 trial stores |
| **Task 3** | Present findings and recommendations in a business-ready presentation |

---

## 3. Data Understanding

Two raw datasets were provided:

**Transaction Data** (`QVI_transaction_data.xlsx`)
- 264,836 rows of chip purchase transactions
- Covers July 2018 to June 2019
- Key columns: date, store number, loyalty card number, product name, quantity, total sales

**Customer Data** (`QVI_purchase_behaviour.csv`)
- 72,637 unique customers
- Key columns: loyalty card number, life stage, customer tier (Budget / Mainstream / Premium)

**Life Stage segments:** New Families, Young Families, Older Families, Young Singles/Couples, Midage Singles/Couples, Older Singles/Couples, Retirees

**Customer Tiers:** Budget, Mainstream, Premium

After merging both datasets, the final working dataset contained **246,740 transactions** with zero unmatched customers.

---

## 4. Data Cleaning Process

The raw data had several issues that were fixed before analysis:

| Issue Found | What Was Done |
|-------------|---------------|
| Dates stored as Excel integers | Converted to proper dates (origin: 30 Dec 1899) |
| 18,094 salsa product rows | Removed — salsa is out of scope for the chip category |
| Customer #226000 bought 200 packs twice | Removed — clearly a commercial buyer, not a regular customer |
| Pack size not available as a column | Extracted from product name (e.g. "Smiths Crinkle 175g" → 175) |
| Brand name not available as a column | Extracted from the first word of the product name |
| Inconsistent brand names (e.g. "DORITO" vs "DORITOS") | Standardised using a brand alias mapping |
| 25 December 2018 showed zero transactions | Confirmed as expected — stores are closed on Christmas Day |

After cleaning, the dataset covered **20 unique pack sizes** (70g to 380g) and **22 standardised brands**.

---

## 5. Analysis & Methodology

### Task 1 — Customer Analytics

Four metrics were calculated for every Life Stage × Customer Tier combination:

- **Total Sales ($)** — total revenue per segment
- **Number of Unique Customers** — how many distinct buyers in each segment
- **Average Units per Customer** — how many chip packs a typical customer buys
- **Average Price per Unit** — what the typical customer pays per pack

A **brand affinity score** and **pack size affinity score** were also calculated for the top segment (Mainstream Young Singles/Couples). The affinity ratio compares the segment's purchase share to the population average. A ratio above 1.0 means the segment over-indexes on that product.

A **two-sample independent t-test** was run to confirm whether Mainstream Young Singles/Couples paying more per unit was statistically significant or just random variation.

### Task 2 — Trial Store Evaluation

Three stores (77, 86, 88) tested a new chip aisle layout from February to April 2019.

To measure the true impact, each trial store needed a **control store** — a similar store that did not run the trial. Control stores were selected using a **composite scoring method**:

- **Pearson Correlation** — checks if the trial and control stores follow the same trends over time
- **Magnitude Distance** — checks if their actual sales and customer numbers are at similar levels

The store with the highest combined score (correlation + magnitude, equally weighted) was chosen as the control for each trial store.

| Trial Store | Control Store | Basis |
|-------------|--------------|-------|
| Store 77 | Store 233 | Highest composite score |
| Store 86 | Store 155 | Highest composite score |
| Store 88 | Store 237 | Highest composite score |

During the trial period, a **one-sided t-test** was used (df=7, 95% confidence level, critical t-value = 1.895) to check whether the trial store's performance was genuinely above what the control store would predict.

---

## 6. Key Findings & Insights

### Customer Analytics (Task 1)

**Top revenue segments:**

| Rank | Life Stage | Customer Tier | Total Sales |
|------|-----------|--------------|-------------|
| 1 | Older Families | Budget | $156,864 |
| 2 | Young Singles/Couples | Mainstream | $147,582 |
| 3 | Retirees | Mainstream | $145,169 |
| 4 | Young Families | Budget | $129,718 |
| 5 | Older Singles/Couples | Budget | $127,834 |

- **Budget Older Families** are the top revenue segment. They buy in high volumes — families tend to stock up on chips for household use and children's snacking.
- **Mainstream Young Singles/Couples** have the highest number of unique buyers across all segments, making them a critical group for engagement.
- **Older Families and Young Families** buy the most chip packs per customer (around 9 units), far higher than other segments.
- **Mainstream Young Singles/Couples pay significantly more per unit** than Budget or Premium counterparts in the same life stage — confirmed by t-test (t = 37.83, p < 0.0001). This suggests impulse-buying behaviour at a slight price premium.

**Brand Affinity — Mainstream Young Singles/Couples vs rest of population:**

| Brand | Affinity Ratio | Meaning |
|-------|---------------|---------|
| Tyrrells | 1.24 | 24% more likely to buy than the average customer |
| Twisties | 1.22 | 22% more likely |
| Doritos | 1.21 | 21% more likely |
| Tostitos | 1.21 | 21% more likely |
| Kettle | 1.19 | 19% more likely |

This segment gravitates toward premium and flavourful, party-style chip brands.

**Pack Size Affinity — Mainstream Young Singles/Couples vs rest of population:**

| Pack Size | Affinity Ratio | Meaning |
|-----------|---------------|---------|
| 270g | 1.27 | 27% more likely to buy |
| 380g | 1.26 | 26% more likely |
| 330g | 1.22 | 22% more likely |

Despite often living alone or as a couple, this segment strongly prefers larger sharing packs — pointing to social and party-occasion buying behaviour. Note: the 270g size is exclusively sold by Twisties, so this also reflects brand preference.

**Pack size distribution (overall):** The 175g pack is the most popular across all customers, followed by 150g and 110g, suggesting a general preference for mid-to-large packs.

**Seasonal pattern:** Chip sales spike in the two weeks before Christmas (December 15–24), then drop to zero on Christmas Day itself.

---

### Trial Store Evaluation (Task 2)

Pre-trial checks confirmed all three control stores closely tracked their matched trial stores in both sales and customer counts before the trial started — validating that the comparisons are fair.

**Trial results (February–April 2019):**

| Store | Control | Sales Uplift | Customer Uplift | Result |
|-------|---------|-------------|-----------------|--------|
| 77 | 233 | Significant in 2/3 months (Mar, Apr) | Significant in 2/3 months (Mar, Apr) | ✅ Successful |
| 86 | 155 | Significant in 2/3 months (Feb, Mar) | Significant in all 3 months | ⚠️ Investigate pricing |
| 88 | 237 | Significant in 2/3 months (Mar, Apr) | Significant in 2/3 months (Mar, Apr) | ✅ Successful |

- **Store 77:** Clear uplift in both sales and customers in March and April. The new layout drove more shoppers in and increased revenue.
- **Store 88:** The strongest and most consistent result. Both sales and customer growth aligned, giving a reliable signal that the new layout works.
- **Store 86:** Customer foot traffic grew significantly across all three trial months, but sales revenue only significantly increased in two months. The gap between strong customer growth and mixed sales growth suggests possible in-store discounting during the trial, which suppressed average price per unit. This needs investigation before a final rollout decision.

---

## 7. Recommendations

1. **Roll out the new chip aisle layout** to all stores with a profile similar to Stores 77 and 88. Both showed statistically significant uplift in sales and customer numbers.

2. **Investigate Store 86 pricing** before including it in the rollout. Strong foot traffic growth but inconsistent sales growth suggests promotional discounting may have suppressed revenue during the trial. Confirm whether any special deals ran in February–April 2019.

3. **Target Budget Older Families** with multi-buy promotions (e.g. buy 2 get 1 free) and larger value packs. They are the top revenue segment and respond well to volume deals.

4. **Target Mainstream Young Singles/Couples** with end-of-aisle placements and social media promotions featuring Tyrrells, Kettle, and Doritos. Ensure 270g–380g packs are well stocked and prominently placed for this group.

5. **Support Mainstream Retirees** with loyalty promotions and familiar, classic chip brands to maintain their strong spend levels.

6. **Stock 175g as the core shelf SKU** across all stores — it is the most purchased pack size overall. Add strong 270g–380g availability in stores with a high Mainstream Young Singles/Couples customer base.

7. **Plan Christmas promotions early.** Sales spike sharply in the first two weeks of December. Run targeted promotions from December 1–15 and ensure stock levels are ready well in advance.

---

## 8. Skills Demonstrated

| Skill | Where Applied |
|-------|--------------|
| Data cleaning & preparation | Fixing date formats, removing outliers, handling missing values |
| Feature engineering | Extracting PACK_SIZE and BRAND from raw product name strings |
| Exploratory data analysis | Segment-level sales, customer count, unit and price analysis |
| Statistical testing | Independent samples t-test for price differences between segments |
| Affinity scoring | Custom brand and pack size affinity ratio calculations |
| Experimental design | Pre-trial validation and control store selection methodology |
| Pearson correlation | Trend similarity scoring between trial and control stores |
| Magnitude distance scoring | Level similarity scoring between trial and control stores |
| Uplift testing | One-sided t-test with 95% confidence interval, 7 degrees of freedom |
| Data visualisation | Line charts, bar charts, confidence interval plots using matplotlib and seaborn |
| Business communication | PDF reports and a 17-slide PowerPoint deck using the Pyramid Principle framework |
| Python scripting | End-to-end scripts using pandas, numpy, scipy, matplotlib, reportlab, python-pptx |

---

## 9. Files in This Repository

```
quantium-retail-analytics/
│
├── README.md                          ← This file
├── requirements.txt                   ← Python dependencies
│
├── data/
│   └── QVI_data.xlsx                  ← Cleaned & merged dataset (output of Task 1)
│
├── code/
│   ├── task1_analysis.py              ← Customer analytics script
│   └── task2_analysis.py              ← Trial store analysis script
│
├── task1_customer_analytics/
│   ├── QVI_Task1_Analysis.pdf         ← Full Task 1 report
│   └── charts/
│       ├── fig1_transactions_over_time.png
│       ├── fig2_pack_size.png
│       ├── fig3_total_sales.png
│       ├── fig4_customer_count.png
│       ├── fig5_avg_units.png
│       ├── fig6_avg_price.png
│       ├── fig7_brand_affinity.png
│       └── fig8_pack_affinity.png
│
├── task2_trial_analysis/
│   ├── QVI_Task2_Analysis.pdf         ← Full Task 2 report
│   └── charts/
│       ├── pre_77_sales.png           ← Pre-trial check: Store 77 vs Control 233 (Sales)
│       ├── pre_77_custs.png           ← Pre-trial check: Store 77 vs Control 233 (Customers)
│       ├── pre_86_sales.png           ← Pre-trial check: Store 86 vs Control 155 (Sales)
│       ├── pre_86_custs.png           ← Pre-trial check: Store 86 vs Control 155 (Customers)
│       ├── pre_88_sales.png           ← Pre-trial check: Store 88 vs Control 237 (Sales)
│       ├── pre_88_custs.png           ← Pre-trial check: Store 88 vs Control 237 (Customers)
│       ├── fig_77_sales.png           ← Trial assessment: Store 77 Sales
│       ├── fig_77_custs.png           ← Trial assessment: Store 77 Customers
│       ├── fig_86_sales.png           ← Trial assessment: Store 86 Sales
│       ├── fig_86_custs.png           ← Trial assessment: Store 86 Customers
│       ├── fig_88_sales.png           ← Trial assessment: Store 88 Sales
│       └── fig_88_custs.png           ← Trial assessment: Store 88 Customers
│
└── task3_presentation/
    ├── QVI_Task3_Presentation.pptx    ← PowerPoint deck (17 slides)
    └── QVI_Task3_Presentation.pdf     ← PDF version of the presentation
```

---

## 10. How to Run

```bash
# Step 1: Install all dependencies
pip install -r requirements.txt

# Step 2: Run Task 1 — Customer Analytics
# Requires: QVI_transaction_data.xlsx and QVI_purchase_behaviour.csv in the same folder
python code/task1_analysis.py

# Step 3: Run Task 2 — Trial Store Analysis
# Requires: QVI_data.csv produced by Task 1
python code/task2_analysis.py
```

All charts save automatically to the relevant `charts/` subfolder. Reports and the PowerPoint are in their respective task folders.

---

## Certificate

**Program:** Quantium Data Analytics Virtual Experience
**Platform:** Forage
**Completed:** 2024

---

*This project was completed as part of a virtual experience program. The data is provided by Quantium / Forage for educational purposes only.*
