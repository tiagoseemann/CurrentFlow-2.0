"""
Configuration constants for the energy analytics project.

This module contains mappings between Brazilian states and regions,
as well as other configuration parameters.
"""

from typing import Dict


# Mapping of Brazilian state codes to regions
# Used to aggregate weather data from INMET stations
STATE_TO_REGION: Dict[str, str] = {
    # Norte (N)
    'AC': 'Norte',      # Acre
    'AP': 'Norte',      # Amapá
    'AM': 'Norte',      # Amazonas
    'PA': 'Norte',      # Pará
    'RO': 'Norte',      # Rondônia
    'RR': 'Norte',      # Roraima
    'TO': 'Norte',      # Tocantins

    # Nordeste (NE)
    'AL': 'Nordeste',   # Alagoas
    'BA': 'Nordeste',   # Bahia
    'CE': 'Nordeste',   # Ceará
    'MA': 'Nordeste',   # Maranhão
    'PB': 'Nordeste',   # Paraíba
    'PE': 'Nordeste',   # Pernambuco
    'PI': 'Nordeste',   # Piauí
    'RN': 'Nordeste',   # Rio Grande do Norte
    'SE': 'Nordeste',   # Sergipe

    # Sudeste/Centro-Oeste (SE)
    'ES': 'Sudeste/Centro-Oeste',  # Espírito Santo
    'MG': 'Sudeste/Centro-Oeste',  # Minas Gerais
    'RJ': 'Sudeste/Centro-Oeste',  # Rio de Janeiro
    'SP': 'Sudeste/Centro-Oeste',  # São Paulo
    'DF': 'Sudeste/Centro-Oeste',  # Distrito Federal
    'GO': 'Sudeste/Centro-Oeste',  # Goiás
    'MT': 'Sudeste/Centro-Oeste',  # Mato Grosso
    'MS': 'Sudeste/Centro-Oeste',  # Mato Grosso do Sul

    # Sul (S)
    'PR': 'Sul',        # Paraná
    'RS': 'Sul',        # Rio Grande do Sul
    'SC': 'Sul',        # Santa Catarina
}


def get_region_from_state(state_code: str) -> str:
    """
    Get the Brazilian region for a given state code.

    Args:
        state_code: Two-letter state code (e.g., 'SP', 'RJ')

    Returns:
        Region name ('Norte', 'Nordeste', 'Sudeste/Centro-Oeste', 'Sul')
        Returns 'Unknown' if state code is not found.

    Example:
        >>> get_region_from_state('SP')
        'Sudeste/Centro-Oeste'
        >>> get_region_from_state('BA')
        'Nordeste'
    """
    return STATE_TO_REGION.get(state_code.upper(), 'Unknown')


def extract_state_from_filename(filename: str) -> str:
    """
    Extract state code from INMET CSV filename.

    INMET filenames follow the pattern:
    INMET_REGION_STATE_CODE_CITY_DATE_A_DATE.CSV
    Example: INMET_SE_MG_A001_BELO_HORIZONTE_01-01-2023_A_31-12-2023.CSV

    Args:
        filename: INMET CSV filename

    Returns:
        Two-letter state code (e.g., 'MG', 'SP'), or 'UNKNOWN' if parsing fails

    Example:
        >>> extract_state_from_filename('INMET_SE_MG_A001_BELO_HORIZONTE_01-01-2023_A_31-12-2023.CSV')
        'MG'
    """
    try:
        parts = filename.split('_')
        if len(parts) >= 3:
            return parts[2]  # State code is the 3rd part (index 2)
    except Exception:
        pass
    return 'UNKNOWN'
