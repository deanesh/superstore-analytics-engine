import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from utils.logger import get_logger
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix

import sys
import os

# Add project root to sys.path so sibling folders like 'utils' can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.logger import get_logger

# Fix KMeans memory leak on Windows
os.environ["OMP_NUM_THREADS"] = "4"

logger = get_logger()


def rfm_segmentation(df, n_clusters=4):
    """
    RFM segmentation for customers using KMeans.
    """
    logger.info("Running RFM segmentation")
    snapshot = df["Order Date"].max()

    rfm = df.groupby("Customer ID").agg({
        "Order Date": lambda x: (snapshot - x.max()).days,
        "Order ID": "count",
        "Sales": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(np.log1p(rfm))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

    return rfm


def return_prediction(df, threshold=0.3):
    """
    Trains a return prediction model using XGBoost with a custom probability threshold.
    Improves detection of returned orders (minority class).
    
    threshold: float, probability cutoff for predicting class 1 (default 0.3)
    """
    logger.info("Training return prediction model with XGBoost")

    # Add customer-level features
    df["Customer_Order_Count"] = df.groupby("Customer ID")["Order ID"].transform("count")
    df["Customer_Total_Sales"] = df.groupby("Customer ID")["Sales"].transform("sum")
    df["Avg_Order_Value"] = df["Customer_Total_Sales"] / df["Customer_Order_Count"]

    features = [
        "Ship Mode",
        "Segment",
        "Region",
        "Category",
        "Sales",
        "Quantity",
        "Discount",
        "Days_to_Ship",
        "Customer_Order_Count",
        "Customer_Total_Sales",
        "Avg_Order_Value"
    ]

    X = df[features].copy()
    y = df["Returned"].apply(lambda x: 1 if x == "Yes" else 0)

    # One-Hot Encoding for categorical features
    categorical_cols = ["Ship Mode", "Segment", "Region", "Category"]
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    # Scale numeric features for SMOTE
    numeric_cols = ["Sales", "Quantity", "Discount", "Days_to_Ship",
                    "Customer_Order_Count", "Customer_Total_Sales", "Avg_Order_Value"]
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    # Stratified train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Balance minority class with SMOTE
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    # Train XGBoost
    model = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=5,
        learning_rate=0.1,
        scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),  # balance
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)

    # Predict probabilities and apply custom threshold
    preds_proba = model.predict_proba(X_test)[:, 1]
    preds = (preds_proba > threshold).astype(int)

    # Evaluation
    print("Classification Report:")
    print(classification_report(y_test, preds))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

    # Feature importance
    importance = model.feature_importances_
    print("\nFeature Importances:")
    for name, score in sorted(zip(X.columns, importance), key=lambda x: x[1], reverse=True):
        print(f"{name}: {score:.3f}")

    logger.info("XGBoost model training complete")
    return model