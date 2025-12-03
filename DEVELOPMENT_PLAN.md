# 🚀 Energy Analytics Dashboard - Plano de Desenvolvimento

**Status:** Main atualizada com PR #4 merged
**Data:** 2025-12-03
**Objetivo:** Dashboard profissional de análise energética com ML

---

## 📊 Estado Atual do Projeto

### ✅ O Que Já Temos (Após Merge)

#### Backend (Pipeline de Dados)
- ✅ **ONSLoader**: Download automático com cache
- ✅ **INMETLoader**: 567 estações meteorológicas
- ✅ **Preprocessor**: ETL completo com 19 features
- ✅ **Utils**: Mapeamento de 27 estados para 4 regiões

#### Frontend (Dashboard Básico)
- ✅ **app.py**: Streamlit app funcional
- ✅ **dashboard.py**: 4 visualizações básicas
  - Correlação
  - Scatter plots
  - Séries temporais
  - Comparação de regiões

#### Dados
- ✅ Dados ONS 2024 (CARGA_ENERGIA_2024.csv)
- ✅ Dados INMET de 11 cidades específicas
- ✅ Pipeline de merge funcional (merge_datasets.py)

### ⚠️ Problemas Identificados

1. **Duplicação de Código**
   - `merge_datasets.py` usa código antigo
   - Não aproveita loaders robustos (ONSLoader, INMETLoader)
   - Processamento manual vs Preprocessor automático

2. **Dashboard Básico**
   - Visualizações simples (sem insights)
   - Sem KPIs principais
   - Sem detecção de anomalias visível
   - Sem filtros temporais

3. **Dependências Faltantes**
   - Streamlit não está em `pyproject.toml`
   - Plotly não está declarado

4. **Arquitetura**
   - Código de produção (loaders) não usado no dashboard
   - Dados estáticos vs sistema dinâmico

---

## 🎯 Roadmap Profissional - 3 Fases

### **FASE 1: Consolidação e Refatoração** (Agora)
**Tempo estimado:** 2-3 horas de desenvolvimento
**Objetivo:** Sistema unificado usando código de produção

#### Task 1.1: Atualizar Dependências
- [ ] Adicionar Streamlit ao pyproject.toml
- [ ] Adicionar Plotly
- [ ] Adicionar outras libs necessárias (XGBoost para ML)

#### Task 1.2: Refatorar Dashboard para Usar Pipeline Robusto
- [ ] Substituir `merge_datasets.py` por chamadas ao Preprocessor
- [ ] Criar `src/app_v2.py` (versão profissional)
- [ ] Manter compatibilidade com app antigo

#### Task 1.3: Estrutura de Pastas Profissional
```
src/
├── app/                    # Frontend (novo)
│   ├── __init__.py
│   ├── main.py            # Entry point Streamlit
│   ├── pages/
│   │   ├── 01_overview.py
│   │   ├── 02_regional.py
│   │   └── 03_anomalies.py
│   └── components/
│       ├── charts.py
│       └── metrics.py
├── data/                  # Backend (existente)
├── models/                # ML (novo)
└── utils/                 # Helpers (existente)
```

---

### **FASE 2: Dashboard Profissional** (Próximo)
**Tempo estimado:** 3-4 horas
**Objetivo:** Visualizações de nível corporativo

#### Task 2.1: Página de Overview (Visão Executiva)
**Componentes:**
- [ ] KPI Cards com métricas principais
  - Carga média nacional
  - Temperatura média
  - Anomalias detectadas (últimos 30 dias)
  - Correlação Temp×Carga por região
- [ ] Gráfico dual-axis: Carga + Temperatura
- [ ] Bandas de confiança (±1σ, ±2σ)
- [ ] Mapa do Brasil colorido por região

#### Task 2.2: Página de Análise Regional
**Componentes:**
- [ ] Filtros interativos (região, período)
- [ ] Comparação entre regiões (boxplots)
- [ ] Séries temporais com médias móveis
- [ ] Sazonalidade (Summer, Fall, Winter, Spring)
- [ ] Heatmap de correlações

#### Task 2.3: Página de Anomalias
**Componentes:**
- [ ] Tabela de anomalias detectadas (top 10)
- [ ] Gráfico de dispersão: Z-score × Data
- [ ] Drill-down por região
- [ ] Timeline de anomalias
- [ ] Estatísticas (taxa de anomalia, distribuição)

#### Task 2.4: Melhorias UX
- [ ] Sidebar com logo e navegação
- [ ] Loading states
- [ ] Cache de dados (@st.cache_data)
- [ ] Tema customizado
- [ ] Responsividade mobile

---

### **FASE 3: Machine Learning** (Depois)
**Tempo estimado:** 4-5 horas
**Objetivo:** Modelo preditivo de anomalias

#### Task 3.1: Feature Engineering Avançado
- [ ] Lag features (t-1, t-7, t-30)
- [ ] Interações (temp × dia_semana)
- [ ] Encoding de variáveis categóricas
- [ ] Normalização/Standardização

