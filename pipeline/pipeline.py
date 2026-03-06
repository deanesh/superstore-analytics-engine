import os
import sys

# -------------------------------------------------
# FIX PYTHON PATH (important for Streamlit runs)
# -------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# -------------------------------------------------

from src.data_loader import load_data
from src.preprocess import preprocess_data
from src.analysis import rfm_segmentation, return_prediction
from src.plots import sales_trend, return_rate_plot


class SuperstorePipeline:

    def __init__(self, file_path):
        self.file_path = file_path

    def run(self):

        # Load datasets
        orders, people, returns = load_data(self.file_path)

        # Preprocess
        df = preprocess_data(orders, people, returns)

        # Customer segmentation
        rfm = rfm_segmentation(df)

        # ML model
        model = return_prediction(df)

        # Visualizations
        fig_sales = sales_trend(df)
        fig_returns = return_rate_plot(df)

        return df, rfm, model, fig_sales, fig_returns