import streamlit as st
from st_constantes import DATA_PATH
from package.funciones import carga_de_datos

st.title("Análisis por cuenta")

# Cargamos la información
try:
    df = carga_de_datos()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

st.markdown("""
            En esta sección se puede explorar la información sobre SIGAF segun las **cuentas**.
            """)

