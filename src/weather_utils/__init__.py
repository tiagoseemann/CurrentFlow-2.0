"""
Adiciona o diretório src ao sys.path para permitir imports internos
quando o pacote weather_utils é usado dentro do projeto.
"""

import sys
from pathlib import Path

# Obtém o diretório raiz do projeto (dois níveis acima deste arquivo)
project_root = Path(__file__).resolve().parents[1]

# Caminho para a pasta src/, onde ficam os módulos principais do projeto
src_path = project_root / "src"

# Adiciona ao sys.path para habilitar imports relativos
sys.path.append(str(src_path))
