#!/usr/bin/env python3
"""
Script para processar dados de múltiplos anos.

Processa dados do ONS e INMET para os anos especificados e salva
em arquivos Parquet separados.

Uso:
    python scripts/process_multiyear_data.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loaders import ONSLoader, INMETLoader
from src.data.preprocessor import Preprocessor


def process_year(year: int) -> bool:
    """
    Processa dados de um ano específico.

    Args:
        year: Ano a ser processado

    Returns:
        True se sucesso, False caso contrário
    """
    print(f"\n{'='*60}")
    print(f"Processando dados de {year}")
    print(f"{'='*60}")

    try:
        # Inicializa componentes
        ons_loader = ONSLoader()
        inmet_loader = INMETLoader()
        preprocessor = Preprocessor()

        # Carrega dados
        print(f"\n📊 Carregando dados do ONS ({year})...")
        ons_df = ons_loader.load(year)
        print(f"   ✓ {len(ons_df):,} registros carregados")

        print(f"\n🌦️  Carregando dados do INMET ({year})...")
        inmet_df = inmet_loader.load(year)
        print(f"   ✓ {len(inmet_df):,} registros carregados")

        # Processa
        print(f"\n⚙️  Processando e gerando features...")
        df = preprocessor.process(ons_df, inmet_df, save=False)
        print(f"   ✓ {len(df):,} registros processados")
        print(f"   ✓ {len(df.columns)} features geradas")

        # Salva com nome específico do ano
        output_path = Path(f"data/processed/energy_weather_{year}.parquet")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n💾 Salvando em {output_path}...")
        df.to_parquet(output_path)

        file_size = output_path.stat().st_size / 1024  # KB
        print(f"   ✓ Arquivo salvo ({file_size:.1f} KB)")

        print(f"\n✅ Ano {year} processado com sucesso!")
        return True

    except Exception as e:
        print(f"\n❌ Erro ao processar {year}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Processa múltiplos anos."""
    print("🚀 Processamento de Dados Multi-Ano")
    print("=" * 60)

    # Anos a processar
    years_to_process = [2021, 2022, 2023, 2024]

    # Verifica quais já existem
    existing_years = []
    missing_years = []

    for year in years_to_process:
        cache_path = Path(f"data/processed/energy_weather_{year}.parquet")
        if cache_path.exists():
            existing_years.append(year)
        else:
            missing_years.append(year)

    print(f"\n📁 Status dos arquivos:")
    print(f"   ✓ Já existem: {existing_years}")
    print(f"   ⚠️  Faltando: {missing_years}")

    if not missing_years:
        print(f"\n✅ Todos os anos já foram processados!")
        return

    # Pergunta se deve processar os faltantes
    print(f"\n📋 Serão processados: {len(missing_years)} ano(s)")
    print(f"   Anos: {missing_years}")

    response = input(f"\n❓ Deseja continuar? [s/N]: ").strip().lower()
    if response not in ['s', 'sim', 'y', 'yes']:
        print("❌ Processamento cancelado.")
        return

    # Processa cada ano faltante
    successful = []
    failed = []

    for year in missing_years:
        if process_year(year):
            successful.append(year)
        else:
            failed.append(year)

    # Resumo
    print(f"\n{'='*60}")
    print("📊 RESUMO DO PROCESSAMENTO")
    print(f"{'='*60}")
    print(f"✅ Sucesso: {len(successful)} ano(s) - {successful}")
    print(f"❌ Falha: {len(failed)} ano(s) - {failed}")

    if successful:
        print(f"\n💡 Arquivos gerados em: data/processed/")
        print(f"   Você pode agora selecionar estes anos no dashboard!")


if __name__ == "__main__":
    main()
