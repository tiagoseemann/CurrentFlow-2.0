"""
Data loaders for ONS (Operador Nacional do Sistema Elétrico) data.
"""


class ONSLoader:
    """Loader for ONS electrical system data."""

    def __init__(self, cache_dir: str = "data/raw"):
        """
        Initialize ONS data loader.

        Args:
            cache_dir: Directory to store cached data files
        """
        self.cache_dir = cache_dir
