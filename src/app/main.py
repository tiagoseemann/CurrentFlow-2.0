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

# Import ML model
from src.models.anomaly_detector import AnomalyDetector


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
# CUSTOM CSS - PROFESSIONAL STYLING
# ============================================================================

st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main container background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Header Styles */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .sub-header {
        font-size: 1.25rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                    0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
                    0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        font-weight: 600;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 12px 24px;
        font-weight: 500;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f8fafc;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: transparent;
    }

    /* Chart Container */
    .element-container iframe {
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Section Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(148, 163, 184, 0.3) 50%,
            transparent 100%);
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Selectbox & Input Styling */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stDateInput > div > div {
        border-radius: 0.5rem;
        border-color: rgba(148, 163, 184, 0.3);
    }

    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 0.75rem;
        border: none;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 0.5rem;
        font-weight: 500;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #64748b;
        font-size: 0.875rem;
    }

    /* Spacing improvements */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Section headers */
    h3 {
        color: #1e293b;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    h4 {
        color: #334155;
        font-weight: 500;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
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
    # Professional header with gradient
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 0.75rem; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 600;'>⚡ Energy Analytics</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.875rem;'>Professional Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

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

    # Info cards in sidebar
    st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem;'>
            <p style='color: #10b981; margin: 0; font-weight: 500;'>✅ Pipeline Status: Active</p>
        </div>
        <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem;'>
            <p style='color: #e2e8f0; margin: 0; font-size: 0.875rem;'>📅 Updated: 2025-12-03</p>
        </div>
        <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 0.5rem;'>
            <p style='color: #e2e8f0; margin: 0; font-size: 0.875rem;'>🌐 Sources: ONS + INMET (567 stations)</p>
        </div>
    """, unsafe_allow_html=True)


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

st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem 1.5rem; border-radius: 0.75rem; margin-bottom: 1.5rem;'>
        <h3 style='color: white; margin: 0; font-size: 1.25rem; font-weight: 600;'>📊 Key Performance Indicators</h3>
    </div>
""", unsafe_allow_html=True)

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview",
    "🗺️ Regional Analysis",
    "⚠️ Anomalies",
    "🔬 Correlation",
    "🤖 ML Predictions",
    "📥 Export & Reports"
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

    # Temporal Analysis
    st.markdown("---")
    st.markdown("### 📅 Temporal & Seasonal Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Moving Averages (7 & 30 days)")
        fig_ma = charts.create_time_series_with_moving_avg(
            df=df,
            x_col='date',
            y_col='val_cargaenergiamwmed',
            windows=[7, 30],
            title='Energy Load with Moving Averages',
            y_label='Energy Load (MW)'
        )
        st.plotly_chart(fig_ma, use_container_width=True)

    with col2:
        st.markdown("#### Seasonal Patterns")
        fig_seasonal = charts.create_seasonal_analysis(
            df=df,
            date_col='date',
            value_col='val_cargaenergiamwmed',
            title='Energy Load by Season'
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)

    # Monthly heatmap
    st.markdown("#### Monthly Patterns Heatmap")
    fig_heatmap = charts.create_monthly_heatmap(
        df=df,
        date_col='date',
        value_col='val_cargaenergiamwmed',
        title='Average Energy Load by Day and Month'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


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


# TAB 5: ML PREDICTIONS
with tab5:
    st.markdown("### 🤖 Machine Learning Anomaly Detection")

    st.info("""
        This tab uses a **Random Forest classifier** trained to detect anomalies in energy load data.
        The model uses features like load, temperature, day of week, and month to predict anomalies.
    """)

    # Try to load the model
    model_path = Path("data/models/anomaly_detector.pkl")

    if not model_path.exists():
        st.warning("⚠️ ML model not found! Please train the model first.")
        st.code("python scripts/train_model.py", language="bash")
        st.info("After training, refresh this page to see predictions.")
    else:
        # Load model
        @st.cache_resource
        def load_ml_model():
            return AnomalyDetector.load(str(model_path))

        try:
            detector = load_ml_model()
            st.success("✅ Model loaded successfully!")

            # Model info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model Type", "Random Forest")
            with col2:
                st.metric("Features Used", len(detector.feature_names) if detector.feature_names else "N/A")
            with col3:
                st.metric("Status", "Trained" if detector.is_trained else "Not Trained")

            st.markdown("---")

            # Make predictions
            st.markdown("#### 📊 Model Predictions vs Ground Truth")

            # Predict on current data
            predictions = detector.predict(df)
            prediction_proba = detector.predict_proba(df)

            # Add predictions to dataframe
            df_with_pred = df.copy()
            df_with_pred['ml_prediction'] = predictions
            df_with_pred['ml_confidence'] = prediction_proba[:, 1]  # Probability of anomaly

            # Comparison metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "ML Predicted Anomalies",
                    f"{predictions.sum()}"
                )

            with col2:
                st.metric(
                    "Ground Truth Anomalies",
                    f"{df['is_anomaly'].sum()}"
                )

            with col3:
                agreement = (predictions == df['is_anomaly']).mean()
                st.metric(
                    "Agreement Rate",
                    f"{agreement:.1%}"
                )

            with col4:
                avg_confidence = prediction_proba[predictions == 1, 1].mean() if predictions.sum() > 0 else 0
                st.metric(
                    "Avg Confidence",
                    f"{avg_confidence:.1%}"
                )

            # Feature importance
            st.markdown("---")
            st.markdown("#### 🎯 Feature Importance")

            importance_df = detector.get_feature_importance()

            # Create bar chart for feature importance
            import plotly.graph_objects as go

            fig_importance = go.Figure(data=[
                go.Bar(
                    x=importance_df['importance'],
                    y=importance_df['feature'],
                    orientation='h',
                    marker_color='rgba(102, 126, 234, 0.8)',
                    text=importance_df['importance'].round(3),
                    textposition='auto',
                )
            ])

            fig_importance.update_layout(
                title="Random Forest Feature Importance",
                xaxis_title="Importance Score",
                yaxis_title="Feature",
                height=400,
                template='plotly_white',
                showlegend=False
            )

            st.plotly_chart(fig_importance, use_container_width=True)

            # Prediction details
            st.markdown("---")
            st.markdown("#### 🔍 Prediction Details")

            # Show predictions where model disagrees with ground truth
            disagreements = df_with_pred[
                df_with_pred['ml_prediction'] != df_with_pred['is_anomaly']
            ]

            if len(disagreements) > 0:
                st.warning(f"⚠️ Found {len(disagreements)} cases where ML prediction differs from ground truth")

                disagreements_display = disagreements[[
                    'date', 'region', 'val_cargaenergiamwmed', 'temp_mean',
                    'is_anomaly', 'ml_prediction', 'ml_confidence'
                ]].copy()

                disagreements_display.columns = [
                    'Date', 'Region', 'Load (MW)', 'Temp (°C)',
                    'Ground Truth', 'ML Prediction', 'Confidence'
                ]

                st.dataframe(disagreements_display, use_container_width=True, hide_index=True)
            else:
                st.success("✅ Perfect agreement between ML predictions and ground truth!")

            # Show top ML predictions by confidence
            st.markdown("---")
            st.markdown("#### 🎯 Top ML Anomaly Predictions (by confidence)")

            ml_anomalies = df_with_pred[df_with_pred['ml_prediction'] == 1].nlargest(
                10, 'ml_confidence'
            )[['date', 'region', 'val_cargaenergiamwmed', 'temp_mean', 'ml_confidence', 'is_anomaly']]

            ml_anomalies.columns = ['Date', 'Region', 'Load (MW)', 'Temp (°C)', 'Confidence', 'Ground Truth']

            st.dataframe(ml_anomalies, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.info("Try retraining the model: `python scripts/train_model.py`")


# TAB 6: EXPORT & REPORTS
with tab6:
    st.markdown("### 📥 Export Data & Generate Reports")

    st.info("""
        Export your filtered data and generate reports in multiple formats.
        The exports include all visualizations and statistics from the current view.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Export Data")

        # Select columns to export
        export_cols = st.multiselect(
            "Select columns to export",
            options=df.columns.tolist(),
            default=['date', 'region', 'val_cargaenergiamwmed', 'temp_mean', 'is_anomaly']
        )

        if export_cols:
            export_df = df[export_cols].copy()

            # CSV Export
            csv = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"energy_data_{selected_year}_{selected_region}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Excel Export
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                export_df.to_excel(writer, sheet_name='Data', index=False)

                # Add summary sheet
                summary_df = pd.DataFrame({
                    'Metric': ['Total Records', 'Date Range', 'Regions', 'Avg Load (MW)', 'Anomalies'],
                    'Value': [
                        len(export_df),
                        f"{export_df['date'].min()} to {export_df['date'].max()}" if 'date' in export_df else 'N/A',
                        export_df['region'].nunique() if 'region' in export_df else 'N/A',
                        f"{export_df['val_cargaenergiamwmed'].mean():.2f}" if 'val_cargaenergiamwmed' in export_df else 'N/A',
                        export_df['is_anomaly'].sum() if 'is_anomaly' in export_df else 'N/A'
                    ]
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)

            excel_data = buffer.getvalue()
            st.download_button(
                label="📊 Download as Excel",
                data=excel_data,
                file_name=f"energy_data_{selected_year}_{selected_region}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            # JSON Export
            json_data = export_df.to_json(orient='records', date_format='iso').encode('utf-8')
            st.download_button(
                label="🔗 Download as JSON",
                data=json_data,
                file_name=f"energy_data_{selected_year}_{selected_region}.json",
                mime="application/json",
                use_container_width=True
            )

            st.success(f"✅ Ready to export {len(export_df)} records with {len(export_cols)} columns")

    with col2:
        st.markdown("#### 📈 Generate Report")

        st.markdown("""
        Generate a comprehensive PDF report including:
        - Executive summary with KPIs
        - All visualizations
        - Statistical analysis
        - Anomaly detection results
        - Regional comparisons
        """)

        report_format = st.selectbox(
            "Report Format",
            options=["PDF (Recommended)", "HTML", "Markdown"],
            help="Choose the format for your report"
        )

        include_sections = st.multiselect(
            "Include sections",
            options=[
                "Executive Summary",
                "Overview Charts",
                "Regional Analysis",
                "Anomaly Detection",
                "Correlation Analysis",
                "ML Predictions"
            ],
            default=[
                "Executive Summary",
                "Overview Charts",
                "Regional Analysis"
            ]
        )

        if st.button("🎯 Generate Report", use_container_width=True, type="primary"):
            with st.spinner("Generating report..."):
                # Generate markdown report
                report_md = f"""# Energy Analytics Report
## Period: {selected_year} | Region: {selected_region}

---

### 📊 Executive Summary

**Key Metrics:**
- Total Records: {len(df):,}
- Date Range: {df['date'].min()} to {df['date'].max()}
- Average Energy Load: {df['val_cargaenergiamwmed'].mean():,.0f} MW
- Average Temperature: {df['temp_mean'].mean():.1f}°C
- Anomalies Detected: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.2f}%)

