import streamlit as st
from st_constantes import DATA_PATH
from package.funciones import carga_de_datos
import matplotlib.pyplot as plt

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

# Elección de cuenta
cuentas = df["Cuenta Unificada"].unique()
cuenta = st.selectbox("Cuenta", cuentas)

if cuenta:
    try:
        df_reducido = df[(df["Cuenta Unificada"] == cuenta)]
        values = df["Condición"].value_counts().values
        labels = df["Condición"].value_counts().index
        # Gráfico 1
        st.subheader("Comparación partidas")
        plt.figure(figsize=(10, 5))
        plt.pie(values, labels=labels, autopct='%1.2f%%')
        plt.title("Comparación partidas")
        st.pyplot()

        # Gráfico 2
        st.subheader("Distribución por condición")
    except:
        st.warning("No existe información para la cuenta seleccionada.")
