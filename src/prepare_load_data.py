import pandas as pd
from pathlib import Path


def load_raw_load_data():
    """
    Lê o arquivo bruto de carga elétrica na pasta data/raw.
    Retorna o dataframe original.
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "CARGA_ENERGIA_2024.csv"

    return pd.read_csv(data_path, sep=';')


def preprocess_load_data(df):
    """
    Seleciona colunas relevantes e converte tipos.
    Retorna dataframe pré-processado.
    """
    df = df[['din_instante', 'id_subsistema', 'val_cargaenergiamwmed']].copy()
    df['din_instante'] = pd.to_datetime(df['din_instante'])
    return df


def filtrar_regiao(df, codigo):
    """
    Filtra região pelo código oficial do ONS.
    Renomeia colunas para padronização interna.
    """
    return (
        df[df['id_subsistema'] == codigo]
        .rename(columns={
            'din_instante': 'data',
            'id_subsistema': 'regiao',
            'val_cargaenergiamwmed': 'carga(MWmed)'
        })
        .reset_index(drop=True)
    )


def load_regions():
    """
    Função principal.
    Carrega o CSV, pré-processa e retorna os 4 dataframes regionais.
    """
    raw = load_raw_load_data()
    base = preprocess_load_data(raw)

    df_sul      = filtrar_regiao(base, 'S')
    df_sudeste  = filtrar_regiao(base, 'SE')
    df_norte    = filtrar_regiao(base, 'N')
    df_nordeste = filtrar_regiao(base, 'NE')

    return df_sul, df_sudeste, df_norte, df_nordeste


# --- Execução direta (opcional) ---
if __name__ == "__main__":
    df_sul, df_se, df_norte, df_ne = load_regions()
    print(df_sul.head())
