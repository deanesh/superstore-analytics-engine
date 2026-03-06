import logging
import os

def get_logger():

    os.makedirs("logs", exist_ok=True)


    logging.basicConfig(
        filename="logs/superstore_analytics.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
    )

    return logging.getLogger(__name__)