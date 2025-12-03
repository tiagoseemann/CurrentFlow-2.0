"""
Test script for INMETLoader - downloads and parses INMET weather data.
"""

from src.data.loaders import INMETLoader


def main():
    """Test the INMETLoader class with real data download and parsing."""
    print("=" * 60)
    print("Testing INMETLoader")
    print("=" * 60)

    # Initialize loader
    loader = INMETLoader()
    print(f"\n1. Loader initialized")
    print(f"   Cache directory: {loader.cache_dir.absolute()}")

    # Load data for 2023 (more stable than 2024)
    print(f"\n2. Loading data for 2023...")
    try:
        df = loader.load(2023)

        # Display basic info
        print(f"\n3. Data loaded successfully!")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)[:10]}...")  # First 10 columns

        print(f"\n4. First 3 rows:")
        print(df.head(3))

        print(f"\n5. Data types (first 10):")
        print(df.dtypes[:10])

        # Check regions
        print(f"\n6. Stations by region:")
        print(df.groupby('region')['station_code'].nunique())

        print(f"\n7. Unique station codes (first 20):")
        print(sorted(df['station_code'].unique())[:20])

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis might be expected if:")
        print("1. INMET changed their URL structure")
        print("2. 2023 data is not available")
        print("3. Network issues")
        print("\nTry testing with a different year or check INMET portal.")


if __name__ == "__main__":
    main()
