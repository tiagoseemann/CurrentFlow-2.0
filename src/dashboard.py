"""
Funções de visualização do dashboard.

Baseado no dashboard.py original da branch cadona,
expandido com funcionalidades profissionais.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from io import BytesIO

# Import components profissionais
from src.app.components import charts, metrics

# Import ML model
try:
    from src.models.anomaly_detector import AnomalyDetector
except ImportError:
    AnomalyDetector = None


# ============================================================================
# FUNÇÕES ORIGINAIS (Mantidas intactas da branch cadona)
# ============================================================================

def correlacao(df):
    """
    Exibe a matriz de correlação apenas das colunas numéricas.
    Útil para ver relações lineares entre temperatura, precipitação e carga.
    """
    st.subheader("Correlação")

    # Seleciona somente colunas numéricas para evitar strings na matriz
    num_df = df.select_dtypes(include="number")

    # Exibe a matriz diretamente
    st.dataframe(num_df.corr())

    # NOVO: Adiciona heatmap visual
    st.markdown("### Heatmap de Correlação")
    if len(num_df.columns) >= 2:
        fig_corr = charts.create_correlation_heatmap(
            df=df,
            columns=num_df.columns[:min(10, len(num_df.columns))].tolist(),
            title='Matriz de Correlação Interativa'
        )
        st.plotly_chart(fig_corr, use_container_width=True)


def scatter(df):
    """
    Gera um gráfico de dispersão entre duas variáveis numéricas.
    Serve para verificar relação visual entre pares (ex: temperatura vs carga).
    """
    st.subheader("Dispersão entre variáveis")

    # Pega apenas colunas numéricas para o menu
    cols = df.select_dtypes(include="number").columns

    # Usuário escolhe eixo X e Y
    x = st.selectbox("X", cols)
    y = st.selectbox("Y", cols)

    # Plota o gráfico
    fig = px.scatter(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)


def serie(df):
    """
    Plota uma série temporal usando 'date' no eixo X
    e qualquer variável numérica no eixo Y.
    """
    st.subheader("Série temporal")

    # Somente colunas numéricas podem ser escolhidas para o Y
    cols = df.select_dtypes(include="number").columns
    y = st.selectbox("Variável", cols)

    # Plota a série temporal
    # Tenta usar 'date' primeiro, se não existir usa 'data'
    date_col = 'date' if 'date' in df.columns else 'data'
    fig = px.line(df, x=date_col, y=y, markers=True)
    st.plotly_chart(fig, use_container_width=True)


def comparar(df, all_df):
    """
    Compara a média de uma variável entre todas as regiões.
    Útil para ver diferenças estruturais regionais.
    """
    st.subheader("Comparar regiões")

    # Variáveis numéricas possíveis
    cols = df.select_dtypes(include="number").columns
    var = st.selectbox("Variável", cols)

    # Tenta usar 'region' primeiro, se não existir usa 'regiao'
    region_col = 'region' if 'region' in all_df.columns else 'regiao'

    # Calcula média da variável selecionada por região
    mean_df = all_df.groupby(region_col)[var].mean().reset_index()

    # Plota comparação por barras
    fig = px.bar(mean_df, x=region_col, y=var)
    st.plotly_chart(fig, use_container_width=True)

    # NOVO: Adiciona box plot para ver distribuição
    st.markdown("### Distribuição por Região")
    if region_col in all_df.columns and var in all_df.columns:
        fig_regional = charts.create_regional_comparison(
            df=all_df,
            region_col=region_col,
            value_col=var,
            title=f'Distribuição de {var} por Região',
            chart_type='box'
        )
        st.plotly_chart(fig_regional, use_container_width=True)


# ============================================================================
# NOVAS FUNÇÕES (Funcionalidades avançadas)
# ============================================================================

def overview(df):
    """
    Visão geral com KPIs e gráficos principais.
    """
    st.subheader("📊 Overview & KPIs")

    # KPI Cards
    kpi_metrics = [
        {
            'label': 'Média de Carga',
            'value': df['val_cargaenergiamwmed'].mean(),
            'format': '{:,.0f} MW',
            'help': 'Carga energética média do período'
        },
        {
            'label': 'Temperatura Média',
            'value': df['temp_mean'].mean(),
            'format': '{:.1f} °C',
            'help': 'Temperatura média do período'
        },
        {
            'label': 'Anomalias',
            'value': df['is_anomaly'].sum() if 'is_anomaly' in df.columns else 0,
            'format': '{:.0f}',
            'help': 'Número de anomalias detectadas'
        },
        {
            'label': 'Registros',
            'value': len(df),
            'format': '{:,.0f}',
            'help': 'Total de registros no período'
        }
    ]

    metrics.display_kpi_row(kpi_metrics)

    st.markdown("---")

    # Gráfico dual-axis
    st.markdown("### Carga vs Temperatura")
    if 'date' in df.columns:
        fig_dual = charts.create_dual_axis_chart(
            df=df,
            x_col='date',
            y1_col='val_cargaenergiamwmed',
            y2_col='temp_mean',
            y1_label='Carga (MW)',
            y2_label='Temperatura (°C)',
            title='Evolução de Carga e Temperatura'
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    # Bandas de confiança
    st.markdown("### Carga com Bandas de Confiança")
    if 'date' in df.columns:
        fig_bands = charts.create_time_series_with_bands(
            df=df,
            x_col='date',
            y_col='val_cargaenergiamwmed',
            title='Carga Energética com ±1σ e ±2σ',
            y_label='Carga (MW)'
        )
        st.plotly_chart(fig_bands, use_container_width=True)


def temporal(df):
    """
    Análise temporal e sazonal.
    """
    st.subheader("📅 Análise Temporal & Sazonal")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Médias Móveis")
        if 'date' in df.columns:
            fig_ma = charts.create_time_series_with_moving_avg(
                df=df,
                x_col='date',
                y_col='val_cargaenergiamwmed',
                windows=[7, 30],
                title='Carga com Médias Móveis (7 e 30 dias)',
                y_label='Carga (MW)'
            )
            st.plotly_chart(fig_ma, use_container_width=True)

    with col2:
        st.markdown("#### Padrões Sazonais")
        if 'date' in df.columns:
            fig_seasonal = charts.create_seasonal_analysis(
                df=df,
                date_col='date',
                value_col='val_cargaenergiamwmed',
                title='Carga por Estação do Ano'
            )
            st.plotly_chart(fig_seasonal, use_container_width=True)

    # Heatmap mensal
    st.markdown("---")
    st.markdown("#### Heatmap Mensal")
    if 'date' in df.columns:
        fig_heatmap = charts.create_monthly_heatmap(
            df=df,
            date_col='date',
            value_col='val_cargaenergiamwmed',
            title='Padrão de Carga por Dia e Mês'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)


def anomalias(df):
    """
    Análise de anomalias detectadas.
    """
    st.subheader("⚠️ Detecção de Anomalias")

    if 'is_anomaly' not in df.columns:
        st.warning("Esta base de dados não possui detecção de anomalias.")
        st.info("Execute o preprocessor para gerar as features de anomalias.")
        return

    # Métricas de anomalias
    total_anomalias = df['is_anomaly'].sum()
    taxa_anomalias = df['is_anomaly'].mean() * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Anomalias", f"{total_anomalias}")
    with col2:
        st.metric("Taxa de Anomalia", f"{taxa_anomalias:.2f}%")
    with col3:
        st.metric("Registros Normais", f"{len(df) - total_anomalias}")

    st.markdown("---")

    # Gráfico de anomalias
    if 'load_zscore' in df.columns and 'date' in df.columns:
        st.markdown("### Visualização de Anomalias (Z-score)")
        fig_anomaly = charts.create_anomaly_scatter(
            df=df,
            x_col='date',
            y_col='load_zscore',
            anomaly_col='is_anomaly',
            title='Detecção de Anomalias por Z-score'
        )
        st.plotly_chart(fig_anomaly, use_container_width=True)

    # Tabela de anomalias
    if total_anomalias > 0:
        st.markdown("### Top 10 Anomalias")
        if 'load_zscore' in df.columns:
            anomalies_df = df[df['is_anomaly'] == 1].nlargest(10, 'load_zscore')[
                ['date', 'val_cargaenergiamwmed', 'temp_mean', 'load_zscore']
            ]
            anomalies_df.columns = ['Data', 'Carga (MW)', 'Temp (°C)', 'Z-Score']
            st.dataframe(anomalies_df, use_container_width=True, hide_index=True)


def ml_predictions(df):
    """
    Predições do modelo de Machine Learning.
    """
    st.subheader("🤖 Machine Learning - Predições")

    model_path = Path("data/models/anomaly_detector.pkl")

    if not model_path.exists():
        st.warning("⚠️ Modelo ML não encontrado!")
        st.info("Treine o modelo primeiro: `python scripts/train_model.py`")
        return

    if AnomalyDetector is None:
        st.error("Erro ao importar AnomalyDetector")
        return

    # Carrega modelo
    try:
        detector = AnomalyDetector.load(str(model_path))
        st.success("✅ Modelo carregado com sucesso!")

        # Info do modelo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tipo de Modelo", "Random Forest")
        with col2:
            st.metric("Features", len(detector.feature_names) if detector.feature_names else "N/A")
        with col3:
            st.metric("Status", "Treinado" if detector.is_trained else "Não Treinado")

        st.markdown("---")

        # Predições
        predictions = detector.predict(df)
        prediction_proba = detector.predict_proba(df)

        df_pred = df.copy()
        df_pred['ml_prediction'] = predictions
        df_pred['ml_confidence'] = prediction_proba[:, 1]

        # Métricas de predição
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Anomalias Previstas (ML)", f"{predictions.sum()}")
        with col2:
            if 'is_anomaly' in df.columns:
                agreement = (predictions == df['is_anomaly']).mean()
                st.metric("Taxa de Concordância", f"{agreement:.1%}")
        with col3:
            avg_conf = prediction_proba[predictions == 1, 1].mean() if predictions.sum() > 0 else 0
            st.metric("Confiança Média", f"{avg_conf:.1%}")

        # Feature importance
        st.markdown("---")
        st.markdown("### Feature Importance")
        importance_df = detector.get_feature_importance()

        import plotly.graph_objects as go
        fig_importance = go.Figure(data=[
            go.Bar(
                x=importance_df['importance'],
                y=importance_df['feature'],
                orientation='h',
                marker_color='rgba(102, 126, 234, 0.8)'
            )
        ])
        fig_importance.update_layout(
            title="Importância das Features",
            xaxis_title="Importância",
            yaxis_title="Feature",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_importance, use_container_width=True)

        # Top predições
        if predictions.sum() > 0:
            st.markdown("---")
            st.markdown("### Top 10 Predições por Confiança")
            ml_anomalies = df_pred[df_pred['ml_prediction'] == 1].nlargest(10, 'ml_confidence')[
                ['date', 'val_cargaenergiamwmed', 'temp_mean', 'ml_confidence']
            ]
            ml_anomalies.columns = ['Data', 'Carga (MW)', 'Temp (°C)', 'Confiança']
            st.dataframe(ml_anomalies, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro ao carregar modelo: {str(e)}")


def export_reports(df, regiao):
    """
    Export de dados e geração de relatórios.
    """
    st.subheader("📥 Export & Relatórios")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Exportar Dados")

        export_cols = st.multiselect(
            "Selecione colunas",
            options=df.columns.tolist(),
            default=['date', 'val_cargaenergiamwmed', 'temp_mean'] if 'date' in df.columns else df.columns[:3].tolist()
        )

        if export_cols:
            export_df = df[export_cols].copy()

            # CSV
            csv = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"energy_data_{regiao}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                export_df.to_excel(writer, sheet_name='Dados', index=False)
            st.download_button(
                label="📊 Download Excel",
                data=buffer.getvalue(),
                file_name=f"energy_data_{regiao}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            st.success(f"✅ Pronto para exportar {len(export_df)} registros")

    with col2:
        st.markdown("#### Gerar Relatório")

        if st.button("🎯 Gerar Relatório", use_container_width=True, type="primary"):
            report_md = f"""# Relatório de Análise Energética
