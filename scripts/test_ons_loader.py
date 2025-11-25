"""
Test script for ONSLoader verification.
"""

from src.data.loaders import ONSLoader


def main():
    """Test the ONSLoader class."""
    print("Testing ONSLoader...")

    loader = ONSLoader()
    print(f"ONSLoader initialized with cache_dir: {loader.cache_dir}")
    print("✓ ONSLoader test passed!")


if __name__ == "__main__":
    main()
