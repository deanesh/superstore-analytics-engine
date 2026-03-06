import os
import sys

# -----------------------------
# Add pipeline folder to sys.path
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PIPELINE_DIR = os.path.join(ROOT_DIR, "pipeline")
if PIPELINE_DIR not in sys.path:
    sys.path.insert(0, PIPELINE_DIR)

from pipeline import SuperstorePipeline  # direct import from pipeline.py

def main():
    file_path = os.path.join("data", "indian_superstore_data.xlsx")
    pipeline = SuperstorePipeline(file_path)
    pipeline.run()

if __name__ == "__main__":
    main()