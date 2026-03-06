import os
import sys
import streamlit as st

# -----------------------------
# Setup sys.path for pipeline and model
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PIPELINE_DIR = os.path.join(ROOT_DIR, "pipeline")
MODEL_DIR = os.path.join(ROOT_DIR, "app", "model")

for folder in [PIPELINE_DIR, MODEL_DIR]:
    if folder not in sys.path:
        sys.path.insert(0, folder)

# -----------------------------
# Imports
# -----------------------------
from pipeline import SuperstorePipeline
from fetch_data import get_analysis

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Superstore Analytics", page_icon="📊", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
df, rfm, fig_sales, fig_returns = get_analysis()

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio("Select Level", ["🌏 Regions", "🗺 States", "🏙 Districts", "🌆 Cities"])

# -----------------------------
# Helper Function
# -----------------------------
def top_performers(data, group_col):
    return data.groupby(group_col).agg({"Sales":"sum","Profit":"sum","Quantity":"sum"}).sort_values("Sales", ascending=False).head(5)

# -----------------------------
# Dashboard
# -----------------------------
st.title("📊 Superstore Sales Intelligence Dashboard")

if page == "🌏 Regions":
    st.subheader("Top Regions Performance")
    region_data = top_performers(df, "Region")
    cols = st.columns(5)
    for i, (region, row) in enumerate(region_data.iterrows()):
        with cols[i]:
            st.metric(f"🌏 {region}", f"₹{row['Sales']:,.0f}", f"Profit ₹{row['Profit']:,.0f}")
    st.markdown("---")
    st.pyplot(fig_sales)

elif page == "🗺 States":
    st.subheader("Top States Performance")
    state_data = top_performers(df, "State")
    for state, row in state_data.iterrows():
        col1, col2, col3 = st.columns([2,1,1])
        with col1: st.write(f"### 🗺 {state}")
        with col2: st.metric("Sales", f"₹{row['Sales']:,.0f}")
        with col3: st.metric("Profit", f"₹{row['Profit']:,.0f}")

elif page == "🏙 Districts":
    st.subheader("Top District Performance")
    st.dataframe(top_performers(df, "District"))

elif page == "🌆 Cities":
    st.subheader("Top Cities Performance")
    st.dataframe(top_performers(df, "City"))

st.markdown("---")
st.subheader("📦 Product Category Performance")
product_icons = {"Furniture":"🪑","Office Supplies":"📎","Technology":"💻"}
cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
cols = st.columns(len(cat))
for i, (category, value) in enumerate(cat.items()):
    with cols[i]: st.metric(f"{product_icons.get(category,'📦')} {category}", f"₹{value:,.0f}")

st.markdown("---")
st.subheader("📉 Return Analysis")
st.pyplot(fig_returns)

st.markdown("---")
st.subheader("👥 Customer Segments (RFM Clusters)")
st.dataframe(rfm.head(20))