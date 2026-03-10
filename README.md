# Jadarat Job Market — Exploratory Data Analysis

An interactive **Streamlit dashboard** that presents insights from the Jadarat cleaned job-postings dataset (Saudi Arabia, Oct 2022 – Jan 2023).

> **Live Demo:** Deploy on Streamlit Cloud — see [deployment instructions](#streamlit-cloud-deployment) below.

---

## 📖 Project Overview

This project performs **Exploratory Data Analysis (EDA)** on real job postings scraped from the **Jadarat** platform and cleaned by [shaykhaaldawsari on Kaggle](https://www.kaggle.com/datasets/shaykhaaldawsari/jadarat-cleaned-data-csv). The analysis notebook (`EDA_project.ipynb`) and the accompanying `app.py` dashboard cover:

- Data quality checks (duplicates, nulls, outliers)
- Salary distribution and patterns
- Job-title frequency & average-salary rankings
- Regional job distribution
- Gender, contract-type, benefits, and experience analysis
- Correlation analysis among numeric features

---

## 📊 Dataset Description

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

---

## 💡 Key Insights

| Insight | Detail |
|:---|:---|
| Average Salary | ~5,295 SAR; median ~4,500 SAR |
| Salary Range | 3,000 – 35,000 SAR (Pilot outlier removed) |
| Experience | 50 % of jobs require **0 years** — great for fresh graduates |
| Top Region | **Riyadh** with ~45 % of all postings |
| Peak Month | **November 2022** |
| Company Size | Most postings come from **small businesses** |
| Benefits | ~73 % of jobs offer **no additional benefits** |
| Data Quality | 83 duplicates removed, 0 nulls, 2 misclassified CEO rows fixed |

---

## 🚀 Running Locally

### Prerequisites

- Python 3.9+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/alkhurayjah/Unit3_Project.git
cd Unit3_Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

The app will open at **http://localhost:8501**.

> **Note:** The app automatically downloads the dataset using `kagglehub`. If you do not have Kaggle credentials configured, you can manually place the `processed_dataset.csv` file in the repository root directory.

### Kaggle Credentials (optional, for local kagglehub)

```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"
```

---

## ☁️ Streamlit Cloud Deployment

1. **Push** `app.py`, `requirements.txt`, and `README.md` to your GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select your repo, branch, and set the main file to `app.py`.
4. **Add secrets** (sidebar → ⚙️ Settings → Secrets):
   ```toml
   KAGGLE_USERNAME = "your_kaggle_username"
   KAGGLE_KEY = "your_kaggle_api_key"
   ```
   Alternatively, download `processed_dataset.csv` from Kaggle, commit it to the repo root, and the app will use the local file automatically (no secrets required).
5. Click **Deploy** — the dashboard will be live in a few minutes.

---

## 📁 Repository Structure

```
Unit3_Project/
├── EDA_project.ipynb   # Original Jupyter EDA notebook
├── app.py              # Streamlit dashboard application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🛠️ Tech Stack

- **Streamlit** — Dashboard framework
- **Plotly** — Interactive visualizations
- **Pandas / NumPy** — Data manipulation
- **kagglehub** — Automated dataset download

---

*Built as part of Unit 3 Project — Data Science & Analysis.*