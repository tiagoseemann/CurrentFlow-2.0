"""
Test script for the complete data pipeline: ONS + INMET + Preprocessor.

This script demonstrates the full data processing workflow:
1. Load ONS energy data
2. Load INMET weather data
3. Clean, merge, and engineer features
4. Save processed data to Parquet
"""

from src.data.loaders import ONSLoader, INMETLoader
from src.data.preprocessor import Preprocessor


def main():
    """Test the complete data pipeline."""
    print("\n" + "=" * 70)
    print("ENERGY ANALYTICS - DATA PIPELINE TEST")
    print("=" * 70 + "\n")

    # Use 2023 data (more complete than 2024)
    year = 2023

    # Step 1: Load ONS data
    print(f"[1/4] Loading ONS energy data for {year}...")
    ons_loader = ONSLoader()
    ons_df = ons_loader.load(year)
    print(f"      ONS data shape: {ons_df.shape}")

    # Step 2: Load INMET data
    print(f"\n[2/4] Loading INMET weather data for {year}...")
    inmet_loader = INMETLoader()
    inmet_df = inmet_loader.load(year)
    print(f"      INMET data shape: {inmet_df.shape}")

    # Step 3: Process data
    print(f"\n[3/4] Processing and merging data...")
    preprocessor = Preprocessor()
    processed_df = preprocessor.process(ons_df, inmet_df, save=True)

    # Step 4: Display results
    print(f"\n[4/4] Pipeline Results:")
    print(f"      Final shape: {processed_df.shape}")
    print(f"\n      Columns: {list(processed_df.columns)}")
    print(f"\n      First 5 rows:")
    print(processed_df.head())

    print(f"\n      Data by region:")
    print(processed_df.groupby('region').agg({
        'val_cargaenergiamwmed': 'mean',
        'temp_mean': 'mean',
        'is_anomaly': 'sum'
    }).round(2))

    print(f"\n      Anomaly statistics:")
    print(f"      Total anomalies detected: {processed_df['is_anomaly'].sum()}")
    print(f"      Anomaly rate: {processed_df['is_anomaly'].mean()*100:.2f}%")

    print("\n" + "=" * 70)
    print("✓ PIPELINE TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
