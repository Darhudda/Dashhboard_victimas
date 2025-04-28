import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from pymongo import MongoClient
from PIL import Image

# Conexión a MongoDB
client = MongoClient("mongodb+srv://elianarm:20062004@cluster0.9daxwsg.mongodb.net/?retryWrites=true&w=majority")
db = client["Proy1_Dataviz_Mongo"]
collection = db["hechos_victimizantes_col"]

# Leer una pequeña muestra de datos
data = pd.DataFrame(list(collection.find({}, {"_id": 0}).limit(5)))

# Configuración de la app
st.set_page_config(page_title="Dashboard Hechos Victimizantes", layout="wide")

# Menú lateral
with st.sidebar:
    selected = option_menu("Menú", ["Inicio", "Mapa", "Dashboard", "Consultas"],
        icons=["house", "geo-alt", "bar-chart", "database"], menu_icon="cast", default_index=0)

# Página de Inicio
if selected == "Inicio":
    st.title("Diagnóstico Exploratorio sobre hechos victimizantes en Colombia")
    
    # Imagen alusiva
    imagen = Image.open("victimas.jpg")  # Asegúrate que la imagen exista en tu carpeta
    st.image(imagen, caption="Fuente: Unidad para las Víctimas", use_container_width=True)

    st.markdown("""
    ### Propósito del Proyecto

    Este proyecto busca analizar los hechos victimizantes reportados en Colombia en el contexto del conflicto armado interno, explorando su distribución en el tiempo y en el espacio geográfico.

    ---

    ### Descripción del conjunto de datos

    El conjunto de datos *hechos_victimizantes_col* contiene registros detallados de hechos de violencia reportados oficialmente, incluyendo:
    - Tipo de hecho victimizante (desplazamiento forzado, homicidio, amenaza, etc.).
    - Departamento y municipio de ocurrencia.
    - Año y mes del evento.
    - Número total de víctimas.
    - Tipo de desplazamiento, en los casos aplicables.

    Este análisis pretende contribuir a la memoria histórica y a la formulación de políticas públicas para la atención y reparación de víctimas.

    ---
    """)

    st.markdown("### Vista preliminar de la base de datos:")
    st.dataframe(data)

    st.info("Utiliza el menú de la izquierda para acceder al **Mapa Interactivo**, al **Dashboard de Análisis** o a las **Consultas específicas** sobre los datos.")

# Página Mapa
elif selected == "Mapa":
    st.switch_page("pages/1_Mapa.py")

# Página Dashboard
elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")

# Página Consultas Mongo
elif selected == "Consultas":
    st.switch_page("pages/3_Consultas_Mongo.py")

# Página Consultas Postgres
elif selected == "Consultas":
    st.switch_page("pages/4_Consultas_Postgres.py")