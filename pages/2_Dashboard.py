import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Conexión a MongoDB Atlas
client = MongoClient("mongodb+srv://elianarm:20062004@cluster0.9daxwsg.mongodb.net/?retryWrites=true&w=majority")
db = client["Proy1_Dataviz_Mongo"]
collection = db["hechos_victimizantes_col"]

# Configuración de página
st.set_page_config(page_title="Dashboard Hechos Victimizantes", layout="wide")
st.title("Dashboard de Hechos Victimizantes en Colombia")
st.markdown("---")

# Sidebar para filtros
st.sidebar.header("Filtros")
años = sorted(collection.distinct("Ano"))
año_sel = st.sidebar.selectbox("Selecciona un año para el dashboard", años)

# Cargar solo los datos del año seleccionado
data = pd.DataFrame(list(collection.find(
    {"Ano": año_sel},
    {"_id": 0}
)))

# Crear data_filtrada (para que funcione todo después)
data_filtrada = data.copy()

# === KPIs Mejorados en Tarjetas ===
col1, col2, col3 = st.columns(3)

# === KPIs Mejorados en Tarjetas ===
col1, col2, col3 = st.columns(3)

with col1:
    total_victimas = 12,853,357 
    st.markdown(f"""
    <div style="background-color: #4A90E2; padding: 15px; border-radius: 10px; text-align: center;">
        <p style="color: white; font-size:16px; margin:0;">Total de Víctimas</p>
        <p style="color: white; font-size:22px; font-weight:bold; margin:0;">{total_victimas:,}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_hechos = 16
    st.markdown(f"""
    <div style="background-color: #F5A623; padding: 15px; border-radius: 10px; text-align: center;">
        <p style="color: white; font-size:16px; margin:0;">Tipos de Hechos</p>
        <p style="color: white; font-size:22px; font-weight:bold; margin:0;">{total_hechos}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_departamentos = 33
    st.markdown(f"""
    <div style="background-color: #7ED321; padding: 15px; border-radius: 10px; text-align: center;">
        <p style="color: white; font-size:16px; margin:0;">Departamentos Afectados</p>
        <p style="color: white; font-size:22px; font-weight:bold; margin:0;">{total_departamentos}</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------------------------
# Filtro adicional de hecho victimizante
hechos = ["General"] + sorted(data["HECHO"].dropna().unique())
hecho_sel = st.sidebar.selectbox("Selecciona un hecho victimizante (o General)", hechos, key="filtro_hecho")

# === Gráficos principales ===
col4, col5 = st.columns(2)

# === Serie de tiempo con filtro por hecho victimizante ===
with col4:
    
    # Aquí usamos toda la colección sin filtrar por año_sel
    if hecho_sel == "General":
        serie = pd.DataFrame(list(collection.aggregate([
            {"$group": {"_id": "$Ano", "total": {"$sum": "$total"}}},
            {"$sort": {"_id": 1}}
        ])))
        serie.rename(columns={"_id": "Ano"}, inplace=True)
    else:
        serie = pd.DataFrame(list(collection.aggregate([
            {"$match": {"HECHO": hecho_sel}},
            {"$group": {"_id": "$Ano", "total": {"$sum": "$total"}}},
            {"$sort": {"_id": 1}}
        ])))
        serie.rename(columns={"_id": "Ano"}, inplace=True)

    # Limitar hasta el año 2025
    serie = serie[pd.to_numeric(serie["Ano"], errors="coerce").notnull()]
    serie["Ano"] = serie["Ano"].astype(int)
    serie = serie[serie["Ano"] <= 2025]

    # Gráfico
    fig = px.line(serie, x="Ano", y="total", markers=True,
                  labels={"Ano": "Año", "total": "Total de Víctimas"},
                  title=f"Serie de Tiempo - {hecho_sel}")
    st.plotly_chart(fig, use_container_width=True)



with col5:
    top_hechos_mongo = collection.aggregate([
        {"$group": {"_id": "$HECHO", "total": {"$sum": "$total"}}},
        {"$sort": {"total": -1}},
        {"$limit": 5}
    ])
    df_top_hechos = pd.DataFrame(top_hechos_mongo).rename(columns={"_id": "HECHO"})

    st.subheader("Top 5 Hechos Victimizantes")
    fig_top_hechos = px.bar(df_top_hechos, x="total", y="HECHO", orientation="h",
                            color="HECHO", labels={"total": "Total de Víctimas"},
                            height=400)
    st.plotly_chart(fig_top_hechos, use_container_width=True)

# === Gráficos secundarios ===
col6, col7 = st.columns(2)

with col6:
    desplazamiento_tipo = data_filtrada.groupby("TIPO_DESPLAZAMIENTO")["total"].sum().sort_values(ascending=False)
    st.subheader(f"Distribución por tipo de desplazamiento en {año_sel}")
    fig = px.pie(names=desplazamiento_tipo.index, values=desplazamiento_tipo.values)
    st.plotly_chart(fig, use_container_width=True)

with col7:
    top_departamentos = data_filtrada.groupby("DEPARTAMENTO_OCU")["total"].sum().sort_values(ascending=False).head(5)
    st.subheader(f"Top 5 departamentos con más víctimas en {año_sel}")
    fig = px.bar(top_departamentos, x=top_departamentos.index, y=top_departamentos.values,
                 labels={"x": "Departamento", "y": "N° de víctimas"})
    st.plotly_chart(fig, use_container_width=True)

# === Gráficos desplazamiento y municipios ===
col8, col9 = st.columns(2)

with col8:
    top_hechos_ano = data_filtrada.groupby("HECHO")["total"].sum().sort_values(ascending=True).tail(5)
    st.subheader(f"Top 5 hechos victimizantes en {año_sel}")
    fig = px.bar(top_hechos_ano, x=top_hechos_ano.values, y=top_hechos_ano.index,
                 orientation="h", labels={"x": "Víctimas", "y": "HECHO"})
    st.plotly_chart(fig, use_container_width=True)


with col9:
    top_municipios = data_filtrada.groupby("MUNICIPIO_OCU")["total"].sum().sort_values(ascending=False).head(5)
    st.subheader(f"Top municipios con más víctimas en {año_sel}")
    fig = px.bar(top_municipios, x=top_municipios.index, y=top_municipios.values,
                 labels={"x": "Municipio", "y": "N° de víctimas"})
    st.plotly_chart(fig, use_container_width=True)