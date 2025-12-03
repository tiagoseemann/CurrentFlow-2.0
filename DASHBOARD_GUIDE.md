# ⚡ Energy Analytics Dashboard - Guia de Uso

## 🚀 Como Rodar o Dashboard

### Método 1: Dashboard V2 (Recomendado - Usa Pipeline Robusto)

```bash
# A partir da raiz do projeto
streamlit run src/app/main.py
```

### Método 2: Dashboard V1 (Antigo - Dados Estáticos)

```bash
streamlit run src/app.py
```

---

## 📊 Funcionalidades do Dashboard V2

### 1. Overview (Tab Principal)
**Visualizações:**
- ✅ **KPI Cards**
  - Carga média (MW)
  - Temperatura média (°C)
  - Total de anomalias
  - Taxa de anomalias (%)

- ✅ **Gráfico Dual-Axis**
  - Carga energética + Temperatura no mesmo gráfico
  - Eixo duplo (Y1: MW, Y2: °C)
  - Hover interativo

- ✅ **Bandas de Confiança**
  - Série temporal com ±1σ e ±2σ
  - Identifica visualmente valores fora do normal
  - Linha de média móvel

- ✅ **Estatísticas Resumidas**
  - Média, Mediana, Desvio Padrão
  - Valores mínimo e máximo
  - Amplitude (range)

### 2. Regional Analysis (Análise por Região)
**Visualizações:**
- ✅ **Comparação de Médias**
  - Gráfico de barras por região
  - Cores customizadas por região

- ✅ **Distribuição (Box Plot)**
  - Quartis, outliers, mediana
  - Comparação visual entre regiões

- ✅ **Tabela de Estatísticas**
  - Mean, Std, Min, Max por região
  - Contagem de anomalias por região

### 3. Anomalies (Detecção de Anomalias)
**Visualizações:**
- ✅ **Scatter Plot Z-Score**
  - Anomalias destacadas em vermelho
  - Threshold visual (Z-score > 2.5)

- ✅ **Top 10 Anomalias**
  - Tabela ordenada por Z-score
  - Data, região, carga, temperatura

### 4. Correlation (Análise de Correlação)
**Visualizações:**
- ✅ **Heatmap Interativo**
  - Matriz de correlação
  - Seleção customizável de variáveis
  - Escala de cores RdBu

- ✅ **Top 5 Correlações**
  - Pares de variáveis mais correlacionados
  - Ordenado por magnitude

---

## 🎛️ Controles Disponíveis

### Sidebar (Barra Lateral)

#### Configuração
- **📅 Seleção de Ano**: 2023 ou 2024
- **🗺️ Filtro de Região**: Norte, Nordeste, Sudeste/CO, Sul, ou Todas
- **📆 Filtro de Data**: Ativar/desativar range de datas

#### Informações
- Status do pipeline
- Última atualização
- Fontes de dados

### Tabs (Abas Superiores)
- 📈 Overview
- 🗺️ Regional Analysis
- ⚠️ Anomalies
- 🔬 Correlation

---

## 💡 Como Usar - Exemplos Práticos

### Caso 1: Analisar Consumo de uma Região Específica

1. No sidebar, selecione a região (ex: "Sudeste/Centro-Oeste")
2. Vá para a tab **Regional Analysis**
3. Observe:
   - Média de consumo vs outras regiões
   - Distribuição (box plot)
   - Estatísticas na tabela

### Caso 2: Identificar Períodos de Anomalia

1. Vá para a tab **Anomalies**
2. Observe o scatter plot:
   - Pontos vermelhos (X) = anomalias
   - Verifique datas no hover
3. Consulte a tabela "Top 10 Anomalias"
4. Filtre por região no sidebar se necessário

### Caso 3: Verificar Relação Temperatura×Carga

1. Vá para a tab **Correlation**
2. Selecione variáveis:
   - `val_cargaenergiamwmed`
   - `temp_mean`
   - `temp_max`
3. Observe o heatmap
4. Veja "Key Correlations" abaixo

### Caso 4: Análise Temporal Completa

1. Vá para a tab **Overview**
2. Analise o gráfico dual-axis:
   - Carga (azul) vs Temperatura (vermelho)
   - Identifique padrões sazonais
3. Observe o gráfico com bandas de confiança:
   - Valores fora de ±2σ são suspeitos

---

## 🔧 Troubleshooting

### Problema: "No module named 'src'"

**Solução:**
```bash
# Execute a partir da raiz do projeto
cd /caminho/para/current-flow-v2
streamlit run src/app/main.py
```

### Problema: Dashboard carregando lentamente

**Causa:** Primeira execução roda todo o pipeline (download + processamento)

