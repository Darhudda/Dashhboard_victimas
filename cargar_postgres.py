import pandas as pd
from sqlalchemy import create_engine

# Carga el archivo CSV (ajusta el nombre al tuyo)
df = pd.read_csv("hechos_victimizantes_col.csv", encoding='latin-1')
print("Primeros registros del archivo:")
print(df.head())

# Datos de conexión a PostgreSQL
usuario = "postgres"
contraseña = "20062004"  # pon la contraseña que configuraste
host = "localhost"
puerto = "5432"
base_datos = "dataviz_db"

# Crear el motor de conexión
engine = create_engine(f"postgresql+psycopg2://{usuario}:{contraseña}@{host}:{puerto}/{base_datos}")

# Cargar el dataframe a PostgreSQL
df.to_sql("datos_csv", engine, if_exists="replace", index=False)
print("\nDatos insertados correctamente en la tabla 'datos_csv'.")
