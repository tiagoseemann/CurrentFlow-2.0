import streamlit as st
import plotly.express as px

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
    Plota uma série temporal usando 'data' no eixo X
    e qualquer variável numérica no eixo Y.
    """
    st.subheader("Série temporal")

    # Somente colunas numéricas podem ser escolhidas para o Y
    cols = df.select_dtypes(include="number").columns
    y = st.selectbox("Variável", cols)

    # Plota a série temporal
    fig = px.line(df, x="data", y=y)
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

    # Calcula média da variável selecionada por região
    mean_df = all_df.groupby("regiao")[var].mean().reset_index()

    # Plota comparação por barras
    fig = px.bar(mean_df, x="regiao", y=var)
    st.plotly_chart(fig, use_container_width=True)
