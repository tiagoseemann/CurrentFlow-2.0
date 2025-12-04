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
# CARREGAMENTO DE DADOS (Pipeline Robusto - Multi-Ano)
# ============================================================================

@st.cache_data(ttl=3600)
def load_processed_data_single_year(year: int) -> pd.DataFrame:
    """
    Carrega dados processados de um único ano.
    """
    cache_path = Path(f"data/processed/energy_weather_{year}.parquet")

    if cache_path.exists():
        return pd.read_parquet(cache_path)

    # Se não existe cache, roda pipeline
    st.info(f"⏳ Processando dados de {year}...")
    try:
        ons_loader = ONSLoader()
        inmet_loader = INMETLoader()
        preprocessor = Preprocessor()

        ons_df = ons_loader.load(year)
        inmet_df = inmet_loader.load(year)
        df = preprocessor.process(ons_df, inmet_df, save=False)

        # Salva com nome específico do ano
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_path)
        st.success(f"✅ Dados de {year} processados com sucesso!")

        return df
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar dados de {year}: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_processed_data_multi_year(years: list) -> pd.DataFrame:
    """
    Carrega dados processados de múltiplos anos.
    """
    dfs = []
    for year in years:
        df_year = load_processed_data_single_year(year)
        if not df_year.empty:
            dfs.append(df_year)

    if dfs:
        df_combined = pd.concat(dfs, ignore_index=True)
        df_combined = df_combined.sort_values('date').reset_index(drop=True)
        return df_combined
    else:
        # Fallback para 2023 se nenhum ano foi carregado
        cache_path = Path("data/processed/energy_weather_processed.parquet")
        if cache_path.exists():
            return pd.read_parquet(cache_path)
        return pd.DataFrame()


# Anos disponíveis para seleção
AVAILABLE_YEARS = [2021, 2022, 2023, 2024]


# ============================================================================
# INTERFACE PRINCIPAL (Estrutura do App Original)
# ============================================================================

st.title("⚡ Dashboard de Análise Energética")

# ============================================================================
# SIDEBAR COM SELETOR DE ANO E MÉTRICAS
# ============================================================================

with st.sidebar:
    st.markdown("### 📅 Seleção de Período")

    # Seletor de ano
    year_option = st.selectbox(
        "Selecione o(s) ano(s)",
        ["2023 (atual)", "2022", "2021", "2024", "Todos os anos (2021-2024)"],
        help="Escolha um ano específico ou todos os anos disponíveis"
    )

    # Mapeia opção para anos
    if "Todos" in year_option:
        selected_years = AVAILABLE_YEARS
        st.caption(f"📊 Carregando {len(selected_years)} anos de dados")
    elif "2023" in year_option:
        selected_years = [2023]
    elif "2022" in year_option:
        selected_years = [2022]
    elif "2021" in year_option:
        selected_years = [2021]
    elif "2024" in year_option:
        selected_years = [2024]

    # Carrega dados baseado na seleção
    with st.spinner(f"Carregando dados de {len(selected_years)} ano(s)..."):
        if len(selected_years) == 1:
            df = load_processed_data_single_year(selected_years[0])
        else:
            df = load_processed_data_multi_year(selected_years)

    # Verifica se dados foram carregados
    if df.empty:
        st.error("❌ Nenhum dado disponível. Usando dados de 2023 como fallback.")
        df = load_processed_data_single_year(2023)

# Prepara dicionário de regiões (como no app original)
REGIONS = {
    "Todas as Regiões": df,
    "Sul": df[df['region'] == 'Sul'],
    "Sudeste/Centro-Oeste": df[df['region'] == 'Sudeste/Centro-Oeste'],
    "Nordeste": df[df['region'] == 'Nordeste'],
    "Norte": df[df['region'] == 'Norte']
}

# ============================================================================
# SIDEBAR - MÉTRICAS E INFORMAÇÕES
# ============================================================================

with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Resumo dos Dados")

    # Métricas gerais
    total_registros = len(df)
    periodo_inicio = df['date'].min().strftime('%d/%m/%Y')
    periodo_fim = df['date'].max().strftime('%d/%m/%Y')

    st.metric("Total de Registros", f"{total_registros:,}")
    st.metric("Período", f"{periodo_inicio}")
    st.caption(f"até {periodo_fim}")

    # Anomalias
    if 'is_anomaly' in df.columns:
        total_anomalias = df['is_anomaly'].sum()
        taxa_anomalias = (total_anomalias / len(df)) * 100
        st.metric(
            "Anomalias Detectadas",
            f"{total_anomalias}",
            delta=f"{taxa_anomalias:.2f}% dos dados",
            delta_color="inverse"
        )

    # Carga média por região
    st.markdown("---")
    st.markdown("### ⚡ Carga Média por Região")
    for region_name, region_df in REGIONS.items():
        if region_name != "Todas as Regiões" and len(region_df) > 0:
            media_carga = region_df['val_cargaenergiamwmed'].mean()
            st.caption(f"{region_name}: **{media_carga:,.0f} MW**")

    # Info adicional
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.caption(f"**Features:** {len(df.columns)} disponíveis")
    st.caption(f"**Regiões:** {len(REGIONS) - 1} + Todas")
    st.caption(f"**Análises:** 9 tipos")

    # Footer
    st.markdown("---")
    st.caption("v2.5.1 | Dashboard Profissional")

# ============================================================================
# FILTROS E NAVEGAÇÃO
# ============================================================================

# Selectbox de região (como no app original)
regiao = st.selectbox("🗺️ Região", list(REGIONS.keys()))
df_filtrado = REGIONS[regiao]

# Filtro temporal interativo (opcional)
col1, col2 = st.columns([2, 1])

with col1:
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

with col2:
    # Toggle para filtro temporal
    usar_filtro = st.checkbox("🗓️ Filtrar período", value=False, help="Ative para filtrar dados por período específico")

# Aplicar filtro temporal se ativado
if usar_filtro:
    df_filtrado['date'] = pd.to_datetime(df_filtrado['date'])
    data_min = df_filtrado['date'].min().date()
    data_max = df_filtrado['date'].max().date()

    col_data1, col_data2 = st.columns(2)
    with col_data1:
        data_inicio = st.date_input(
            "Data Início",
            value=data_min,
            min_value=data_min,
            max_value=data_max,
            help="Selecione a data inicial do período"
        )
    with col_data2:
        data_fim = st.date_input(
            "Data Fim",
            value=data_max,
            min_value=data_min,
            max_value=data_max,
            help="Selecione a data final do período"
        )

    # Aplicar filtro
    df_filtrado = df_filtrado[
        (df_filtrado['date'].dt.date >= data_inicio) &
        (df_filtrado['date'].dt.date <= data_fim)
    ]

    # Mostrar info sobre filtro aplicado
    st.info(f"📅 Filtro ativo: {len(df_filtrado):,} registros entre {data_inicio.strftime('%d/%m/%Y')} e {data_fim.strftime('%d/%m/%Y')}")

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
