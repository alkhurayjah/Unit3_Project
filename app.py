"""
Jadarat Job Market -- Exploratory Data Analysis Dashboard
=========================================================
Interactive Streamlit dashboard presenting insights from the
Jadarat (Saudi Arabia) cleaned job-postings dataset.

Dataset source: Kaggle -- shaykhaaldawsari/jadarat-cleaned-data-csv
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -- Page configuration ------------------------------------------------
st.set_page_config(
    page_title="Jadarat Job Market EDA",
    layout="wide",
)

# -- Custom CSS --------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #4019D1 0%, #7A5AF8 100%);
        border-radius: 12px;
        padding: 16px 20px;
        color: white;
    }
    div[data-testid="stMetric"] label { color: #e0d4ff !important; font-size: 0.85rem; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 700; }

    /* Section dividers */
    hr { border: none; border-top: 2px solid #e6e1f7; margin: 2rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -- Colour palette (matches notebook) ---------------------------------
BRAND = "#4019D1"
BRAND_DARK = "#21136B"
BRAND_LIGHT = "#7A5AF8"
PALETTE = [BRAND_DARK, BRAND_LIGHT, BRAND]


# -- Data loading & cleaning (mirrors notebook) ------------------------
@st.cache_data(show_spinner="Loading Jadarat dataset ...")
def load_data() -> pd.DataFrame:
    """Load the Jadarat dataset via kagglehub or a local fallback."""
    df: pd.DataFrame | None = None

    # 1) Try kagglehub
    try:
        import kagglehub
        path = kagglehub.dataset_download(
            "shaykhaaldawsari/jadarat-cleaned-data-csv"
        )
        df = pd.read_csv(f"{path}/processed_dataset.csv")
    except Exception:
        pass

    # 2) Fallback to local CSV
    if df is None:
        import os
        local = os.path.join(os.path.dirname(__file__), "processed_dataset.csv")
        if os.path.exists(local):
            df = pd.read_csv(local)
        else:
            st.error(
                "Could not load the dataset. "
                "Place `processed_dataset.csv` in the repo root or "
                "configure Kaggle API credentials."
            )
            st.stop()

    # -- Cleaning (same steps as the notebook) -------------------------
    df.drop_duplicates(inplace=True)
    df["job_date"] = pd.to_datetime(df["job_date"])
    df["year"] = df["job_date"].dt.year
    df["month"] = df["job_date"].dt.month

    # Remove Pilot outlier
    df = df[df["job_title"] != "Pilot"]

    # Reclassify two mis-labelled CEO rows to Manager
    mask = (df["job_title"] == "CEO") & (df["Salary"] == 6000.0)
    df.loc[mask, "job_title"] = "Manager"

    # Drop columns not used in analysis
    df.drop(
        columns=["city", "job_date", "eco_activity", "positions",
                 "comp_type", "comp_name"],
        inplace=True,
        errors="ignore",
    )
    return df


df = load_data()

# -- Helper maps -------------------------------------------------------
GENDER_MAP = {0: "Male", 1: "Female", 2: "Both"}
CONTRACT_MAP = {0: "Remote", 1: "Full-time"}
BENEFITS_MAP = {0: "No Benefits", 1: "Benefits Offered"}
COMP_SIZE_LABELS = {
    "SA": "Small A", "SB": "Small B",
    "MA": "Medium A", "MB": "Medium B", "MC": "Medium C",
    "L": "Large", "XL": "Extra Large", "G": "Giant",
}

# ======================================================================
# 1 - HEADER
# ======================================================================

st.markdown(
    "<h1 style='text-align:center; color:#21136B;'>"
    "Jadarat Job Market EDA Dashboard </h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; font-size:1.1rem; color:#555;'>"
    "Interactive exploration of <b>1,400+</b> cleaned Saudi job postings "
    "from the <b>Jadarat</b> platform (Oct 2022 - Jan 2023) </p>",
    unsafe_allow_html=True,
)
st.markdown("---")

filtered = df

# ======================================================================
# 2 - DATASET OVERVIEW
# ======================================================================

st.markdown("## Dataset Overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Records", f"{len(filtered):,}")
m2.metric("Job Titles", filtered["job_title"].nunique())
m3.metric("Regions", filtered["region"].nunique())
m4.metric("Avg Salary (SAR)", f"{filtered['Salary'].mean():,.0f}")

with st.expander("Preview Data", expanded=False):
    st.dataframe(filtered.head(50), use_container_width=True)

with st.expander("Summary Statistics", expanded=False):
    st.dataframe(
        filtered.describe().T.style.format("{:.2f}"),
        use_container_width=True,
    )

st.markdown("---")

# ======================================================================
# 3 - KEY INSIGHTS
# ======================================================================

st.markdown("## Key Insights from the EDA")

i1, i2 = st.columns(2)

with i1:
    st.markdown(
        """
        **Salary**
        - Average salary is approximately **5,295 SAR**, median is approximately **4,500 SAR**
        - Range: **3,000 -- 35,000 SAR** (after removing the Pilot outlier)
        - 50% of jobs offer 4,500 SAR or less, indicating mostly entry-to-mid-level roles

        **Experience**
        - Average required experience is approximately **1.3 years**
        - 50% of jobs require **0 years**, ideal for fresh graduates

        **Vacancies**
        - Average of approximately 3 positions per posting; some postings advertise up to 50
        """
    )

with i2:
    st.markdown(
        """
        **Data Quality**
        - 83 duplicate rows removed
        - No missing values in any column
        - "Pilot" roles removed as salary outliers (35,000 SAR)
        - 2 misclassified CEO rows reclassified as Manager

        **Market Insights**
        - **Riyadh** region dominates with approximately 45% of all postings
        - Most jobs are posted by **small businesses**
        - Approximately 73% of jobs offer **no additional benefits**
        - The dataset covers Oct 2022 -- Jan 2023; peak month is **November**
        """
    )

st.markdown("---")

# ======================================================================
# 4 - VISUALIZATIONS
# ======================================================================

st.markdown("## Visualizations")

# -- Row 1: Top Job Titles & Top Salaries ------------------------------

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Top Job Titles by Count")
    top_titles = (
        filtered["job_title"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_titles.columns = ["Job Title", "Count"]
    fig = px.bar(
        top_titles,
        x="Job Title",
        y="Count",
        color="Count",
        color_continuous_scale=["#e0d4ff", BRAND],
        text_auto=True,
    )
    fig.update_layout(
        xaxis_tickangle=-40,
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=20, b=60),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### Top Average Salaries by Job Title")
    top_sal = (
        filtered.groupby("job_title")["Salary"]
        .mean()
        .nlargest(10)
        .reset_index()
    )
    top_sal.columns = ["Job Title", "Avg Salary"]
    fig = px.bar(
        top_sal,
        x="Job Title",
        y="Avg Salary",
        color="Avg Salary",
        color_continuous_scale=["#e0d4ff", BRAND],
        text_auto=",.0f",
    )
    fig.update_layout(
        xaxis_tickangle=-40,
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=20, b=60),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

# -- Row 2: Region Pie & Gender / Contract ----------------------------

c3, c4 = st.columns(2)

with c3:
    st.markdown("### Jobs by Region")
    region_counts = (
        filtered["region"]
        .value_counts()
        .reset_index()
    )
    region_counts.columns = ["Region", "Count"]
    fig = px.pie(
        region_counts,
        names="Region",
        values="Count",
        color_discrete_sequence=px.colors.sequential.Purples_r,
        hole=0.35,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("### Jobs by Gender and Contract Type")
    gc = filtered.copy()
    gc["Gender"] = gc["gender"].map(GENDER_MAP)
    gc["Contract"] = gc["contract"].map(CONTRACT_MAP)
    gc_grouped = (
        gc.groupby(["Contract", "Gender"])
        .size()
        .reset_index(name="Count")
    )
    fig = px.bar(
        gc_grouped,
        x="Contract",
        y="Count",
        color="Gender",
        barmode="group",
        color_discrete_sequence=[BRAND_DARK, BRAND_LIGHT, BRAND],
        text_auto=True,
    )
    fig.update_layout(margin=dict(t=20, b=20), height=420)
    st.plotly_chart(fig, use_container_width=True)


# -- Row 4: Jobs by Month & Company Size ------------------------------

c7, c8 = st.columns(2)

with c7:
    st.markdown("### Job Postings by Month")
    month_counts = (
        filtered["month"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    month_counts.columns = ["Month", "Count"]
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    }
    month_counts["Month Name"] = month_counts["Month"].map(month_names)
    fig = px.bar(
        month_counts,
        x="Month Name",
        y="Count",
        color="Count",
        color_continuous_scale=["#e0d4ff", BRAND],
        text_auto=True,
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=20, b=20),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

with c8:
    st.markdown("### Jobs by Company Size")
    cs = (
        filtered["comp_size"]
        .value_counts()
        .reset_index()
    )
    cs.columns = ["Size Code", "Count"]
    cs["Size"] = cs["Size Code"].map(
        lambda x: COMP_SIZE_LABELS.get(x, x)
    )
    fig = px.bar(
        cs,
        x="Size",
        y="Count",
        color="Count",
        color_continuous_scale=["#e0d4ff", BRAND],
        text_auto=True,
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=20, b=20),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

# -- Row 4: Jobs by Benefits -------------------------------------------

st.markdown("### Jobs by Benefits")
ben = filtered.copy()
ben["Benefits"] = ben["benefits"].map(BENEFITS_MAP)
ben_counts = (
    ben["Benefits"]
    .value_counts()
    .reset_index()
)
ben_counts.columns = ["Benefits", "Count"]
fig = px.pie(
    ben_counts,
    names="Benefits",
    values="Count",
    color_discrete_sequence=[BRAND, "#e0d4ff"],
    hole=0.4,
)
fig.update_traces(textposition="inside", textinfo="percent+label")
fig.update_layout(margin=dict(t=20, b=20), height=420)
st.plotly_chart(fig, use_container_width=True)

# -- Row 5: Correlation Heat Map ----------------------------------------

st.markdown("### Correlation Heat Map")

df_hm = filtered.copy()

# Encode categorical features (same approach as the notebook)
df_hm["job_title"] = df_hm.groupby("job_title")["Salary"].transform("mean")
df_hm["region"] = df_hm.groupby("region")["Salary"].transform("mean")

size_map = {"SA": 1, "SB": 2, "MA": 3, "MB": 4, "MC": 5, "L": 6, "G": 7, "U": 8}
df_hm["comp_size"] = df_hm["comp_size"].map(size_map)

features = [
    "job_title", "region", "comp_size",
    "exper", "gender", "benefits", "contract", "Salary",
]
corr = df_hm[features].corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale=["#f5f0ff", "#e0d4ff", BRAND_LIGHT, BRAND, BRAND_DARK],
    aspect="auto",
    labels=dict(color="Correlation"),
)
fig.update_layout(
    margin=dict(t=20, b=20),
    height=520,
    coloraxis_showscale=True,
)
st.plotly_chart(fig, use_container_width=True)

# -- Footer ------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#aaa; font-size:0.85rem;'>"
    "Data from Jadarat Cleaned Dataset (Kaggle) - "
    "EDA by Abdullah Alkhurayjah</p>",
    unsafe_allow_html=True,
)
