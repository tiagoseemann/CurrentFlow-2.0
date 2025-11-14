from pathlib import Path

DATA_DIR = Path(r"C:\Users\guica\OneDrive\Documentos\GitHub\CurrentFlow-2.0\data\raw\inmet")

REGIONS = {
    "norte": [
        DATA_DIR / "dados_belem_A201_D.csv",
        DATA_DIR / "dados_manaus_A101_D.csv",
        DATA_DIR / "dados_porto_velho_A925_D.csv",
    ],
    "nordeste": [
        DATA_DIR / "dados_fortaleza_A305_D.csv",
        DATA_DIR / "dados_salvador_A401_D.csv",
    ],
    "sudeste": [
        DATA_DIR / "dados_sao_paulo_A771_D.csv",
        DATA_DIR / "dados_rio_de_janeiro_A621_D.csv",
        DATA_DIR / "dados_belo_horizonte_A521_D.csv",
    ],
    "sul": [
        DATA_DIR / "dados_florianopolis_A806_D.csv",
        DATA_DIR / "dados_curitiba_A807_D.csv",
        DATA_DIR / "dados_porto_alegre_A801_D.csv",
    ],
}


"""
Norte:      Manaus - Belém - Porto Velho
Nordeste:   Fortaleza - Salvador
Sul:        Porto Alegre (Jardim botânico) - Curitiba - Florianópolis
Sudeste:    São Paulo (Interlagos) - Rio de Janeiro (Vila Militar) - Belo Horizonte (Pampulha)
"""
