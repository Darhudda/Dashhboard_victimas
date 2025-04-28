import pandas as pd
from pymongo import MongoClient

# Conectarse a MongoDB Atlas
client = MongoClient("mongodb+srv://elianarm:20062004@cluster0.9daxwsg.mongodb.net/?retryWrites=true&w=majority")

# Base nueva: Proy1_Dataviz_Mongo
# Colección (dataset): hechos_victimizantes_col
db = client["Proy1_Dataviz_Mongo"]
collection = db["hechos_victimizantes_col"]

# Leer el CSV
df = pd.read_csv("hechos_victimizantes_col.csv", encoding="latin-1")

# Convertir y subir
data = df.to_dict(orient="records")
collection.insert_many(data)

print("Dataset insertado correctamente en 'Proy1_Dataviz_Mongo.hechos_victimizantes_col'")
