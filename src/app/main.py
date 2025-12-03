"""
⚡ Energy Analytics Dashboard - Professional Version

This is the main entry point for the Streamlit dashboard.
It uses the robust data pipeline (ONSLoader, INMETLoader, Preprocessor)
and provides professional visualizations for energy analytics.

Run with:
    streamlit run src/app/main.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import pipeline components
from src.data.loaders import ONSLoader, INMETLoader
from src.data.preprocessor import Preprocessor

# Import dashboard components
from src.app.components import metrics, charts


# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Energy Analytics Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING (with caching)
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_processed_data(year: int = 2023) -> pd.DataFrame:
    """
    Load and process data using the robust pipeline.

    This function leverages the production-ready ONSLoader, INMETLoader,
    and Preprocessor to provide clean, feature-engineered data.

    Args:
        year: Year to load (default 2023)

    Returns:
        Processed DataFrame with 19 features
    """
    # Try to load from cached Parquet first
    cache_path = Path("data/processed/energy_weather_processed.parquet")

    if cache_path.exists():
        st.info("📦 Loading from cache (Parquet)...")
        df = pd.read_parquet(cache_path)
        return df

    # If no cache, run full pipeline
    st.info("🔄 Running data pipeline... This may take a few minutes.")

    with st.spinner("Loading ONS energy data..."):
        ons_loader = ONSLoader()
        ons_df = ons_loader.load(year)

    with st.spinner("Loading INMET weather data (567 stations)..."):
        inmet_loader = INMETLoader()
        inmet_df = inmet_loader.load(year)

    with st.spinner("Processing and merging data..."):
        preprocessor = Preprocessor()
        df = preprocessor.process(ons_df, inmet_df, save=True)

    st.success("✅ Data loaded successfully!")
    return df


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/white?text=Energy+Analytics",
             use_container_width=True)

    st.markdown("---")

    st.markdown("### ⚙️ Configuration")

    # Year selection
    selected_year = st.selectbox(
        "📅 Select Year",
        options=[2023, 2024],
        index=0,
        help="Choose the year for data analysis"
    )

    # Region filter
    st.markdown("### 🗺️ Region Filter")
    all_regions = ['All', 'Norte', 'Nordeste', 'Sudeste/Centro-Oeste', 'Sul']
    selected_region = st.selectbox(
        "Select Region",
        options=all_regions,
        index=0
    )

    # Date range filter
    st.markdown("### 📆 Date Range")
    use_date_filter = st.checkbox("Enable date filter", value=False)

    st.markdown("---")
    st.markdown("### 📊 Data Info")
    st.caption("Pipeline Status: ✅ Active")
    st.caption("Last Updated: 2025-12-03")
    st.caption("Data Sources: ONS + INMET")


# ============================================================================
# LOAD DATA
# ============================================================================

# Load data with progress indicator
df = load_processed_data(selected_year)

# Apply filters
if selected_region != 'All':
    df = df[df['region'] == selected_region]

if use_date_filter:
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date()
    )
    if len(date_range) == 2:
        df = df[(df['date'] >= pd.Timestamp(date_range[0])) &
                (df['date'] <= pd.Timestamp(date_range[1]))]


# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header
st.markdown('<h1 class="main-header">⚡ Energy Analytics Dashboard</h1>',
            unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">Analyzing {len(df):,} records from {selected_year}</p>',
            unsafe_allow_html=True)

st.markdown("---")


# ============================================================================
# KPI ROW
# ============================================================================

st.markdown("### 📊 Key Performance Indicators")

kpi_metrics = [
    {
        'label': 'Avg Energy Load',
        'value': df['val_cargaenergiamwmed'].mean(),
        'format': '{:,.0f} MW',
        'help': 'Average energy load across all regions and dates'
    },
    {
        'label': 'Avg Temperature',
        'value': df['temp_mean'].mean(),
        'format': '{:.1f} °C',
        'help': 'Average temperature across all regions'
    },
    {
        'label': 'Anomalies Detected',
        'value': df['is_anomaly'].sum(),
        'format': '{:.0f}',
        'help': 'Number of anomalies detected (Z-score > 2.5)'
    },
    {
        'label': 'Anomaly Rate',
        'value': df['is_anomaly'].mean() * 100,
        'format': '{:.2f} %',
        'help': 'Percentage of records flagged as anomalies'
    }
]

metrics.display_kpi_row(kpi_metrics)

st.markdown("---")


# ============================================================================
# MAIN VISUALIZATIONS
# ============================================================================

# Tab-based navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "🗺️ Regional Analysis",
    "⚠️ Anomalies",
    "🔬 Correlation"
])

# TAB 1: OVERVIEW
with tab1:
    st.markdown("### Energy Load vs Temperature Over Time")

    # Dual-axis chart
    fig_dual = charts.create_dual_axis_chart(
        df=df,
        x_col='date',
        y1_col='val_cargaenergiamwmed',
        y2_col='temp_mean',
        y1_label='Energy Load (MW)',
        y2_label='Temperature (°C)',
        title='Energy Load and Temperature Trends'
    )
    st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("### Energy Load with Confidence Bands")

    # Time series with bands
    fig_bands = charts.create_time_series_with_bands(
        df=df,
        x_col='date',
        y_col='val_cargaenergiamwmed',
        title='Energy Load with ±1σ and ±2σ Confidence Bands',
        y_label='Energy Load (MW)'
    )
    st.plotly_chart(fig_bands, use_container_width=True)

    # Statistics summary
    metrics.display_stat_summary(
        title="Energy Load Statistics",
        mean=df['val_cargaenergiamwmed'].mean(),
        median=df['val_cargaenergiamwmed'].median(),
        std=df['val_cargaenergiamwmed'].std(),
        min_val=df['val_cargaenergiamwmed'].min(),
        max_val=df['val_cargaenergiamwmed'].max(),
        unit="MW"
    )


# TAB 2: REGIONAL ANALYSIS
with tab2:
    st.markdown("### Regional Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Average Energy Load by Region")
        fig_regional_bar = charts.create_regional_comparison(
            df=df,
            region_col='region',
            value_col='val_cargaenergiamwmed',
            title='Average Energy Load by Region',
            chart_type='bar'
        )
        st.plotly_chart(fig_regional_bar, use_container_width=True)

    with col2:
        st.markdown("#### Energy Load Distribution by Region")
        fig_regional_box = charts.create_regional_comparison(
            df=df,
            region_col='region',
            value_col='val_cargaenergiamwmed',
            title='Energy Load Distribution',
            chart_type='box'
        )
        st.plotly_chart(fig_regional_box, use_container_width=True)

    # Regional statistics table
    st.markdown("#### Regional Statistics Summary")
    regional_stats = df.groupby('region').agg({
        'val_cargaenergiamwmed': ['mean', 'std', 'min', 'max'],
        'temp_mean': ['mean', 'std'],
        'is_anomaly': 'sum'
    }).round(2)
    regional_stats.columns = ['Load Mean (MW)', 'Load Std', 'Load Min', 'Load Max',
                               'Temp Mean (°C)', 'Temp Std', 'Anomalies']
    st.dataframe(regional_stats, use_container_width=True)


# TAB 3: ANOMALIES
with tab3:
    st.markdown("### Anomaly Detection Results")

    # Anomaly scatter plot
    if 'load_zscore' in df.columns:
        fig_anomaly = charts.create_anomaly_scatter(
            df=df,
            x_col='date',
            y_col='load_zscore',
            anomaly_col='is_anomaly',
            title='Anomaly Detection (Z-score Method)'
        )
        st.plotly_chart(fig_anomaly, use_container_width=True)

    # Anomaly table
    st.markdown("#### Top 10 Anomalies")
    if 'load_zscore' in df.columns:
        anomalies_df = df[df['is_anomaly'] == 1].nlargest(10, 'load_zscore')[
            ['date', 'region', 'val_cargaenergiamwmed', 'temp_mean', 'load_zscore']
        ]
        anomalies_df.columns = ['Date', 'Region', 'Load (MW)', 'Temp (°C)', 'Z-Score']
        st.dataframe(anomalies_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Z-score column not found in data.")


# TAB 4: CORRELATION
with tab4:
    st.markdown("### Correlation Analysis")

    # Select columns for correlation
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    selected_cols = st.multiselect(
        "Select variables for correlation analysis",
        options=numeric_cols,
        default=['val_cargaenergiamwmed', 'temp_mean', 'temp_min', 'temp_max',
                'radiation_mean', 'precipitation_total'][:min(6, len(numeric_cols))]
    )

    if len(selected_cols) >= 2:
        fig_corr = charts.create_correlation_heatmap(
            df=df,
            columns=selected_cols,
            title='Correlation Matrix'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Please select at least 2 variables for correlation analysis.")

    # Correlation insights
    if len(selected_cols) >= 2:
        st.markdown("#### Key Correlations")
        corr_matrix = df[selected_cols].corr()

        # Find top 5 correlations (excluding diagonal)
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })

        corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation',
                                                       key=abs,
                                                       ascending=False).head(5)
        st.dataframe(corr_df, use_container_width=True, hide_index=True)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>⚡ Energy Analytics Dashboard v2.0 |
        Data Sources: ONS + INMET (567 stations) |
        Powered by Streamlit & Plotly</p>
    </div>
""", unsafe_allow_html=True)
