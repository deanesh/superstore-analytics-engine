import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from pipeline.pipeline import SuperstorePipeline


file_path = "data/indian_superstore_data.xlsx"

pipeline = SuperstorePipeline(file_path)

df, rfm, model, fig_sales, fig_returns = pipeline.run()

st.title("Superstore Sales Insights")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Sales Trend")
st.pyplot(fig_sales)

st.subheader("Return Rate by Category")
st.pyplot(fig_returns)

st.subheader("Customer Segments")
st.dataframe(rfm.head())