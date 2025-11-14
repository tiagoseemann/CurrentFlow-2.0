from pathlib import Path
import pandas as pd

def load_inmet(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=';', skiprows=10)

def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[[
        'Data Medicao',
        'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)',
        'TEMPERATURA MEDIA, DIARIA (AUT)(°C)'
    ]]
