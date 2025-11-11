## EDA de Carga ONS – Programação Diária

Este projeto inclui um script de EDA para extrair e analisar dados de carga a partir do arquivo Excel público da ONS (Programação Diária).

- Fonte do exemplo (10/11/2025): [`https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/programacao_diaria/PROGRAMACAO_DIARIA_2025_11_10.xlsx`](https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/programacao_diaria/PROGRAMACAO_DIARIA_2025_11_10.xlsx)

### Requisitos

- Python 3.13+
- Dependências (já listadas no `pyproject.toml`):
  - pandas, numpy, matplotlib, seaborn, openpyxl, requests, scikit-learn

Instale com:

```bash
pip install -e .
```

ou:

```bash
pip install pandas numpy matplotlib seaborn openpyxl requests scikit-learn
```

### Rodando o EDA

O script baixa o Excel, inspeciona as planilhas, tenta identificar e normalizar tabelas de carga por região, salva CSVs processados e figuras com os gráficos básicos.

```bash
python scripts/eda_ons.py \
  --url "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/programacao_diaria/PROGRAMACAO_DIARIA_2025_11_10.xlsx" \
  --output-dir .
```

Saídas:
- `data/raw/PROGRAMACAO_DIARIA_YYYY-MM-DD.xlsx` – arquivo bruto baixado
- `data/processed/carga_long_YYYY-MM-DD.csv` – dados normalizados no formato longo (`timestamp`, `region`, `load_mw`)
- `reports/figures/` – figuras (`timeseries_por_regiao_*.png`, `media_diaria_por_regiao_*.png`) e um `resumo_diario_por_regiao_*.csv`

### Próximas Fases

- Fase 1: Correlacionar carga diária por região com temperatura média (regressão/classificação).
- Fase 2: Criar modelo de classificação de perfis diários de carga.
- Fase 3: Implementar detecção de anomalias para picos inexplicados.

O script atual cobre a extração/normalização e EDA inicial. As fases seguintes serão adicionadas sobre os dados processados (`data/processed`).


