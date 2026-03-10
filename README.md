# Jadarat Job Market — Exploratory Data Analysis

An interactive **Streamlit dashboard** that presents insights from the Jadarat cleaned job-postings dataset (Saudi Arabia, Oct 2022 – Jan 2023).

---

##  Live Dashboard
You can explore the interactive analysis here:  
 **[Jadarat Job Market Analysis Dashboard](https://unit3project-qccuprbtdt5pveqdja3h65.streamlit.app/)**

---

## Project Overview

This project performs **Exploratory Data Analysis (EDA)** on real job postings scraped from the **Jadarat** platform and cleaned by [shaykhaaldawsari on Kaggle](https://www.kaggle.com/datasets/shaykhaaldawsari/jadarat-cleaned-data-csv). The analysis notebook (`EDA_project.ipynb`) and the accompanying `app.py` dashboard cover:

- Data quality checks (duplicates, nulls, outliers)
- Salary distribution and patterns
- Job-title frequency & average-salary rankings
- Regional job distribution
- Gender, contract-type, benefits, and experience analysis
- Correlation analysis among numeric features

---

## Dataset Description

| Column | Description |
|:---|:---|
| `job_title` | Simplified job role (e.g. Analyst, Salesperson) |
| `job_date` | Posting date (Gregorian) |
| `comp_name` | Company name (Arabic) |
| `comp_type` | **1** = Private, **0** = Semi-Governmental |
| `comp_size` | Company size code (SA, SB, MA, MB, MC, L, XL, G) |
| `eco_activity` | Industry sector |
| `region` | Saudi region (e.g. Riyadh, Makkah) |
| `city` | City name |
| `contract` | **1** = Full-time, **0** = Remote |
| `benefits` | **1** = Benefits offered, **0** = None |
| `positions` | Number of vacancies in the posting |
| `exper` | Required years of experience |
| `gender` | **0** = Male, **1** = Female, **2** = Both |
| `Salary` | Monthly salary in SAR |

**Shape:** 1,470 rows × 14 columns (before cleaning)
