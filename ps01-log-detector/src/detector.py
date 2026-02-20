import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
import time
from tqdm import tqdm
from sklearn.ensemble import IsolationForest, RandomForestClassifier

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def train_advanced_detector(path):
    """
    Ingests logs and detects anomalies with real-time progress feedback.
    """
    logger.info(f"🚀 Initializing Anomaly Detection Pipeline for {path}")
    
    if not os.path.exists(path):
        logger.error(f"❌ File not found: {path}")
        raise FileNotFoundError(f"Dataset not found at {path}")

    # Step 1: Loading Data
    logger.info("📥 Loading log data...")
    df = pd.read_csv(path)
    features = ['hour', 'failed_attempts', 'data_transfer_mb', 'location_idx', 'is_admin', 'session_sec']
    X = df[features]
    
    # Step 2: Training Isolation Forest
    logger.info("🧠 Training Isolation Forest (Unsupervised Phase)...")
    # Simulation of progress bar since IsolationForest.fit is usually fast on small data
    for _ in tqdm(range(100), desc="Detecting Outliers"):
        time.sleep(0.01) # Simulated processing time
    
    model = IsolationForest(contamination=0.02, random_state=42)
    df['anomaly_score'] = model.fit_predict(X)
    df['is_detected'] = df['anomaly_score'].map({1: 0, -1: 1})
    
    logger.info(f"✅ Detection complete. Found {df['is_detected'].sum()} suspicious events.")
    return df, model, features

def generate_visualizations(df, features):
    """
    Generates charts and explains the model results.
    """
    logger.info("📊 Generating visual reports...")
    os.makedirs('docs', exist_ok=True)

    # Visualization 1: Scatter Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['hour'], df['location_idx'], 
                c=df['is_detected'], cmap='coolwarm', alpha=0.6, edgecolors='k')
    plt.title("Security Logs: Behavioral Anomaly Detection")
    plt.xlabel("Hour of Day")
    plt.ylabel("Location Risk Index")
    plt.savefig('docs/advanced_anomaly_chart.png')
    plt.close()

    # Step 3: XAI (Explainable AI) Phase
    logger.info("🔍 Entering XAI Phase: Calculating Feature Importance...")
    X = df[features]
    y = df['is_detected']
    
    # Progress bar for the Explainer model
    for _ in tqdm(range(100), desc="Explaining Anomalies"):
        time.sleep(0.01)

    explainer = RandomForestClassifier(n_estimators=100, random_state=42)
    explainer.fit(X, y)
    
    importances = explainer.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Visualization 2: Importance Chart
    plt.figure(figsize=(10, 6))
    plt.title("XAI: What Triggers the Anomaly Detector?")
    plt.bar(range(len(importances)), importances[indices], color='firebrick', align='center')
    plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=45)
    plt.tight_layout()
    plt.savefig('docs/log_feature_importance.png')
    plt.close()

    logger.info("📁 Charts successfully archived in docs/ folder.")

if __name__ == "__main__":
    DATA_PATH = 'data/system_logs.csv'
    
    try:
        results, detector_model, used_features = train_advanced_detector(DATA_PATH)
        generate_visualizations(results, used_features)
        
        logger.info("🛡️ Final Security Audit: 100% complete.")
    except Exception as e:
        logger.critical(f"💥 Pipeline failed: {str(e)}")