---

### 📈 Statistical Summary

#### Energy Load (MW)
- Mean: {df['val_cargaenergiamwmed'].mean():,.1f}
- Median: {df['val_cargaenergiamwmed'].median():,.1f}
- Std Dev: {df['val_cargaenergiamwmed'].std():,.1f}
- Min: {df['val_cargaenergiamwmed'].min():,.1f}
- Max: {df['val_cargaenergiamwmed'].max():,.1f}

#### Temperature (°C)
- Mean: {df['temp_mean'].mean():.2f}
- Median: {df['temp_mean'].median():.2f}
- Std Dev: {df['temp_mean'].std():.2f}
- Min: {df['temp_min'].min():.2f}
- Max: {df['temp_max'].max():.2f}

---

### 🗺️ Regional Analysis

"""
                # Add regional stats
                for region in df['region'].unique():
                    region_df = df[df['region'] == region]
                    report_md += f"""
#### {region}
- Records: {len(region_df):,}
- Avg Load: {region_df['val_cargaenergiamwmed'].mean():,.0f} MW
- Avg Temp: {region_df['temp_mean'].mean():.1f}°C
- Anomalies: {region_df['is_anomaly'].sum()}
"""

                report_md += f"""

---

### ⚠️ Anomaly Detection

**Total Anomalies:** {df['is_anomaly'].sum()}

