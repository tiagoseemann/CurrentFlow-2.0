from pathlib import Path
import pandas as pd

def load_inmet_file(path: Path) -> pd.DataFrame:
    """
    Lê arquivo bruto do INMET.
    Ignora as 10 primeiras linhas (metadados).
    """
    return pd.read_csv(path, sep=';', skiprows=10)


def select_relevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mantém apenas as colunas necessárias para processamento posterior.
    """
    return df[[
        'Data Medicao',
        'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)',
        'TEMPERATURA MEDIA, DIARIA (AUT)(°C)'
    ]]
