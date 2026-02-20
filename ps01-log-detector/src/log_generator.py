import pandas as pd
import numpy as np
import os

def generate_advanced_logs(n_normal=2000, n_anomaly=40):
    """
    Generates a multi-feature synthetic log dataset for anomaly detection.
    """
    np.random.seed(42)
    
    # 1. Normal Traffic: Business hours, domestic locations, standard behavior
    normal_logs = {
        'hour': np.random.randint(8, 19, n_normal),
        'failed_attempts': np.random.randint(0, 2, n_normal),
        'data_transfer_mb': np.random.uniform(5, 100, n_normal),
        'location_idx': np.random.randint(0, 3, n_normal), # 0-2: "Trusted/Home"
        'is_admin': np.random.choice([0, 1], n_normal, p=[0.95, 0.05]),
        'session_sec': np.random.randint(300, 3600, n_normal),
        'label': 0
    }
    
    # 2. Anomaly Traffic: Off-hours, high failures, unusual data spikes
    anomaly_logs = {
        'hour': np.random.randint(0, 6, n_anomaly),
        'failed_attempts': np.random.randint(3, 15, n_anomaly),
        'data_transfer_mb': np.random.uniform(500, 2000, n_anomaly),
        'location_idx': np.random.randint(10, 15, n_anomaly), # 10-15: "Untrusted/VPN"
        'is_admin': np.random.choice([0, 1], n_anomaly, p=[0.4, 0.6]),
        'session_sec': np.random.randint(14400, 86400, n_anomaly),
        'label': 1
    }
    
    # 3. Combine and Shuffle
    df = pd.concat([pd.DataFrame(normal_logs), pd.DataFrame(anomaly_logs)])
    df = df.sample(frac=1).reset_index(drop=True)
    
    # 4. Save to CSV
    os.makedirs('data', exist_ok=True)
    output_path = 'data/system_logs.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Success: Dataset generated at {output_path}")
    print(f"📈 Total records: {len(df)} (Normal: {n_normal}, Anomalies: {n_anomaly})")

if __name__ == "__main__":
    # This block allows the script to be executed directly from the terminal
    generate_advanced_logs()