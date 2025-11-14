import sys
from pathlib import Path

project_root = Path().resolve().parents[1]   # notebooks → raiz
src_path = project_root / 'src'

sys.path.append(str(src_path))
