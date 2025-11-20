import pandas as pd

def standardize(df):
    df = df.rename(columns={
        'Data Medicao': 'data',
        'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)': 'precipitacao',
        'TEMPERATURA MEDIA, DIARIA (AUT)(°C)': 'temperatura'
    })
    df['data'] = pd.to_datetime(df['data'])
    return df


def fix_commas(df):
    df['temperatura'] = df['temperatura'].astype(str).str.replace(',', '.').astype(float)
    df['precipitacao'] = df['precipitacao'].astype(str).str.replace(',', '.').astype(float)
    return df


def merge_region(dfs):
    df = pd.concat(dfs, ignore_index=True)
    return df.groupby('data')[['temperatura', 'precipitacao']].mean().reset_index()
