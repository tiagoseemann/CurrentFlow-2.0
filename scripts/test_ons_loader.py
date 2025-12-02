"""
Test script for ONSLoader - downloads and parses ONS energy data.
"""

from src.data.loaders import ONSLoader


def main():
    """Test the ONSLoader class with real data download and parsing."""
    print("=" * 60)
    print("Testing ONSLoader")
    print("=" * 60)

    # Initialize loader
    loader = ONSLoader()
    print(f"\n1. Loader initialized")
    print(f"   Cache directory: {loader.cache_dir.absolute()}")

    # Load data for 2024 (will download if not cached)
    print(f"\n2. Loading data for 2024...")
    df = loader.load(2024)

    # Display basic info
    print(f"\n3. Data loaded successfully!")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"\n4. First 5 rows:")
    print(df.head())

    print(f"\n5. Data types:")
    print(df.dtypes)

    print(f"\n6. Basic statistics:")
    print(df.describe())

    # Check for regions
    if 'nom_subsistema' in df.columns:
        print(f"\n7. Unique regions found:")
        print(df['nom_subsistema'].unique())

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
