import os
import sys

# -----------------------------
# Add pipeline to sys.path
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PIPELINE_DIR = os.path.join(ROOT_DIR, "pipeline")
if PIPELINE_DIR not in sys.path:
    sys.path.insert(0, PIPELINE_DIR)

from pipeline import SuperstorePipeline

def get_analysis():
    file_path = os.path.join(ROOT_DIR, "data", "indian_superstore_data.xlsx")
    pipeline = SuperstorePipeline(file_path)
    df, rfm, _, fig_sales, fig_returns = pipeline.run()
    return df, rfm, fig_sales, fig_returns