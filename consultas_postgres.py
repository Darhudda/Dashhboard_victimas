import pandas as pd
from sqlalchemy import create_engine

# Datos de conexión a PostgreSQL
usuario = "postgres"
contraseña = "20062004"
host = "localhost"
puerto = "5432"
base_datos = "dataviz_db"

# Crear motor de conexión
engine = create_engine(f"postgresql+psycopg2://{usuario}:{contraseña}@{host}:{puerto}/{base_datos}")

# 1. Total de documentos (registros)
query_total = "SELECT COUNT(*) AS total_registros FROM datos_csv;"
df_total = pd.read_sql(query_total, engine)
print("\nTotal de documentos (hechos):")
print(df_total)

# 2. Top 5 hechos con más víctimas
query_top_hechos = """
SELECT "HECHO", SUM("total") AS total_victimas
FROM datos_csv
GROUP BY "HECHO"
ORDER BY total_victimas DESC
LIMIT 5;
"""
df_top_hechos = pd.read_sql(query_top_hechos, engine)
print("\nTop 5 hechos con más víctimas:")
print(df_top_hechos)

# 3. Total de víctimas por año
query_victimas_ano = """
SELECT "Ano", SUM("total") AS total_victimas
FROM datos_csv
GROUP BY "Ano"
ORDER BY "Ano" ASC;
"""
df_victimas_ano = pd.read_sql(query_victimas_ano, engine)
print("\nVíctimas por año:")
print(df_victimas_ano)

# 4. Top 10 departamentos con más víctimas
query_victimas_dpto = """
SELECT "DEPARTAMENTO_OCU", SUM("total") AS total_victimas
FROM datos_csv
GROUP BY "DEPARTAMENTO_OCU"
ORDER BY total_victimas DESC
LIMIT 10;
"""
df_victimas_dpto = pd.read_sql(query_victimas_dpto, engine)
print("\nTop 10 departamentos con más víctimas:")
print(df_victimas_dpto)

# 5. Distribución por tipo de desplazamiento
query_tipo_desplazamiento = """
SELECT "TIPO_DESPLAZAMIENTO", COUNT(*) AS conteo
FROM datos_csv
GROUP BY "TIPO_DESPLAZAMIENTO"
ORDER BY conteo DESC;
"""
df_tipo_desplazamiento = pd.read_sql(query_tipo_desplazamiento, engine)
print("\nDistribución por tipo de desplazamiento:")
print(df_tipo_desplazamiento)

# 6. Top 5 municipios con más víctimas
query_top_municipios = """
SELECT "MUNICIPIO_OCU", SUM("total") AS total_victimas
FROM datos_csv
GROUP BY "MUNICIPIO_OCU"
ORDER BY total_victimas DESC
LIMIT 5;
"""
df_top_municipios = pd.read_sql(query_top_municipios, engine)
print("\nTop 5 municipios con más víctimas:")
print(df_top_municipios)

# 7. Top 5 hechos con más víctimas en 2020
query_top_hechos_2020 = """
SELECT "HECHO", SUM("total") AS total_victimas
FROM datos_csv
WHERE "Ano" = 2020
GROUP BY "HECHO"
ORDER BY total_victimas DESC
LIMIT 5;
"""
df_top_hechos_2020 = pd.read_sql(query_top_hechos_2020, engine)
print("\nTop 5 hechos con más víctimas en 2020:")
print(df_top_hechos_2020)
