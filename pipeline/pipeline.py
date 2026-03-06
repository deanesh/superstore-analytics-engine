import os
import sys

# -----------------------------
# Add src and utils to sys.path dynamically
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
UTILS_DIR = os.path.join(ROOT_DIR, "utils")

for folder in [SRC_DIR, UTILS_DIR]:
    if folder not in sys.path:
        sys.path.insert(0, folder)

# -----------------------------
# Imports
# -----------------------------
from data_loader import load_data
from preprocess import preprocess_data
from analysis import rfm_segmentation, return_prediction
from plots import sales_trend, return_rate_plot

class SuperstorePipeline:
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self):
        orders, people, returns = load_data(self.file_path)
        df = preprocess_data(orders, people, returns)
        rfm = rfm_segmentation(df)
        model = return_prediction(df)
        fig_sales = sales_trend(df)
        fig_returns = return_rate_plot(df)
        return df, rfm, model, fig_sales, fig_returns