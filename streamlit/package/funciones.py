import pandas as pd
from st_constantes import DATA_PATH
import folium

def carga_de_datos():
    """
    Carga los datos de la base de datos a un dataframe.
    Args:
        None.
    Returns:
        df (dataframe): Dataframe con toda la información de SIGAF.
    """
    file_path = DATA_PATH / "Base Consolidada.xlsx"
    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo \"Base Consolidada.xlsx\".")
    df = pd.read_excel(file_path, sheet_name="SIGAF")
    return df

def conditions(df):
    """
    Separa las condiciones en partidas y cáscaras vacías.
    Args:
        df (dataframe): Dataframe con toda la información de SIGAF.
    Returns:
        values2 (list): Lista con los valores para el gráfico de distribución de partidas.
    """
    con_partida = {"Epecuén.", "Con partida.", "Partida repetida, esta es la madre.", "Partida repetida, esta es la agregación.", "Revisar. Son varias manzanas con varias partidas."}
    cantidad_con_partida = df["Condición"].isin(con_partida).sum()
    return [cantidad_con_partida, len(df) - cantidad_con_partida]

def coordenates(df):
    """
    Toma la cantidad de fichas que tienen y no tienen coordenadas.
    Args:
        df (dataframe): Dataframe con toda la información de SIGAF.
    Returns:
        values3 (list): Lista con los valores para el gráfico de distribución de coordenadas.
    """
    cantidad_con_coordenadas = df["Coordenadas"].count()
    return [cantidad_con_coordenadas, len(df) - cantidad_con_coordenadas]

def generar_mapa():
    """
    Genera el mapa para mostrar las fichas con coordenadas.
    Args:
        None.
    Returns:
        m (folium.Map): Mapa para las fichas con coordenadas.
    """
    attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    m = folium.Map(
        location=(-36.6769, -60.5588),
        control_scale=True,
        zoom_start=6,
        name='es',
        tiles=tiles,
        attr=attr
    )
    return m

def agregar_coordenadas(columna):
    """
    Agrega todas las coordenadas de una columna a un mapa.
    Args:
        columna (Series): Series con todas las coordenadas.
    Returns:
        mapa (folium.Map): Mapa donde estararán todas las fichas.
    """
    mapa = generar_mapa()
    for coord in columna:
        match coord:
            case "-":
                pass
            case _:
                coords = coord.split(",")
                folium.Marker(coords, popup=coord, icon=folium.Icon(color="green")).add_to(mapa)
    return mapa