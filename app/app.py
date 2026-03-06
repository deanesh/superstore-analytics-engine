import os
import sys
import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Fix Python import path for fetch_data
# ---------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(APP_DIR, "model")

if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from fetch_data import get_analysis


# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
df, rfm, fig_sales, fig_returns = get_analysis()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "View Level",
    ["Regions", "States", "Districts", "Cities"]
)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>

.block-container{
padding-top:1rem;
}

.metric-box{
padding:14px;
border-radius:10px;
color:white;
text-align:center;
font-family:sans-serif;
margin-bottom:10px;
}

.blue{background:#1f77b4;}
.green{background:#2ca02c;}
.orange{background:#ff7f0e;}
.purple{background:#9467bd;}
.red{background:#d62728;}

.metric-title{
font-size:15px;
font-weight:bold;
}

.metric-value{
font-size:15px;
}

.metric-profit{
font-size:14px;
}

thead tr th{
background-color:#4CAF50 !important;
color:white !important;
font-weight:bold !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.markdown(
"""
<h1 style="
text-align:center;
font-size:32px;
font-weight:bold;
margin-top:10px;
margin-bottom:20px;
">
📊 Superstore Dashboard
</h1>
""",
unsafe_allow_html=True
)

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

colors = ["blue","green","orange","purple","red"]

def metric_box(title,sales,profit,color):

    st.markdown(
        f"""
        <div class="metric-box {color}">
            <div class="metric-title">{title}</div>
            <div class="metric-value">Sales: ₹{sales:,.0f}</div>
            <div class="metric-profit">Profit: ₹{profit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def top_performers(data,col):

    return (
        data.groupby(col)[["Sales","Profit"]]
        .sum()
        .sort_values("Sales",ascending=False)
        .head(5)
    )

# ---------------------------------------------------
# Regions / States / Districts / Cities
# ---------------------------------------------------

if page == "Regions":

    st.subheader("Top Regions")

    data = top_performers(df,"Region")

    cols = st.columns(len(data))

    for i,(name,row) in enumerate(data.iterrows()):
        with cols[i]:
            metric_box(name,row["Sales"],row["Profit"],colors[i%5])


elif page == "States":

    st.subheader("Top States")

    data = top_performers(df,"State")

    cols = st.columns(len(data))

    for i,(name,row) in enumerate(data.iterrows()):
        with cols[i]:
            metric_box(name,row["Sales"],row["Profit"],colors[i%5])


elif page == "Districts":

    st.subheader("Top Districts")

    data = top_performers(df,"District")

    styled = data.style.format({
        "Sales":"₹{:,.0f}",
        "Profit":"₹{:,.0f}"
    })

    st.table(styled)


elif page == "Cities":

    st.subheader("Top Cities")

    data = top_performers(df,"City")

    styled = data.style.format({
        "Sales":"₹{:,.0f}",
        "Profit":"₹{:,.0f}"
    })

    st.table(styled)

# ---------------------------------------------------
# Product Categories
# ---------------------------------------------------

st.subheader("📦 Product Categories")

category_data = (
    df.groupby("Category")[["Sales","Profit"]]
    .sum()
    .sort_values("Sales",ascending=False)
)

cols = st.columns(len(category_data))

for i,(cat,row) in enumerate(category_data.iterrows()):
    with cols[i]:
        metric_box(cat,row["Sales"],row["Profit"],colors[i%5])

# ---------------------------------------------------
# Profit Ratio
# ---------------------------------------------------

st.subheader("📊 Profit Ratio by Category")

profit_ratio = df.groupby("Category")[["Sales","Profit"]].sum()

profit_ratio["Profit Ratio (%)"] = (
profit_ratio["Profit"] / profit_ratio["Sales"]
) * 100

profit_ratio = profit_ratio[["Profit Ratio (%)"]].round(2)

st.caption("Formula: Profit / Sales × 100")

st.table(profit_ratio)

# ---------------------------------------------------
# Customer Segments
# ---------------------------------------------------

st.subheader("👥 Customer Segments")

rfm_display = rfm.copy()

rfm_display = rfm_display.rename(columns={

"CustomerID":"Customer",
"Monetary":"Total Spending (₹)",
"Recency":"Days Since Last Purchase",
"Frequency":"Total Orders",
"Cluster":"Customer Segment"

})

rfm_display = rfm_display.head(3)

st.table(rfm_display)