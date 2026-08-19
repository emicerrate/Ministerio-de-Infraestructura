import streamlit as st
from st_constantes import DATA_PATH
from package.funciones import carga_de_datos, conditions, coordenates, generar_mapa
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

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
cuenta = st.selectbox("Cuenta", cuentas, index=None)

if cuenta:
    try:
        # Filtro el dataframe por cuenta
        df_reducido = df[(df["Cuenta Unificada"] == cuenta)]

        st.subheader("Comparación partidas, Distribución por condición y Cantidad con coordenadas")

        # Creamos los tres gráficos
        fig, ax = plt.subplots(3, 1, figsize=(12, 18))
        
        # Gráfico 1
        values = df_reducido["Condición"].value_counts().values
        labels = df_reducido["Condición"].value_counts().index
        ax[0].pie(values, labels=labels, 
                  autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, p * sum(values) / 100))
        ax[0].set_title("COMPARACIÓN PARTIDAS")

        # Gráfico 2
        values2 = conditions(df_reducido)
        labels2 = ["Con partida", "Cáscara vacía"]
        ax[1].pie(values2, labels=labels2, colors=["green", "red"],
                  autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, p * sum(values2) / 100))
        ax[1].set_title("DISTRIBUCIÓN POR CONDICIÓN")
        
        # Gráfico 3
        values3 = coordenates(df_reducido)
        labels3 = ["Tienen coordenadas", "No tienen coordenadas"]
        ax[2].pie(values3, labels=labels3, colors=["green", "red"],
                  autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, p * sum(values2) / 100))
        ax[2].set_title("COMPARACIÓN COORDENADAS")

        # Ajustamos los gráficos y los mostramos
        fig.tight_layout()
        st.pyplot(fig)

        # Mapa para las partidas con coordenadas
        st.subheader("Mapa con las coordenadas")
        mapa = generar_mapa()
        st_folium(mapa)
    except:
        st.warning("No existe información para la cuenta seleccionada.")
