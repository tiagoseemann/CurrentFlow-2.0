# ⚡ Quickstart - Energy Analytics Dashboard

## 🚀 Rodar o Dashboard (3 Métodos)

### Método 1: Script Automatizado (RECOMENDADO)

```bash
./run_dashboard.sh
```

Este script:
- Configura PYTHONPATH automaticamente
- Verifica se dados estão processados
- Inicia o dashboard

### Método 2: Comando Manual

```bash
export PYTHONPATH=$(pwd)
uv run streamlit run src/app/main.py
```

### Método 3: Sem UV

```bash
export PYTHONPATH=$(pwd)
streamlit run src/app/main.py
```

---

## 📊 Primeira Vez? Gere os Dados Primeiro

```bash
# Rode o pipeline para gerar dados processados
export PYTHONPATH=$(pwd)
uv run python scripts/test_pipeline.py
```

Isso vai:
- Baixar dados do ONS (2023)
- Baixar dados do INMET (567 estações)
- Processar e salvar em `data/processed/energy_weather_processed.parquet`

**Tempo:** ~2-5 minutos na primeira vez

---

## 🌐 URLs do Dashboard

Após iniciar, acesse:

- **Local**: http://localhost:8501
- **Network**: Veja no terminal

---

## 🛑 Parar o Dashboard

Pressione `Ctrl+C` no terminal

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'src'"

**Solução**: Sempre rode com PYTHONPATH configurado:

```bash
export PYTHONPATH=$(pwd)
uv run streamlit run src/app/main.py
```

Ou use o script `./run_dashboard.sh`

### Erro: "FileNotFoundError: data/processed/..."

**Solução**: Gere os dados primeiro:

```bash
export PYTHONPATH=$(pwd)
uv run python scripts/test_pipeline.py
```

### Dashboard lento na primeira carga

**Normal!** O Streamlit carrega e processa os dados.
- Primeira carga: ~5-10 segundos
- Próximas: < 1 segundo (cache)

---

## 📚 Documentação Completa

- **Dashboard Guide**: Ver `DASHBOARD_GUIDE.md`
- **Development Plan**: Ver `DEVELOPMENT_PLAN.md`
- **Implementation Status**: Ver `IMPLEMENTATION_STATUS.md`

---

## 🎯 Navegação Rápida

### Sidebar (Esquerda)
- **📅 Select Year**: Escolha 2023 ou 2024
- **🗺️ Region Filter**: Filtre por região
- **📆 Date Range**: Ative para filtrar período

### Tabs (Topo)
- **📈 Overview**: KPIs + Gráficos principais
- **🗺️ Regional Analysis**: Comparações entre regiões
- **⚠️ Anomalies**: Detecção de anomalias
- **🔬 Correlation**: Análise de correlações

---

## ⚡ Dicas Rápidas

1. **Hover** sobre gráficos para ver valores
2. **Clique e arraste** para zoom
3. **Duplo clique** para resetar zoom
4. **📷 ícone** no canto para baixar gráfico
5. **Filtros** aplicam em tempo real

---

**Criado:** 2025-12-03
**Versão:** 2.0