**Soluções:**
1. **Aguarde**: Primeira carga leva ~2-5 minutos
2. **Use cache**: Próximas cargas usam Parquet (< 3 segundos)
3. **Pre-process**: Rode antes:
   ```bash
   PYTHONPATH=. python scripts/test_pipeline.py
   ```

### Problema: "FileNotFoundError: data/processed/..."

**Solução:**
```bash
# Gere os dados processados primeiro
PYTHONPATH=. python scripts/test_pipeline.py
```

### Problema: Gráficos não aparecem

**Causas possíveis:**
- Dados vazios após filtros
- Colunas faltantes

**Solução:**
- Limpe filtros (selecione "All" em região)
- Desative filtro de data
- Recarregue a página (Ctrl+R)

---

## 📈 Diferenças: Dashboard V1 vs V2

| Feature | V1 (app.py) | V2 (app/main.py) |
|---------|-------------|------------------|
| **Data Source** | Dados estáticos (11 cidades) | Pipeline robusto (567 estações) |
| **Data Size** | ~12 registros por região | 1,460 registros totais |
| **Loaders** | Código manual | ONSLoader + INMETLoader |
| **Features** | 3-5 features | 19 features engineered |
| **Anomaly Detection** | ❌ Não | ✅ Z-score automático |
| **Cache** | ❌ Não | ✅ Parquet + @st.cache_data |
| **Design** | Básico | Profissional (CSS customizado) |
| **Visualizations** | 4 gráficos simples | 10+ gráficos interativos |
| **Performance** | N/A | < 3s (com cache) |

---

## 🎨 Customização

### Alterar Cores

Edite `src/app/components/charts.py`:

```python
REGION_COLORS = {
    'Norte': '#2ecc71',         # Verde
    'Nordeste': '#e74c3c',      # Vermelho
    'Sudeste/Centro-Oeste': '#3498db',  # Azul
    'Sul': '#f39c12',           # Laranja
}
```

### Adicionar Novos KPIs

Edite `src/app/main.py`, seção "KPI ROW":

```python
kpi_metrics.append({
    'label': 'Novo KPI',
    'value': df['coluna'].mean(),
    'format': '{:.2f}',
    'help': 'Descrição do KPI'
})
```

### Adicionar Nova Tab

Em `src/app/main.py`:

```python
tab5 = st.tabs([..., "🆕 Nova Tab"])

with tab5:
    st.markdown("### Conteúdo da Nova Tab")
    # ... seu código aqui
```

---

## 📊 Estrutura de Dados

### Colunas Disponíveis (19 features)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | datetime | Data |
| `region` | string | Região (Norte, Nordeste, etc.) |
| `val_cargaenergiamwmed` | float | Carga energética (MW) |
| `temp_mean` | float | Temperatura média (°C) |
| `temp_min` | float | Temperatura mínima (°C) |
| `temp_max` | float | Temperatura máxima (°C) |
| `radiation_mean` | float | Radiação solar (Kj/m²) |
| `precipitation_total` | float | Precipitação total (mm) |
| `day_of_week` | int | Dia da semana (0-6) |
| `month` | int | Mês (1-12) |
| `year` | int | Ano |
| `season` | string | Estação (Summer, Fall, Winter, Spring) |
| `load_ma_7d` | float | Média móvel 7 dias (carga) |
| `load_ma_30d` | float | Média móvel 30 dias (carga) |
| `temp_ma_7d` | float | Média móvel 7 dias (temp) |
| `temp_ma_30d` | float | Média móvel 30 dias (temp) |
| `load_zscore` | float | Z-score da carga |
| `is_anomaly` | int | Flag de anomalia (0/1) |
| `load_mom` | float | Variação MoM (%) |

---

## 🔮 Próximas Funcionalidades (Roadmap)

### Fase 2 (Em Desenvolvimento)
- [ ] Página de predições
- [ ] Filtros avançados (slider de data)
- [ ] Export de dados (CSV, Excel)
- [ ] Comparação ano a ano
- [ ] Mapa do Brasil interativo

### Fase 3 (ML)
- [ ] Modelo de predição de anomalias
- [ ] SHAP values (explicabilidade)
- [ ] Previsão de carga (LSTM)
- [ ] Alertas automáticos
- [ ] API REST para predições

---

## 📚 Referências

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Python**: https://plotly.com/python/
- **Pipeline de Dados**: Ver `IMPLEMENTATION_STATUS.md`
- **Plano de Desenvolvimento**: Ver `DEVELOPMENT_PLAN.md`

---

**Última atualização:** 2025-12-03
**Versão:** 2.0
