import pandas as pd
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