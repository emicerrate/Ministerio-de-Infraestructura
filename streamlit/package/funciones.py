import pandas as pd
from st_constantes import DATA_PATH

def carga_de_datos():
    """
    Carga los datos de la base de datos a un dataframe.
    Args:
        None.
    Returns:
        df (dataframe): Dataframe con toda la información de SIGAF.
    """
    file_path = DATA_PATH / "Base Consolidada 2.xlsx"
    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo \"Base Consolidada.xlsx\".")
    df = pd.read_excel(file_path, sheet_name="SIGAF")
    return df
