"""
Data loaders for ONS (Operador Nacional do Sistema Elétrico) and INMET data.
"""

from pathlib import Path
from typing import Optional, List
import requests
import pandas as pd
import zipfile
import io
from src.utils.config import extract_state_from_filename, get_region_from_state


class ONSLoader:
    """
    Loader for ONS electrical system data.

    Downloads and caches daily energy load data from ONS (Operador Nacional
    do Sistema Elétrico). Data is available from 2000 onwards.

    Example:
        >>> loader = ONSLoader()
        >>> df = loader.load(2024)
        >>> print(df.head())
    """

    BASE_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/carga_energia_di"

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize ONS data loader.

        Args:
            cache_dir: Directory to store cached data files.
                      Defaults to 'data/raw' in project root.
        """
        if cache_dir is None:
            cache_dir = Path("data/raw")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, year: int) -> Path:
        """
        Get the local cache file path for a given year.

        Args:
            year: Year of the data (e.g., 2024)

        Returns:
            Path object pointing to the cached CSV file
        """
        return self.cache_dir / f"CARGA_ENERGIA_{year}.csv"

    def _download(self, year: int) -> Path:
        """
        Download ONS data for a specific year.

        Args:
            year: Year to download (e.g., 2024)

        Returns:
            Path to the downloaded file

        Raises:
            requests.HTTPError: If download fails (e.g., year not available)
        """
        url = f"{self.BASE_URL}/CARGA_ENERGIA_{year}.csv"
        cache_path = self._get_cache_path(year)

        print(f"Downloading ONS data for {year} from {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Fail fast on HTTP errors

        # Save to cache
        cache_path.write_bytes(response.content)
        print(f"✓ Downloaded and cached at {cache_path}")

        return cache_path

    def load(self, year: int = 2024) -> pd.DataFrame:
        """
        Load ONS energy data for a given year.

        Downloads from ONS if not in cache, otherwise uses cached version.

        Args:
            year: Year to load (defaults to 2024)

        Returns:
            DataFrame with columns:
                - din_instante: timestamp
                - nom_subsistema: region name (SUL, SUDESTE, etc.)
                - val_cargaenergiamwmed: energy load in MW (average)

        Example:
            >>> loader = ONSLoader()
            >>> df = loader.load(2024)
            >>> print(df.shape)
            (8760, 3)  # ~365 days * 24 hours
        """
        cache_path = self._get_cache_path(year)

        # Download if not cached
        if not cache_path.exists():
            cache_path = self._download(year)
        else:
            print(f"Using cached data from {cache_path}")

        # Parse CSV with Brazilian locale (sep=';', decimal=',')
        df = pd.read_csv(
            cache_path,
            sep=";",
            decimal=",",
            encoding="utf-8"
        )

        # Convert data types
        df['din_instante'] = pd.to_datetime(df['din_instante'])
        df['val_cargaenergiamwmed'] = pd.to_numeric(
            df['val_cargaenergiamwmed'],
            errors='coerce'
        )

        print(f"✓ Loaded {len(df)} rows for year {year}")
        return df


class INMETLoader:
    """
    Loader for INMET (Instituto Nacional de Meteorologia) weather data.

    Downloads and processes meteorological data from INMET's historical database.
    Data includes temperature, humidity, radiation, and other weather variables
    from weather stations across Brazil.

    Example:
        >>> loader = INMETLoader()
        >>> df = loader.load(2024)
        >>> print(df.head())
    """

    BASE_URL = "https://portal.inmet.gov.br/uploads/dadoshistoricos"

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize INMET data loader.

        Args:
            cache_dir: Directory to store cached data files.
                      Defaults to 'data/raw/inmet' in project root.
        """
        if cache_dir is None:
            cache_dir = Path("data/raw/inmet")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, year: int) -> Path:
        """
        Get the local cache file path for a given year.

        Args:
            year: Year of the data (e.g., 2024)

        Returns:
            Path object pointing to the cached ZIP file
        """
        return self.cache_dir / f"INMET_{year}.zip"

    def _download(self, year: int) -> Path:
        """
        Download INMET data for a specific year.

        Args:
            year: Year to download (e.g., 2024)

        Returns:
            Path to the downloaded ZIP file

        Raises:
            requests.HTTPError: If download fails
        """
        url = f"{self.BASE_URL}/{year}.zip"
        cache_path = self._get_cache_path(year)

        print(f"Downloading INMET data for {year} from {url}...")
        response = requests.get(url, timeout=120)
        response.raise_for_status()

        # Save to cache
        cache_path.write_bytes(response.content)
        print(f"✓ Downloaded and cached at {cache_path}")

        return cache_path

    def _extract_station_data(self, zip_path: Path) -> List[pd.DataFrame]:
        """
        Extract and parse all station CSV files from ZIP.

        Args:
            zip_path: Path to the ZIP file

        Returns:
            List of DataFrames, one per weather station
        """
        dataframes = []

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.CSV')]

            print(f"Found {len(csv_files)} station files in ZIP")

            for csv_file in csv_files:
                try:
                    # Read CSV from ZIP
                    with zip_ref.open(csv_file) as file:
                        # INMET CSVs use ';' separator and skip first 8 rows (header info)
                        df = pd.read_csv(
                            file,
                            sep=';',
                            encoding='latin-1',
                            skiprows=8,
                            decimal=','
                        )

                        # Extract station code and state from filename
                        # Typical format: INMET_SE_MG_A001_BELO_HORIZONTE_01-01-2024_A_31-12-2024.CSV
                        parts = csv_file.split('_')
                        station_code = parts[3] if len(parts) > 3 else 'UNKNOWN'
                        state_code = extract_state_from_filename(csv_file)

                        # Add metadata
                        df['station_code'] = station_code
                        df['state_code'] = state_code
                        df['source_file'] = csv_file

                        dataframes.append(df)

                except Exception as e:
                    print(f"Warning: Failed to parse {csv_file}: {e}")
                    continue

        return dataframes

    def _map_region(self, state_code: str) -> str:
        """
        Map a state code to its Brazilian region.

        Args:
            state_code: Two-letter state code (e.g., 'MG', 'SP')

        Returns:
            Region name ('Norte', 'Nordeste', 'Sudeste/Centro-Oeste', or 'Sul')
        """
        return get_region_from_state(state_code)

    def load(self, year: int = 2024) -> pd.DataFrame:
        """
        Load INMET weather data for a given year.

        Downloads from INMET if not in cache, otherwise uses cached version.
        Extracts all station data and combines into a single DataFrame.

        Args:
            year: Year to load (defaults to 2024)

        Returns:
            DataFrame with weather data from all stations, including:
                - Data: date
                - Hora UTC: hour (UTC)
                - TEMPERATURA DO AR - BULBO SECO, HORARIA (°C): temperature
                - RADIACAO GLOBAL (Kj/m²): solar radiation
                - station_code: weather station identifier
                - region: Brazilian region (N, NE, SE/CO, S)

        Example:
            >>> loader = INMETLoader()
            >>> df = loader.load(2024)
            >>> print(df.groupby('region')['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean())
        """
        cache_path = self._get_cache_path(year)

        # Download if not cached
        if not cache_path.exists():
            cache_path = self._download(year)
        else:
            print(f"Using cached data from {cache_path}")

        # Extract all station data
        station_dfs = self._extract_station_data(cache_path)

        if not station_dfs:
            raise ValueError(f"No valid station data found in {cache_path}")

        # Combine all stations
        df = pd.concat(station_dfs, ignore_index=True)

        # Map regions based on state code
        df['region'] = df['state_code'].apply(self._map_region)

        print(f"✓ Loaded {len(df)} rows from {len(station_dfs)} stations for year {year}")
        print(f"✓ Regions found: {df['region'].unique()}")

        return df
