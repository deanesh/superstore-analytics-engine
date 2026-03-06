import pandas as pd
import sys
import os

# Add project root to sys.path so sibling folders like 'utils' can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.logger import get_logger
from utils.logger import get_logger

logger = get_logger()

def preprocess_data(orders, people, returns):

    logger.info("Starting preprocessing")

    orders["Order Date"] = pd.to_datetime(orders["Order Date"])
    orders["Ship Date"] = pd.to_datetime(orders["Ship Date"])

    returns_unique = returns.drop_duplicates(subset="Order ID")

    df = orders.merge(people, on="Region", how="left")
    df = df.merge(returns_unique, on="Order ID", how="left")

    df["Returned"] = df["Returned"].fillna("No")

    df["Days_to_Ship"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    logger.info("Preprocessing completed")

    return df