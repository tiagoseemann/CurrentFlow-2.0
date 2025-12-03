import streamlit as st
import pandas as pd
import dashboard

from merge_datasets import df_sul, df_sudeste, df_nordeste, df_norte

REGIONS = {
    "Sul": df_sul,
    "Sudeste": df_sudeste,
    "Nordeste": df_nordeste,
    "Norte": df_norte
}

all_df = pd.concat(REGIONS.values(), ignore_index=True)

st.title("Dashboard - Current Flow")

regiao = st.selectbox("Região", REGIONS.keys())
df = REGIONS[regiao]

tipo = st.selectbox(
    "Escolha",
    ["Correlação", "Scatter", "Série temporal", "Comparar regiões"]
)

if tipo == "Correlação":
    dashboard.correlacao(df)

elif tipo == "Scatter":
    dashboard.scatter(df)

elif tipo == "Série temporal":
    dashboard.serie(df)

elif tipo == "Comparar regiões":
    dashboard.comparar(df, all_df)
