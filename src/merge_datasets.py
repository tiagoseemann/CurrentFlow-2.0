import pandas as pd
from prepare_load_data import load_regions
from weather_utils.get_weather import load_inmet_file, select_relevant_columns
from weather_utils.process_weather import standardize_weather, fix_decimal_commas, merge_weather_files
from weather_utils.regions import REGIONS

# Carrega dataframes de carga (já pré-processados)
load_sul, load_se, load_norte, load_ne = load_regions()

LOAD_MAP = {
    "sul": load_sul,
    "sudeste": load_se,
    "norte": load_norte,
    "nordeste": load_ne
}

def process_weather_region(region_name: str):
    """
    Carrega, padroniza e integra todos os arquivos meteorológicos da região.
    """
    dfs_weather = []

    for path in REGIONS[region_name]:
        df = load_inmet_file(path)
        df = select_relevant_columns(df)
        df = standardize_weather(df)
        df = fix_decimal_commas(df)
        dfs_weather.append(df)

    return merge_weather_files(dfs_weather)


def make_final_region_df(region_name: str):
    """
    Retorna o dataframe final combinando clima + carga para a região escolhida.
    """
    weather = process_weather_region(region_name)

    load_df = LOAD_MAP[region_name][['regiao', 'carga(MWmed)']].reset_index(drop=True)

    final_df = pd.concat(
        [weather.reset_index(drop=True), load_df],
        axis=1
    )
    return final_df

# Dataframes finais
df_sul = make_final_region_df('sul')
df_sudeste = make_final_region_df('sudeste')
df_norte = make_final_region_df('norte')
df_nordeste = make_final_region_df('nordeste')
