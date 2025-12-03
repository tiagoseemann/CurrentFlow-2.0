# ⚡ Energy Analytics Dashboard

**Plataforma profissional de análise energética do Brasil** com dashboard interativo, pipeline robusto de dados e machine learning para detecção de anomalias.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Objetivo

Construir um sistema completo de análise energética que:
1. **Coleta** dados do ONS (carga) e INMET (meteorologia)
2. **Processa** com pipeline ETL robusto
3. **Visualiza** em dashboard interativo profissional
4. **Detecta** anomalias usando Machine Learning

---

## 📊 Features

### ✅ Implementado

#### Backend (Pipeline de Dados)
- 🔄 **ONSLoader**: Download automático de dados do ONS
  - 567 estações meteorológicas
  - Sistema de cache inteligente
  - Parsing de CSV brasileiro
- 🌦️ **INMETLoader**: Dados meteorológicos completos
  - ~5M registros/ano processados
  - Mapeamento automático de regiões
- ⚙️ **Preprocessor**: ETL completo
  - Limpeza de dados (nulls, outliers)
  - 19 features engineered
  - Detecção automática de anomalias (Z-score)

#### Frontend (Dashboard)
- 📊 **Dashboard V2 Profissional**
  - KPIs principais
  - Gráficos dual-axis (Carga × Temperatura)
  - Bandas de confiança (±1σ, ±2σ)
  - Análise regional comparativa
  - Heatmap de correlações
  - Detecção visual de anomalias
  - Filtros interativos (região, data)

### 🔲 Roadmap

#### Fase 2: Dashboard Avançado
- Mapas interativos do Brasil
- Análise sazonal detalhada
- Export de relatórios (PDF, Excel)
- Comparação ano a ano

#### Fase 3: Machine Learning
- Modelo preditivo de anomalias (XGBoost)
- SHAP values para explicabilidade
- Previsão de carga (LSTM)
- API REST para predições
- Alertas automáticos

---

## 🚀 Quickstart

### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/tiagoseemann/CurrentFlow-2.0.git
cd CurrentFlow-2.0

# Instale dependências (usando UV)
uv sync

# Ou com pip
pip install -r requirements.txt
```

### 2. Gerar Dados Processados (Primeira Vez)

```bash
# Rode o pipeline completo
PYTHONPATH=. uv run python scripts/test_pipeline.py

# Isso vai:
# - Baixar dados do ONS (2023)
# - Baixar dados do INMET (567 estações)
# - Processar e gerar features
# - Salvar em data/processed/energy_weather_processed.parquet
```

### 3. Rodar o Dashboard

```bash
# Dashboard V2 (Recomendado)
streamlit run src/app/main.py

# Dashboard V1 (Antigo)
streamlit run src/app.py
```

Acesse: http://localhost:8501

---

## 📁 Estrutura do Projeto

```
current-flow-v2/
├── src/
│   ├── app/                    # Dashboard V2 (Frontend)
│   │   ├── main.py            # Entry point Streamlit
│   │   ├── components/
│   │   │   ├── metrics.py     # KPI cards
│   │   │   └── charts.py      # Gráficos Plotly
│   │   └── pages/             # Páginas futuras
│   ├── data/                  # Backend (ETL)
│   │   ├── loaders.py         # ONSLoader + INMETLoader
│   │   └── preprocessor.py    # Pipeline completo
│   ├── utils/
│   │   └── config.py          # Mapeamentos de regiões
│   ├── app.py                 # Dashboard V1 (antigo)
│   └── dashboard.py           # Funções antigas
├── scripts/
│   ├── test_pipeline.py       # Testa pipeline completo
│   ├── test_ons_loader.py     # Testa ONS
│   └── test_inmet_loader.py   # Testa INMET
├── data/
│   ├── raw/                   # Cache de downloads (gitignored)
│   └── processed/             # Dados processados (Parquet)
├── notebooks_explore/         # Jupyter notebooks
├── DASHBOARD_GUIDE.md         # Guia de uso do dashboard
├── DEVELOPMENT_PLAN.md        # Plano de desenvolvimento
├── IMPLEMENTATION_STATUS.md   # Status da implementação
└── pyproject.toml             # Dependências
```

---

## 📊 Dados

### Fontes

1. **ONS** (Operador Nacional do Sistema Elétrico)
   - Carga energética diária por região
   - URL: `https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/carga_energia_di/`
   - Formato: CSV

2. **INMET** (Instituto Nacional de Meteorologia)
   - Dados meteorológicos horários
   - 567 estações em todo Brasil
   - URL: `https://portal.inmet.gov.br/uploads/dadoshistoricos/`
   - Formato: ZIP (múltiplos CSVs)

