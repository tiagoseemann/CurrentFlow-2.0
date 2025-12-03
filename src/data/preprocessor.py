"""
Data preprocessing module for energy analytics.

This module provides functionality to clean, aggregate, merge, and engineer
features from ONS and INMET raw data.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import numpy as np


class Preprocessor:
    """
    Preprocessor for ONS and INMET data.

    Handles data cleaning, aggregation by region, temporal merging,
    and feature engineering for the energy analytics pipeline.

    Example:
        >>> preprocessor = Preprocessor()
        >>> ons_df = ONSLoader().load(2023)
        >>> inmet_df = INMETLoader().load(2023)
        >>> clean_df = preprocessor.process(ons_df, inmet_df)
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize Preprocessor.

        Args:
            output_dir: Directory to save processed data.
                       Defaults to 'data/processed' in project root.
        """
        if output_dir is None:
            output_dir = Path("data/processed")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def clean_ons_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean ONS energy data.

        Steps:
            1. Remove null values in critical columns
            2. Remove duplicates
            3. Filter outliers (Z-score > 3)
            4. Ensure correct data types

        Args:
            df: Raw ONS DataFrame

        Returns:
            Cleaned ONS DataFrame
        """
        print("Cleaning ONS data...")
        initial_rows = len(df)

        # Make a copy to avoid modifying original
        clean_df = df.copy()

        # Remove rows with null values in critical columns
        clean_df = clean_df.dropna(subset=['din_instante', 'val_cargaenergiamwmed', 'nom_subsistema'])

        # Remove duplicates
        clean_df = clean_df.drop_duplicates(subset=['din_instante', 'nom_subsistema'])

        # Remove outliers (Z-score > 3)
        z_scores = np.abs(
            (clean_df['val_cargaenergiamwmed'] - clean_df['val_cargaenergiamwmed'].mean()) /
            clean_df['val_cargaenergiamwmed'].std()
        )
        clean_df = clean_df[z_scores <= 3]

        # Ensure datetime type
        if not pd.api.types.is_datetime64_any_dtype(clean_df['din_instante']):
            clean_df['din_instante'] = pd.to_datetime(clean_df['din_instante'])

        removed_rows = initial_rows - len(clean_df)
        print(f"✓ Removed {removed_rows} rows ({removed_rows/initial_rows*100:.2f}%)")
        print(f"✓ Clean data: {len(clean_df)} rows")

        return clean_df

    def aggregate_inmet_by_region(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate INMET data by region and date.

        Takes hourly station data and aggregates to daily regional averages.

        Args:
            df: Raw INMET DataFrame with hourly data from multiple stations

        Returns:
            Aggregated DataFrame with daily data by region
                - date: date
                - region: region name
                - temp_mean: mean temperature (°C)
                - temp_min: minimum temperature (°C)
                - temp_max: maximum temperature (°C)
                - radiation_mean: mean solar radiation (Kj/m²)
                - precipitation_total: total precipitation (mm)
        """
        print("Aggregating INMET data by region...")

        # Make a copy
        agg_df = df.copy()

        # Parse date column (format: YYYY/MM/DD or YYYY-MM-DD)
        if not pd.api.types.is_datetime64_any_dtype(agg_df['Data']):
            agg_df['Data'] = pd.to_datetime(agg_df['Data'], format='%Y/%m/%d', errors='coerce')
            if agg_df['Data'].isna().any():
                agg_df['Data'] = pd.to_datetime(agg_df['Data'], errors='coerce')

        # Extract date (remove time)
        agg_df['date'] = agg_df['Data'].dt.date

        # Column names from INMET (may vary)
        temp_col = 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'
        radiation_col = 'RADIACAO GLOBAL (Kj/m²)'
        precip_col = 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'

        # Aggregate by region and date
        aggregated = agg_df.groupby(['region', 'date']).agg({
            temp_col: ['mean', 'min', 'max'],
            radiation_col: 'mean',
            precip_col: 'sum'
        }).reset_index()

        # Flatten column names
        aggregated.columns = [
            'region', 'date',
            'temp_mean', 'temp_min', 'temp_max',
            'radiation_mean',
            'precipitation_total'
        ]

        # Convert date back to datetime for merging
        aggregated['date'] = pd.to_datetime(aggregated['date'])

        print(f"✓ Aggregated to {len(aggregated)} daily regional records")
        return aggregated

    def merge_ons_inmet(
        self,
        ons_df: pd.DataFrame,
        inmet_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge ONS energy data with INMET weather data.

        Performs temporal join on date and region.

        Args:
            ons_df: Cleaned ONS DataFrame
            inmet_df: Aggregated INMET DataFrame

        Returns:
            Merged DataFrame with energy load and weather data
        """
        print("Merging ONS and INMET data...")

        # Prepare ONS data
        ons_prep = ons_df.copy()
        ons_prep['date'] = ons_prep['din_instante'].dt.date
        ons_prep['date'] = pd.to_datetime(ons_prep['date'])

        # Rename region column to match
        ons_prep = ons_prep.rename(columns={'nom_subsistema': 'region'})

        # Merge on date and region
        merged = pd.merge(
            ons_prep[['date', 'region', 'val_cargaenergiamwmed']],
            inmet_df,
            on=['date', 'region'],
            how='inner'
        )

        print(f"✓ Merged to {len(merged)} records")
        return merged

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer derived features for analysis and ML.

        Creates:
            - Moving averages (7-day, 30-day)
            - Z-scores for anomaly detection
            - Month-over-month (MoM) changes
            - Year-over-year (YoY) changes
            - Day of week, month, season

        Args:
            df: Merged DataFrame

        Returns:
            DataFrame with additional engineered features
        """
        print("Engineering features...")

        feature_df = df.copy()

        # Sort by region and date for rolling calculations
        feature_df = feature_df.sort_values(['region', 'date'])

        # Time-based features
        feature_df['day_of_week'] = feature_df['date'].dt.dayofweek
        feature_df['month'] = feature_df['date'].dt.month
        feature_df['year'] = feature_df['date'].dt.year

        # Season (Brazil: Summer=Dec-Feb, Fall=Mar-May, Winter=Jun-Aug, Spring=Sep-Nov)
        feature_df['season'] = feature_df['month'].map({
            12: 'Summer', 1: 'Summer', 2: 'Summer',
            3: 'Fall', 4: 'Fall', 5: 'Fall',
            6: 'Winter', 7: 'Winter', 8: 'Winter',
            9: 'Spring', 10: 'Spring', 11: 'Spring'
        })

        # Moving averages (by region)
        for window in [7, 30]:
            feature_df[f'load_ma_{window}d'] = feature_df.groupby('region')['val_cargaenergiamwmed'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
            feature_df[f'temp_ma_{window}d'] = feature_df.groupby('region')['temp_mean'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )

        # Z-scores for anomaly detection
        feature_df['load_zscore'] = feature_df.groupby('region')['val_cargaenergiamwmed'].transform(
            lambda x: (x - x.mean()) / x.std()
        )

        # Binary anomaly flag (Z-score > 2.5)
        feature_df['is_anomaly'] = (np.abs(feature_df['load_zscore']) > 2.5).astype(int)

        # Month-over-month changes
        feature_df['load_mom'] = feature_df.groupby('region')['val_cargaenergiamwmed'].pct_change(periods=30)

        print(f"✓ Engineered {feature_df.shape[1]} features")
        return feature_df

    def process(
        self,
        ons_df: pd.DataFrame,
        inmet_df: pd.DataFrame,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Execute full preprocessing pipeline.

        Steps:
            1. Clean ONS data
            2. Aggregate INMET data by region
            3. Merge datasets
            4. Engineer features
            5. Save to Parquet (optional)

        Args:
            ons_df: Raw ONS DataFrame
            inmet_df: Raw INMET DataFrame
            save: Whether to save processed data to disk

        Returns:
            Fully processed DataFrame ready for analysis/ML

        Example:
            >>> preprocessor = Preprocessor()
            >>> result = preprocessor.process(ons_raw, inmet_raw)
        """
        print("\n" + "=" * 60)
        print("Starting data preprocessing pipeline")
        print("=" * 60 + "\n")

        # Step 1: Clean ONS data
        ons_clean = self.clean_ons_data(ons_df)

        # Step 2: Aggregate INMET data
        inmet_agg = self.aggregate_inmet_by_region(inmet_df)

        # Step 3: Merge datasets
        merged = self.merge_ons_inmet(ons_clean, inmet_agg)

        # Step 4: Engineer features
        final_df = self.engineer_features(merged)

        # Step 5: Save to disk
        if save:
            output_path = self.output_dir / "energy_weather_processed.parquet"
            final_df.to_parquet(output_path, index=False)
            print(f"\n✓ Saved processed data to {output_path}")

        print("\n" + "=" * 60)
        print("Preprocessing pipeline completed!")
        print(f"Final dataset: {final_df.shape[0]} rows × {final_df.shape[1]} columns")
        print("=" * 60 + "\n")

        return final_df
