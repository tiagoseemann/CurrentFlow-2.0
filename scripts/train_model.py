"""
Train the simple Random Forest anomaly detector.

This script loads the processed data, trains the model,
evaluates it, and saves it for use in the dashboard.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.anomaly_detector import AnomalyDetector
import pandas as pd


def main():
    """Train and evaluate the anomaly detector."""
    print("=" * 60)
    print("TRAINING ANOMALY DETECTION MODEL")
    print("=" * 60)

    # Load processed data
    data_path = Path("data/processed/energy_weather_processed.parquet")

    if not data_path.exists():
        print("Error: Processed data not found!")
        print("Please run: python scripts/test_pipeline.py")
        return

    print("\n1. Loading data...")
    df = pd.read_parquet(data_path)
    print(f"   Loaded {len(df)} records")
    print(f"   Anomalies in data: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.2f}%)")

    # Check if we have enough anomalies
    if df['is_anomaly'].sum() < 5:
        print("\n   Warning: Very few anomalies in the dataset.")
        print("   The model may not perform well.")

    # Initialize and train model
    print("\n2. Initializing model...")
    detector = AnomalyDetector(random_state=42)

    print("\n3. Training model (80/20 train/test split)...")
    metrics = detector.train(df, test_size=0.2)

    # Feature importance
    print("\n4. Feature Importance:")
    importance = detector.get_feature_importance()
    print(importance.to_string(index=False))

    # Save model
    print("\n5. Saving model...")
    detector.save()

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\nModel saved to: data/models/anomaly_detector.pkl")
    print(f"Accuracy: {metrics['accuracy']:.1%}")
    print(f"F1-Score: {metrics['f1_score']:.3f}")
    print("\nYou can now use this model in the dashboard!")


if __name__ == "__main__":
    main()
