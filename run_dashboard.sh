#!/bin/bash
# Script para rodar o Energy Analytics Dashboard

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}⚡ Energy Analytics Dashboard${NC}"
echo "================================"
echo ""

# Configura PYTHONPATH
export PYTHONPATH="$(pwd)"

# Verifica se dados processados existem
if [ ! -f "data/processed/energy_weather_processed.parquet" ]; then
    echo -e "${GREEN}📊 Gerando dados processados (primeira vez)...${NC}"
    echo "Isso pode levar 2-5 minutos..."
    echo ""
    uv run python scripts/test_pipeline.py
    echo ""
fi

echo -e "${GREEN}🚀 Iniciando dashboard...${NC}"
echo ""
echo "URLs disponíveis:"
echo "  Local:   http://localhost:8501"
echo "  Network: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

# Roda o Streamlit
uv run streamlit run src/app/main.py