## Região: {regiao}

### Métricas Principais
- Total de Registros: {len(df):,}
- Carga Média: {df['val_cargaenergiamwmed'].mean():,.0f} MW
- Temperatura Média: {df['temp_mean'].mean():.1f}°C
- Anomalias: {df['is_anomaly'].sum() if 'is_anomaly' in df.columns else 0}

### Estatísticas
#### Carga (MW)
- Média: {df['val_cargaenergiamwmed'].mean():,.1f}
- Mediana: {df['val_cargaenergiamwmed'].median():,.1f}
- Desvio Padrão: {df['val_cargaenergiamwmed'].std():,.1f}

#### Temperatura (°C)
- Média: {df['temp_mean'].mean():.2f}
- Min: {df['temp_min'].min():.2f}
- Max: {df['temp_max'].max():.2f}

---
*Gerado em: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*
"""

            with st.expander("📄 Preview do Relatório", expanded=True):
                st.markdown(report_md)

            st.download_button(
                label="📝 Download Relatório (Markdown)",
                data=report_md.encode('utf-8'),
                file_name=f"relatorio_{regiao}.md",
                mime="text/markdown",
                use_container_width=True
            )

    # Preview dos dados
    st.markdown("---")
    st.markdown("### Preview dos Dados")
    st.dataframe(df.head(10), use_container_width=True)
