import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium import Choropleth
from pymongo import MongoClient

# Configuración de la página
st.set_page_config(page_title="Mapa", layout="wide")
st.title("🗺️ Mapa Interactivo - Víctimas por Departamento")

# Conexión a MongoDB
client = MongoClient("mongodb+srv://elianarm:20062004@cluster0.9daxwsg.mongodb.net/?retryWrites=true&w=majority")
db = client["Proy1_Dataviz_Mongo"]
collection = db["hechos_victimizantes_col"]

# Filtro lateral de año
st.sidebar.header("Filtros")
años = sorted(collection.distinct("Ano"))
año_sel = st.sidebar.selectbox("Selecciona un año para el mapa", años)

# Consultar solo los datos de ese año
data = pd.DataFrame(list(collection.find(
    {"Ano": año_sel},
    {"_id": 0}
)))

# Asegurar nombres en mayúsculas y limpiar datos
data["DEPARTAMENTO_OCU"] = data["DEPARTAMENTO_OCU"].str.upper()
data = data[data["DEPARTAMENTO_OCU"].notna()]
data["Ano"] = data["Ano"].astype(int)

# Agrupar por departamento
mapa_data = (
    data.groupby("DEPARTAMENTO_OCU")["total"]
    .sum()
    .reset_index()
)

# Leer GeoJSON de Colombia
colombia_geo = gpd.read_file("https://raw.githubusercontent.com/lihkir/Uninorte/main/AppliedStatisticMS/DataVisualizationRPython/Lectures/Python/PythonDataSets/Colombia.geo.json")

# Unir datos del CSV con el mapa
colombia_geo_merged = colombia_geo.merge(
    mapa_data, left_on="NOMBRE_DPT", right_on="DEPARTAMENTO_OCU", how="left"
)
colombia_geo_merged["total"] = colombia_geo_merged["total"].fillna(0)

# Crear mapa base
centro = [4.5709, -74.2973]
m = folium.Map(location=centro, zoom_start=5.2)

# Agregar coropletas
Choropleth(
    geo_data=colombia_geo_merged.__geo_interface__,
    data=colombia_geo_merged,
    columns=["NOMBRE_DPT", "total"],
    key_on="feature.properties.NOMBRE_DPT",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Número de Víctimas"
).add_to(m)

# Agregar etiquetas de cantidad en los departamentos
for _, row in colombia_geo_merged.iterrows():
    if row["total"] > 0:
        folium.Marker(
            location=[row["geometry"].centroid.y, row["geometry"].centroid.x],
            icon=None,
            popup=f"{row['NOMBRE_DPT']}: {int(row['total'])} víctimas"
        ).add_to(m)

# Mostrar mapa en Streamlit
st_folium(m, width=1000, height=550)
