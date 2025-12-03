"""
Compare Random Forest vs XGBoost for anomaly detection.

This script trains both models and compares their performance.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.anomaly_detector import AnomalyDetector, XGBOOST_AVAILABLE
import pandas as pd


def main():
    """Compare RF vs XGBoost."""
    print("=" * 70)
    print("MODEL COMPARISON: Random Forest vs XGBoost")
    print("=" * 70)

    # Load data
    data_path = Path("data/processed/energy_weather_processed.parquet")

    if not data_path.exists():
        print("Error: Processed data not found!")
        print("Please run: python scripts/test_pipeline.py")
        return

    print("\n📊 Loading data...")
    df = pd.read_parquet(data_path)
    print(f"   Loaded {len(df)} records")
    print(f"   Features: {df.shape[1]}")
    print(f"   Anomalies: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.2f}%)")

    # Train Random Forest
    print("\n" + "=" * 70)
    print("1️⃣  RANDOM FOREST")
    print("=" * 70)

    rf_detector = AnomalyDetector(model_type='random_forest', random_state=42)
    rf_metrics = rf_detector.train(df, test_size=0.2)

    # Train XGBoost (if available)
    if XGBOOST_AVAILABLE:
        print("\n" + "=" * 70)
        print("2️⃣  XGBOOST")
        print("=" * 70)

        xgb_detector = AnomalyDetector(model_type='xgboost', random_state=42)
        xgb_metrics = xgb_detector.train(df, test_size=0.2)

        # Comparison
        print("\n" + "=" * 70)
        print("🏆 COMPARISON RESULTS")
        print("=" * 70)

        print(f"\n{'Metric':<20} {'Random Forest':<20} {'XGBoost':<20}")
        print("-" * 60)
        print(f"{'Accuracy':<20} {rf_metrics['accuracy']:<20.3f} {xgb_metrics['accuracy']:<20.3f}")
        print(f"{'Precision':<20} {rf_metrics['precision']:<20.3f} {xgb_metrics['precision']:<20.3f}")
        print(f"{'Recall':<20} {rf_metrics['recall']:<20.3f} {xgb_metrics['recall']:<20.3f}")
        print(f"{'F1-Score':<20} {rf_metrics['f1_score']:<20.3f} {xgb_metrics['f1_score']:<20.3f}")
        print(f"{'N Features':<20} {rf_metrics['n_features']:<20} {xgb_metrics['n_features']:<20}")

        # Determine winner
        print("\n" + "=" * 70)
        if xgb_metrics['f1_score'] > rf_metrics['f1_score']:
            print("🥇 Winner: XGBoost (better F1-score)")
            winner = xgb_detector
            winner_name = 'xgboost'
        else:
            print("🥇 Winner: Random Forest (better F1-score)")
            winner = rf_detector
            winner_name = 'random_forest'

        # Save best model
        print(f"\n💾 Saving best model ({winner_name})...")
        winner.save()
        print("=" * 70)

    else:
        print("\n⚠️  XGBoost not available. Install with: uv add xgboost")
        print("   Saving Random Forest model...")
        rf_detector.save()

    print("\n✅ Comparison complete!")


if __name__ == "__main__":
    main()
