import requests
from pathlib import Path
import argparse

def baixar_arquivo(url: str, destino: Path):
    """Baixa o arquivo da URL e salva no caminho especificado."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    print(f"Baixando: {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    with open(destino, "wb") as f:
        f.write(resp.content)

    print(f"Arquivo salvo em: {destino.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="Baixa o arquivo de programação diária da ONS")
    parser.add_argument("--url", required=True, help="URL do arquivo XLSX da ONS")
    parser.add_argument("--output-dir", default="data/raw", help="Diretório de saída")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    nome_arquivo = Path(args.url).name
    destino = output_dir / nome_arquivo

    baixar_arquivo(args.url, destino)

if __name__ == "__main__":
    main()
