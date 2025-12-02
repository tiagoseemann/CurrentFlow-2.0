import pandas as pd

def standardize_weather(df):
    """
    Padroniza nomes das colunas e converte a data.
    Mantém apenas temperatura e precipitação.
    """
    df = df.rename(columns={
        'Data Medicao': 'data',
        'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)': 'precipitacao',
        'TEMPERATURA MEDIA, DIARIA (AUT)(°C)': 'temperatura'
    })
    df['data'] = pd.to_datetime(df['data'])
    return df


def fix_decimal_commas(df):
    """
    Converte números no formato '12,4' para formato float.
    Aplica isso para temperatura e precipitação.

    Trata valores nulos:
        - Precipitação -> Zera o valor
        - Temperatura -> Descarta a linha
    """
    df['temperatura'] = df['temperatura'].astype(str).replace(',', '.', regex=True).astype(float)
    df['precipitacao'] = df['precipitacao'].astype(str).replace(',', '.', regex=True).astype(float)

    # Precipitação nula
    df['precipitacao'] = df['precipitacao'].fillna(0)

    # Temperatura nula
    df = df.dropna(subset=['temperatura'])

    return df
    return df


def merge_weather_files(dfs):
    """
    Concatena vários arquivos de clima da região.
    Tira a média diária entre estações diferentes.
    """
    df = pd.concat(dfs, ignore_index=True)
    return df.groupby('data')[['temperatura', 'precipitacao']].mean().reset_index()
