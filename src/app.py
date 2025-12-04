"""
Dashboard de Análise Energética do Brasil

Baseado na estrutura original do app.py da branch cadona,
mas utilizando o pipeline robusto e funcionalidades avançadas.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import pipeline robusto
from src.data.loaders import ONSLoader, INMETLoader
from src.data.preprocessor import Preprocessor

# Import funções do dashboard
import src.dashboard as dashboard

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Energy Analytics Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Profissional (mantém estética do v2)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }

    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #e2e8f0 !important;
    }

    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# CARREGAMENTO DE DADOS (Pipeline Robusto)
# ============================================================================

@st.cache_data(ttl=3600)
def load_processed_data(year: int = 2023) -> pd.DataFrame:
    """
    Carrega dados processados usando o pipeline robusto.
    Similar ao app original mas com melhor arquitetura.
    """
    cache_path = Path("data/processed/energy_weather_processed.parquet")

    if cache_path.exists():
        return pd.read_parquet(cache_path)

    # Se não existe cache, roda pipeline
    st.info("Processando dados pela primeira vez...")
    ons_loader = ONSLoader()
    inmet_loader = INMETLoader()
    preprocessor = Preprocessor()

    ons_df = ons_loader.load(year)
    inmet_df = inmet_loader.load(year)
    df = preprocessor.process(ons_df, inmet_df, save=True)

    return df


# Carrega dados
df = load_processed_data(2023)

# Prepara dicionário de regiões (como no app original)
REGIONS = {
    "Todas as Regiões": df,
    "Sul": df[df['region'] == 'Sul'],
    "Sudeste/Centro-Oeste": df[df['region'] == 'Sudeste/Centro-Oeste'],
    "Nordeste": df[df['region'] == 'Nordeste'],
    "Norte": df[df['region'] == 'Norte']
}


# ============================================================================
# INTERFACE PRINCIPAL (Estrutura do App Original)
# ============================================================================

st.title("⚡ Dashboard de Análise Energética")

# Selectbox de região (como no app original)
regiao = st.selectbox("🗺️ Região", list(REGIONS.keys()))
df_filtrado = REGIONS[regiao]

# Selectbox de tipo de análise (expandido do original)
tipo = st.selectbox(
    "📊 Escolha o tipo de análise",
    [
        "Overview & KPIs",
        "Correlação",
        "Scatter",
        "Série temporal",
        "Comparar regiões",
        "Análise Temporal & Sazonal",
        "Anomalias",
        "ML Predictions",
        "Export & Reports"
    ]
)

st.markdown("---")

# ============================================================================
# RENDERIZAÇÃO (Baseado na estrutura original)
# ============================================================================

# Mantém a estrutura if/elif do app original
if tipo == "Overview & KPIs":
    dashboard.overview(df_filtrado)

elif tipo == "Correlação":
    dashboard.correlacao(df_filtrado)

elif tipo == "Scatter":
    dashboard.scatter(df_filtrado)

elif tipo == "Série temporal":
    dashboard.serie(df_filtrado)

elif tipo == "Comparar regiões":
    dashboard.comparar(df_filtrado, df)

elif tipo == "Análise Temporal & Sazonal":
    dashboard.temporal(df_filtrado)

elif tipo == "Anomalias":
    dashboard.anomalias(df_filtrado)

elif tipo == "ML Predictions":
    dashboard.ml_predictions(df_filtrado)

elif tipo == "Export & Reports":
    dashboard.export_reports(df_filtrado, regiao)
