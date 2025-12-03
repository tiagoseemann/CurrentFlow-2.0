"""
Update existing processed data with new advanced features.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.data.preprocessor import Preprocessor


def main():
    """Update features in existing parquet file."""
    data_path = Path("data/processed/energy_weather_processed.parquet")

    if not data_path.exists():
        print("Error: Processed data not found!")
        return

    print("Loading existing data...")
    df = pd.read_parquet(data_path)
    print(f"Current features: {df.shape[1]}")

    # Apply feature engineering again (this will add new features)
    print("\nReprocessing with new features...")
    preprocessor = Preprocessor()
    df_updated = preprocessor.engineer_features(df)

    print(f"New features: {df_updated.shape[1]}")

    # Save
    df_updated.to_parquet(data_path)
    print(f"\n✅ Updated data saved to {data_path}")
    print(f"   Added {df_updated.shape[1] - df.shape[1]} new features")


if __name__ == "__main__":
    main()
