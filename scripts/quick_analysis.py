"""
Quick analysis of processed data to verify quality and generate insights.
"""

import pandas as pd


def main():
    """Load and analyze processed data."""
    print("\n" + "=" * 70)
    print("QUICK DATA ANALYSIS")
    print("=" * 70 + "\n")

    # Load processed data
    df = pd.read_parquet("data/processed/energy_weather_processed.parquet")

    print(f"Dataset Overview:")
    print(f"  - Records: {len(df):,}")
    print(f"  - Features: {df.shape[1]}")
    print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  - Regions: {', '.join(df['region'].unique())}")

    print(f"\n\nData Quality:")
    print(f"  - Missing values: {df.isnull().sum().sum()}")
    print(f"  - Duplicates: {df.duplicated().sum()}")

    print(f"\n\nEnergy Load Statistics (MW):")
    stats = df.groupby('region')['val_cargaenergiamwmed'].agg([
        ('Mean', 'mean'),
        ('Std', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2)
    print(stats)

    print(f"\n\nTemperature Statistics (°C):")
    temp_stats = df.groupby('region')['temp_mean'].agg([
        ('Mean', 'mean'),
        ('Std', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2)
    print(temp_stats)

    print(f"\n\nAnomaly Detection Results:")
    anomaly_counts = df.groupby('region')['is_anomaly'].agg([
        ('Total_Anomalies', 'sum'),
        ('Anomaly_Rate_%', lambda x: (x.sum() / len(x)) * 100)
    ]).round(2)
    print(anomaly_counts)

    print(f"\n\nTop 5 Anomalies (Highest Z-scores):")
    top_anomalies = df.nlargest(5, 'load_zscore')[
        ['date', 'region', 'val_cargaenergiamwmed', 'temp_mean', 'load_zscore']
    ]
    print(top_anomalies.to_string(index=False))

    print(f"\n\nSeasonal Average Load (MW):")
    seasonal = df.groupby(['region', 'season'])['val_cargaenergiamwmed'].mean().unstack().round(2)
    print(seasonal)

    print(f"\n\nCorrelation: Energy Load vs Temperature:")
    corr = df.groupby('region').apply(
        lambda x: x['val_cargaenergiamwmed'].corr(x['temp_mean'])
    ).round(3)
    print(corr)

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
