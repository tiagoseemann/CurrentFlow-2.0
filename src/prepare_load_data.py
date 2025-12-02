import pandas as pd
from pathlib import Path

def load_raw_load_data():
    """
    Lê o arquivo bruto de carga elétrica no diretório data/raw.
    Retorna o dataframe original.
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "CARGA_ENERGIA_2024.csv"
    return pd.read_csv(data_path, sep=';')


def preprocess_load_data(df):
    """
    Seleciona colunas úteis e converte para tipos adequados.

    Valores nulos -> zero

    Retorna dataframe pré-processado.
    """
    df = df[['din_instante', 'id_subsistema', 'val_cargaenergiamwmed']].copy()
    df['din_instante'] = pd.to_datetime(df['din_instante'])

    df['val_cargaenergiamwmed'] = df['val_cargaenergiamwmed'].fillna(0)
    return df


def filter_region(df, code):
    """
    Filtra a região com base no código do ONS.
    Renomeia colunas para manter padrão interno do projeto.
    """
    return (
        df[df['id_subsistema'] == code]
        .rename(columns={
            'din_instante': 'data',
            'id_subsistema': 'regiao',
            'val_cargaenergiamwmed': 'carga(MWmed)'
        })
        .reset_index(drop=True)
    )


def load_regions():
    """
    Carrega o CSV, pré-processa e retorna os 4 dataframes regionais (S, SE, N, NE).
    """
    raw = load_raw_load_data()
    base = preprocess_load_data(raw)

    df_sul      = filter_region(base, 'S')
    df_sudeste  = filter_region(base, 'SE')
    df_norte    = filter_region(base, 'N')
    df_nordeste = filter_region(base, 'NE')

    return df_sul, df_sudeste, df_norte, df_nordeste
