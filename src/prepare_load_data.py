import numpy as np
import pandas as pd
from pathlib import Path

# Path
data_path = Path(r'C:\Users\guica\OneDrive\Documentos\GitHub\CurrentFlow-2.0\data\raw\CARGA_ENERGIA_2024.csv')

# Leitura
raw_data = pd.read_csv(data_path, sep=';')

# Selecting data and converting the type
df = raw_data[['din_instante', 'id_subsistema', 'val_cargaenergiamwmed']].copy()
df['din_instante'] = pd.to_datetime(df['din_instante'])

# Organizing by regions
def filtrar_regiao(df, codigo):
    return (
        df[df['id_subsistema'] == codigo]
        .rename(columns={
            'din_instante': 'data',
            'id_subsistema': 'regiao',
            'val_cargaenergiamwmed': 'carga(MWmed)'
        })
        .reset_index(drop=True)
    )

# Aplicações
df_sul      = filtrar_regiao(df, 'S')
df_sudeste  = filtrar_regiao(df, 'SE')
df_norte    = filtrar_regiao(df, 'N')
df_nordeste = filtrar_regiao(df, 'NE')

print(df_sul)
