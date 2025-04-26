from pymongo import MongoClient

# Conexión a MongoDB Atlas
client = MongoClient("mongodb+srv://elianarm:20062004@cluster0.9daxwsg.mongodb.net/?retryWrites=true&w=majority")
db = client["Proy1_Dataviz_Mongo"]
collection = db["hechos_victimizantes_col"]

# 1. Total de documentos
total_docs = collection.count_documents({})
print(f"Total de documentos (hechos): {total_docs}")

# 2. Top 5 hechos con más víctimas
print("\nTop 5 hechos con más víctimas:")
top_hechos = collection.aggregate([
    {"$group": {"_id": "$HECHO", "total_victimas": {"$sum": "$total"}}},
    {"$sort": {"total_victimas": -1}},
    {"$limit": 5}
])
for h in top_hechos:
    print(f"{h['_id']}: {h['total_victimas']} víctimas")

# 3. Total de víctimas por año
print("\nVíctimas por año:")
victimas_ano = collection.aggregate([
    {"$group": {"_id": "$Ano", "total_victimas": {"$sum": "$total"}}},
    {"$sort": {"_id": 1}}
])
for a in victimas_ano:
    print(f"{a['_id']}: {a['total_victimas']} víctimas")

# 4. Top 10 departamentos con más víctimas
print("\nTop 10 departamentos con más víctimas:")
victimas_dpto = collection.aggregate([
    {"$group": {"_id": "$DEPARTAMENTO_OCU", "total_victimas": {"$sum": "$total"}}},
    {"$sort": {"total_victimas": -1}},
    {"$limit": 10}
])
for d in victimas_dpto:
    print(f"{d['_id']}: {d['total_victimas']} víctimas")

# 5. Distribución por tipo de desplazamiento
print("\nDistribución por tipo de desplazamiento:")
desplazamiento = collection.aggregate([
    {"$group": {"_id": "$TIPO_DESPLAZAMIENTO", "conteo": {"$sum": 1}}},
    {"$sort": {"conteo": -1}}
])
for t in desplazamiento:
    print(f"{t['_id']}: {t['conteo']} registros")

# 6. Top 5 municipios con más víctimas
print("\nTop 5 municipios con más víctimas:")
top_municipios = collection.aggregate([
    {"$group": {"_id": "$MUNICIPIO_OCU", "total_victimas": {"$sum": "$total"}}},
    {"$sort": {"total_victimas": -1}},
    {"$limit": 5}
])
for m in top_municipios:
    print(f"{m['_id']}: {m['total_victimas']} víctimas")


# 7. Filtrar por hechos del año 2020
print("\nTop 5 hechos con más víctimas en 2020:")
top_hechos_2020 = collection.aggregate([
    {"$match": {"Ano": 2020}},  # <- filtro aplicado aquí
    {"$group": {"_id": "$HECHO", "total_victimas": {"$sum": "$total"}}},
    {"$sort": {"total_victimas": -1}},
    {"$limit": 5}
])
for h in top_hechos_2020:
    print(f"{h['_id']}: {h['total_victimas']} víctimas")