**Anomaly Rate:** {df['is_anomaly'].mean()*100:.2f}%

**Detection Method:** Z-score (threshold: ±2.5σ)

---

*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Tool: Energy Analytics Dashboard v2.0*
"""

                # Display preview
                with st.expander("📄 Report Preview", expanded=True):
                    st.markdown(report_md)

                # Download buttons
                st.markdown("---")
                col_a, col_b = st.columns(2)

                with col_a:
                    # Markdown download
                    st.download_button(
                        label="📝 Download Markdown",
                        data=report_md.encode('utf-8'),
                        file_name=f"energy_report_{selected_year}_{selected_region}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                with col_b:
                    # HTML download
                    html_report = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Energy Analytics Report</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            h1 {{ color: #667eea; }}
                            h2 {{ color: #764ba2; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
                            h3 {{ color: #3498db; }}
                            h4 {{ color: #555; }}
                            hr {{ border: none; height: 2px; background: linear-gradient(90deg, transparent, #667eea, transparent); }}
                            .metric {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                        </style>
                    </head>
                    <body>
                        {report_md.replace('### ', '<h3>').replace('## ', '<h2>').replace('# ', '<h1>').replace('---', '<hr>').replace('**', '<strong>').replace('*', '</strong>')}
                    </body>
                    </html>
                    """
                    st.download_button(
                        label="🌐 Download HTML",
                        data=html_report.encode('utf-8'),
                        file_name=f"energy_report_{selected_year}_{selected_region}.html",
                        mime="text/html",
                        use_container_width=True
                    )

    # Data Preview
    st.markdown("---")
    st.markdown("### 👁️ Data Preview")

    preview_rows = st.slider("Number of rows to preview", min_value=5, max_value=100, value=10)
    st.dataframe(df.head(preview_rows), use_container_width=True)

    # Dataset info
    st.markdown("---")
    st.markdown("### ℹ️ Dataset Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    with col2:
        st.metric("Total Columns", f"{df.shape[1]}")
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    with col4:
        st.metric("Missing Values", f"{df.isnull().sum().sum()}")


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
    <div class='footer'>
        <div style='background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
            <p style='font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;'>⚡ Energy Analytics Dashboard v2.0</p>
            <p style='color: #64748b; margin: 0.25rem 0;'>
                <span style='color: #667eea; font-weight: 500;'>567 Weather Stations</span> •
                <span style='color: #764ba2; font-weight: 500;'>4 Regions</span> •
                <span style='color: #10b981; font-weight: 500;'>Real-time Analytics</span>
            </p>
            <p style='color: #94a3b8; font-size: 0.875rem; margin-top: 0.75rem;'>
                Powered by Streamlit • Plotly • Python
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
