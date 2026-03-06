import pandas as pd
import sys
import os

# Add project root to sys.path so sibling folders like 'utils' can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.logger import get_logger

logger = get_logger()

def load_data(file_path):

    try:
        orders = pd.read_excel(file_path, sheet_name="Orders")
        people = pd.read_excel(file_path, sheet_name="People")
        returns = pd.read_excel(file_path, sheet_name="Returns")

        logger.info("Data loaded successfully")

        return orders, people, returns

    except Exception as e:
        logger.error(f"Data loading failed: {e}")
        raise