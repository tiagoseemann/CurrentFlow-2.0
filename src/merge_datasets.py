import numpy as np
import pandas as pd
from prepare_load_data import load_regions
from weather_utils.get_weather import load_inmet, select_columns
from weather_utils.process_weather import standardize, fix_commas, merge_region
from weather_utils.regions import REGIONS, DATA_DIR

load_sul, load_se, load_norte, load_ne = load_regions()

dfs_weather_sul = []

for path in REGIONS['sul']:
    df = load_inmet(path=path)
    df = select_columns(df=df)
    df = standardize(df=df)
    df = fix_commas(df=df)
    dfs_weather_sul.append(df)

weather_sul = merge_region(dfs_weather_sul)

df = pd.concat(
    [weather_sul.reset_index(drop=True),
     load_sul[['regiao', 'carga(MWmed)']].reset_index(drop=True)],
    axis=1
)

print(df)