### Regiões

- **Norte**: AC, AP, AM, PA, RO, RR, TO (88 estações)
- **Nordeste**: AL, BA, CE, MA, PB, PE, PI, RN, SE (142 estações)
- **Sudeste/Centro-Oeste**: ES, MG, RJ, SP, DF, GO, MT, MS (242 estações)
- **Sul**: PR, RS, SC (95 estações)

---

## 🔧 Uso Avançado

### Carregar Dados Programaticamente

```python
from src.data.loaders import ONSLoader, INMETLoader
from src.data.preprocessor import Preprocessor

# Carregar dados
ons = ONSLoader().load(2023)
inmet = INMETLoader().load(2023)

# Processar
preprocessor = Preprocessor()
df = preprocessor.process(ons, inmet, save=True)

# Analisar
print(df.head())
print(f"Anomalias detectadas: {df['is_anomaly'].sum()}")
```

### Análise Rápida

```bash
# Estatísticas resumidas
PYTHONPATH=. python scripts/quick_analysis.py
```

---

## 📈 Resultados (Dados de 2023)

### Métricas

- **Registros processados**: 1,460
- **Features geradas**: 19
- **Anomalias detectadas**: 10 (0.68%)
- **Correlação Temp×Carga**:
  - Norte: 0.828 (forte)
  - Sudeste/CO: 0.696
  - Nordeste: 0.668
  - Sul: 0.475

### Consumo Médio por Região

| Região | Carga Média (MW) | Temp Média (°C) |
|--------|------------------|-----------------|
| Sudeste/Centro-Oeste | 41,881 | 23.4 |
| Sul | 12,567 | 19.4 |
| Nordeste | 12,117 | 26.3 |
| Norte | 7,140 | 26.8 |

---

## 🛠️ Desenvolvimento

### Rodar Testes

```bash
# Pipeline completo
PYTHONPATH=. python scripts/test_pipeline.py

# ONS apenas
PYTHONPATH=. python scripts/test_ons_loader.py

# INMET apenas
PYTHONPATH=. python scripts/test_inmet_loader.py
```

### Contribuir

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m "feat: adiciona nova feature"`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request

---

## 📚 Documentação Completa

- 📊 **[Dashboard Guide](DASHBOARD_GUIDE.md)** - Como usar o dashboard
- 🚀 **[Development Plan](DEVELOPMENT_PLAN.md)** - Plano de desenvolvimento
- ✅ **[Implementation Status](IMPLEMENTATION_STATUS.md)** - Status atual

---

## 🤝 Equipe

- **Tiago Seemann** - Pipeline de Dados & Dashboard
- **Colaborador** - Dashboard Inicial & Dados

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- **ONS** - Dados de carga energética
- **INMET** - Dados meteorológicos
- **Streamlit** - Framework de dashboard
- **Plotly** - Visualizações interativas

---

<div align="center">

**⚡ Energy Analytics Dashboard**

*Análise profissional de dados energéticos do Brasil*

[Documentação](DASHBOARD_GUIDE.md) • [Roadmap](DEVELOPMENT_PLAN.md) • [Status](IMPLEMENTATION_STATUS.md)

</div>


