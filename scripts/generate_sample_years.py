#!/usr/bin/env python3
"""
Gera dados de exemplo para múltiplos anos baseados nos dados de 2023.

Este script cria dados simulados para demonstrar a funcionalidade multi-ano
sem precisar baixar dados reais que podem não estar disponíveis.

Uso:
    python scripts/generate_sample_years.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))


def generate_year_data(base_df: pd.DataFrame, target_year: int) -> pd.DataFrame:
    """
    Gera dados simulados para um ano baseado nos dados base.

    Args:
        base_df: DataFrame com dados de 2023
        target_year: Ano alvo para gerar dados

    Returns:
        DataFrame com dados do ano alvo
    """
    df = base_df.copy()

    # Ajusta as datas
    df['date'] = pd.to_datetime(df['date'])
    year_diff = target_year - 2023
    df['date'] = df['date'] + pd.DateOffset(years=year_diff)
    df['year'] = target_year

    # Adiciona variação realística aos dados
    np.random.seed(target_year)  # Seed baseado no ano para consistência

    # Variação na carga (±5%)
    df['val_cargaenergiamwmed'] = df['val_cargaenergiamwmed'] * (1 + np.random.uniform(-0.05, 0.05, len(df)))

    # Variação na temperatura (±2°C)
    temp_variation = np.random.uniform(-2, 2, len(df))
    df['temp_mean'] = df['temp_mean'] + temp_variation
    df['temp_min'] = df['temp_min'] + temp_variation
    df['temp_max'] = df['temp_max'] + temp_variation

    # Variação na radiação (±10%)
    df['radiation_mean'] = df['radiation_mean'] * (1 + np.random.uniform(-0.1, 0.1, len(df)))

    # Variação na precipitação (±20%)
    df['precipitation_total'] = df['precipitation_total'] * (1 + np.random.uniform(-0.2, 0.2, len(df)))
    df['precipitation_total'] = df['precipitation_total'].clip(lower=0)  # Não pode ser negativo

    # Recalcula features derivadas
    if 'temp_range' in df.columns:
        df['temp_range'] = df['temp_max'] - df['temp_min']

    if 'load_zscore' in df.columns:
        # Recalcula Z-score por região
        df['load_zscore'] = df.groupby('region')['val_cargaenergiamwmed'].transform(
            lambda x: (x - x.mean()) / x.std()
        )

    if 'is_anomaly' in df.columns:
        df['is_anomaly'] = (df['load_zscore'].abs() > 3).astype(int)

    # Recalcula médias móveis se existirem
    for window in [7, 30]:
        col_load = f'load_ma_{window}d'
        col_temp = f'temp_ma_{window}d'

        if col_load in df.columns:
            df[col_load] = df.groupby('region')['val_cargaenergiamwmed'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )

        if col_temp in df.columns:
            df[col_temp] = df.groupby('region')['temp_mean'].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )

    # Recalcula lag features se existirem
    for lag in [1, 7]:
        col_load = f'load_lag_{lag}d'
        col_temp = f'temp_lag_{lag}d'

        if col_load in df.columns:
            df[col_load] = df.groupby('region')['val_cargaenergiamwmed'].shift(lag)

        if col_temp in df.columns:
            df[col_temp] = df.groupby('region')['temp_mean'].shift(lag)

    # Recalcula interações se existirem
    if 'load_x_temp' in df.columns:
        df['load_x_temp'] = df['val_cargaenergiamwmed'] * df['temp_mean']

    if 'temp_x_dayofweek' in df.columns:
        df['temp_x_dayofweek'] = df['temp_mean'] * df['day_of_week']

    # Recalcula mom se existir
    if 'load_mom' in df.columns:
        df['load_mom'] = df.groupby('region')['val_cargaenergiamwmed'].pct_change(periods=30)

    return df


def main():
    """Gera dados de exemplo para múltiplos anos."""
    print("🎲 Gerador de Dados de Exemplo Multi-Ano")
    print("=" * 60)

    # Carrega dados base (2023)
    base_path = Path("data/processed/energy_weather_2023.parquet")

    if not base_path.exists():
        print(f"❌ Arquivo base não encontrado: {base_path}")
        print(f"   Execute primeiro o pipeline para gerar dados de 2023.")
        return

    print(f"\n📂 Carregando dados base de 2023...")
    base_df = pd.read_parquet(base_path)
    print(f"   ✓ {len(base_df):,} registros")
    print(f"   ✓ {len(base_df.columns)} colunas")

    # Anos a gerar
    years_to_generate = [2021, 2022, 2024]

    print(f"\n📋 Gerando dados para {len(years_to_generate)} anos:")
    print(f"   Anos: {years_to_generate}")
    print(f"\n⚠️  ATENÇÃO: Estes são dados SIMULADOS para demonstração!")
    print(f"   Baseados em 2023 com variações aleatórias realísticas.")

    response = input(f"\n❓ Deseja continuar? [s/N]: ").strip().lower()
    if response not in ['s', 'sim', 'y', 'yes']:
        print("❌ Geração cancelada.")
        return

    # Gera dados para cada ano
    for year in years_to_generate:
        print(f"\n{'='*60}")
        print(f"Gerando dados de {year}")
        print(f"{'='*60}")

        # Gera dados
        df_year = generate_year_data(base_df, year)

        # Salva
        output_path = Path(f"data/processed/energy_weather_{year}.parquet")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n💾 Salvando em {output_path}...")
        df_year.to_parquet(output_path)

        file_size = output_path.stat().st_size / 1024  # KB
        print(f"   ✓ Arquivo salvo ({file_size:.1f} KB)")

        # Estatísticas
        print(f"\n📊 Estatísticas de {year}:")
        print(f"   - Registros: {len(df_year):,}")
        print(f"   - Período: {df_year['date'].min().strftime('%Y-%m-%d')} a {df_year['date'].max().strftime('%Y-%m-%d')}")
        print(f"   - Carga média: {df_year['val_cargaenergiamwmed'].mean():,.0f} MW")
        print(f"   - Temp média: {df_year['temp_mean'].mean():.1f}°C")
        print(f"   - Anomalias: {df_year['is_anomaly'].sum()}")

    # Resumo final
    print(f"\n{'='*60}")
    print("✅ GERAÇÃO COMPLETA")
    print(f"{'='*60}")
    print(f"\n💡 Arquivos gerados em: data/processed/")
    print(f"   - energy_weather_2021.parquet")
    print(f"   - energy_weather_2022.parquet")
    print(f"   - energy_weather_2023.parquet (já existia)")
    print(f"   - energy_weather_2024.parquet")
    print(f"\n🎯 Você pode agora selecionar qualquer ano no dashboard!")
    print(f"   ou escolher 'Todos os anos' para visualizar 4 anos juntos.")


if __name__ == "__main__":
    main()