#### Task 3.2: Modelo de Classificação
**Algoritmos a testar:**
- [ ] Random Forest (baseline)
- [ ] XGBoost
- [ ] Isolation Forest (unsupervised)
- [ ] LSTM (séries temporais)

**Métricas:**
- [ ] Precision, Recall, F1-Score
- [ ] ROC-AUC
- [ ] Confusion Matrix
- [ ] Feature Importance (SHAP)

#### Task 3.3: Integração com Dashboard
- [ ] Página de Predições
- [ ] Confidence scores
- [ ] Explicabilidade (SHAP values)
- [ ] Model performance tracking

---

## 📋 Implementação Detalhada - FASE 1

### Step 1: Atualizar Dependências

```toml
# pyproject.toml
dependencies = [
    "pandas>=2.2.2",
    "numpy>=2.1.2",
    "matplotlib>=3.9.2",
    "seaborn>=0.13.2",
    "openpyxl>=3.1.5",
    "requests>=2.32.3",
    "scikit-learn>=1.5.2",
    "pyarrow>=22.0.0",
    "streamlit>=1.28.0",      # ← Novo
    "plotly>=5.18.0",         # ← Novo
    "xgboost>=2.0.0",         # ← Para ML
    "shap>=0.43.0",           # ← Explicabilidade
]
```

### Step 2: Criar Novo Entry Point

```python
# src/app/main.py
import streamlit as st
from src.data.loaders import ONSLoader, INMETLoader
from src.data.preprocessor import Preprocessor

st.set_page_config(
    page_title="Energy Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data(year=2023):
    """Carrega e processa dados usando pipeline robusto."""
    ons = ONSLoader().load(year)
    inmet = INMETLoader().load(year)
    preprocessor = Preprocessor()
    return preprocessor.process(ons, inmet, save=False)

df = load_data()
st.title("⚡ Energy Analytics Dashboard")
# ... resto do código
```

### Step 3: Componentes Reutilizáveis

```python
# src/app/components/metrics.py
import streamlit as st

def display_kpi(label, value, delta=None, format_str="{:,.0f}"):
    """Exibe KPI card."""
    col = st.columns(1)[0]
    col.metric(
        label=label,
        value=format_str.format(value),
        delta=delta
    )
```

---

## 🎨 Design System (Tema do Dashboard)

### Paleta de Cores
```python
COLORS = {
    'primary': '#1f77b4',      # Azul
    'secondary': '#ff7f0e',    # Laranja
    'success': '#2ca02c',      # Verde
    'danger': '#d62728',       # Vermelho
    'warning': '#ff9800',      # Amarelo
    'info': '#17a2b8',         # Ciano
}

REGIONS = {
    'Norte': '#2ecc71',
    'Nordeste': '#e74c3c',
    'Sudeste/Centro-Oeste': '#3498db',
    'Sul': '#f39c12',
}
```

### Tipografia
- **Título**: Streamlit default (sem-serif)
- **Corpo**: 14px
- **Métricas**: 24px bold

---

## 📊 Métricas de Sucesso

### Performance
- [ ] Dashboard carrega em < 3 segundos
- [ ] Cache de dados funciona corretamente
- [ ] Gráficos renderizam em < 1 segundo

### Qualidade de Código
- [ ] 100% type hints
- [ ] Docstrings Google style
- [ ] Cobertura de testes > 80%
- [ ] Sem código duplicado

### UX
- [ ] Interface intuitiva (user testing)
- [ ] Mobile-friendly
- [ ] Acessível (contraste, tamanho de fonte)

---

## 🔄 Fluxo de Desenvolvimento

1. **Criar branch de feature**: `feat/dashboard-v2`
2. **Desenvolver incrementalmente** (commits pequenos)
3. **Testar localmente**: `streamlit run src/app/main.py`
4. **Code review** (se em equipe)
5. **Merge para main**
6. **Deploy** (Streamlit Cloud ou Heroku)

---

## 📚 Recursos e Referências

### Streamlit
- Docs: https://docs.streamlit.io
- Gallery: https://streamlit.io/gallery
- Components: https://streamlit.io/components

### Plotly
- Docs: https://plotly.com/python/
- Templates: https://plotly.com/python/templates/

### Machine Learning
- Scikit-learn: https://scikit-learn.org
- XGBoost: https://xgboost.readthedocs.io
- SHAP: https://shap.readthedocs.io

---

## ⏱️ Timeline

| Fase | Tarefas | Tempo | Status |
|------|---------|-------|--------|
| **Fase 1** | Consolidação | 2-3h | 🔄 Em andamento |
| **Fase 2** | Dashboard Pro | 3-4h | ⏸️ Aguardando |
| **Fase 3** | ML | 4-5h | ⏸️ Aguardando |
| **Total** | - | **9-12h** | - |

---

## 🎯 Próxima Ação Imediata

**AGORA:** Começar Fase 1 - Task 1.1
1. Adicionar Streamlit e Plotly ao pyproject.toml
2. Instalar dependências
3. Testar dashboard atual
4. Criar estrutura de pastas nova

---

**Última atualização:** 2025-12-03
