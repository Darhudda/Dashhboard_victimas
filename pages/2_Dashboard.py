import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Conexión a MongoDB Atlas
client = MongoClient("mongodb+srv://elianarm:20062004@cluster0.9daxwsg.mongodb.net/?retryWrites=true&w=majority")
db = client["Proy1_Dataviz_Mongo"]
collection = db["hechos_victimizantes_col"]

# Cargar datos
data = pd.DataFrame(list(collection.find()))
data["_id"] = data["_id"].astype(str)

# Configuración de página
st.set_page_config(page_title="Dashboard Hechos Victimizantes", layout="wide")
st.title("📊 Dashboard de Hechos Victimizantes en Colombia")
st.markdown("---")

# === KPIs Interactivos ===
col1, col2, col3 = st.columns(3)

with col1:
    total_victimas = int(data["total"].sum())
    st.metric(label="🔢 Total de Víctimas", value=f"{total_victimas:,}")

with col2:
    total_hechos = data["HECHO"].nunique()
    st.metric(label="📌 Tipos de Hechos", value=total_hechos)

with col3:
    total_departamentos = data["DEPARTAMENTO_OCU"].nunique()
    st.metric(label="🌐 Departamentos Afectados", value=total_departamentos)

# === Gráfico Top 5 hechos victimizantes (MongoDB) ===
top_hechos_mongo = collection.aggregate([
    {"$group": {"_id": "$HECHO", "total": {"$sum": "$total"}}},
    {"$sort": {"total": -1}},
    {"$limit": 5}
])
df_top_hechos = pd.DataFrame(top_hechos_mongo).rename(columns={"_id": "HECHO"})

st.subheader("🏆 Top 5 Hechos Victimizantes (MongoDB)")
fig_top_hechos = px.bar(df_top_hechos, x="total", y="HECHO", orientation="h",
                        color="HECHO", labels={"total": "Total de Víctimas"},
                        height=400)
st.plotly_chart(fig_top_hechos, use_container_width=True)

# === Filtro de año ===
st.sidebar.header("Filtros")
años = sorted(data["Ano"].dropna().unique())
año_sel = st.sidebar.selectbox("Selecciona un año", años)
data_filtrada = data[data["Ano"] == año_sel]

# === Gráficos en línea: hechos y departamentos ===
col4, col5 = st.columns(2)

with col4:
    top_hechos_ano = data_filtrada.groupby("HECHO")["total"].sum().sort_values(ascending=True).tail(5)
    st.subheader(f"Top 5 hechos victimizantes en {año_sel}")
    fig = px.bar(top_hechos_ano, x=top_hechos_ano.values, y=top_hechos_ano.index,
                 orientation="h", labels={"x": "Víctimas", "y": "HECHO"})
    st.plotly_chart(fig, use_container_width=True)

with col5:
    top_departamentos = data_filtrada.groupby("DEPARTAMENTO_OCU")["total"].sum().sort_values(ascending=False).head(5)
    st.subheader(f"Top 5 departamentos con más víctimas en {año_sel}")
    fig = px.bar(top_departamentos, x=top_departamentos.index, y=top_departamentos.values,
                 labels={"x": "Departamento", "y": "N° de víctimas"})
    st.plotly_chart(fig, use_container_width=True)

# === Gráficos en línea: desplazamiento y municipios ===
col6, col7 = st.columns(2)

with col6:
    desplazamiento_tipo = data_filtrada.groupby("TIPO_DESPLAZAMIENTO")["total"].sum().sort_values(ascending=False)
    st.subheader(f"Distribución por tipo de desplazamiento en {año_sel}")
    fig = px.pie(names=desplazamiento_tipo.index, values=desplazamiento_tipo.values)
    st.plotly_chart(fig, use_container_width=True)

with col7:
    top_municipios = data_filtrada.groupby("MUNICIPIO_OCU")["total"].sum().sort_values(ascending=False).head(5)
    st.subheader(f"Top municipios con más víctimas en {año_sel}")
    fig = px.bar(top_municipios, x=top_municipios.index, y=top_municipios.values,
                 labels={"x": "Municipio", "y": "N° de víctimas"})
    st.plotly_chart(fig, use_container_width=True)

# === Serie de tiempo ===
st.subheader("📈 Serie de Tiempo: Víctimas Totales por Año")
serie = data.groupby("Ano")["total"].sum().reset_index()
serie = serie[pd.to_numeric(serie["Ano"], errors="coerce").notnull()]
serie["Ano"] = serie["Ano"].astype(int)
serie = serie.sort_values("Ano")
fig = px.line(serie, x="Ano", y="total", markers=True, labels={"Ano": "Año", "total": "Total de Víctimas"})
st.plotly_chart(fig, use_container_width=True)