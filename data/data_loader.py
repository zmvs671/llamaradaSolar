import os
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

#Verificar que la variable de entorno esté configurada
db_password = os.getenv("DB_PASSWORD")

if not db_password:
	raise ValueError("La variable de entorno DB_PASSWORD para usar SQL no está configurada.Establezca la variable de entorno antes de ejecutar el código.")

#Procesamiento del archivo .txt de los datos originales y convertirlo a .csv
txt_file = "data/20240507_20240512.txt"
csv_file = "data/viento_solar.csv"

#Leer el archivo .txt, saltando las líneas de encabezado y separando por espacios
df = pd.read_csv(txt_file, delim_whitespace=True, header=None)

#Definir nombres de columnas
df.columns = ["year", "dayOfYear", "houOfDay", "plasmaTemperature", "protonDensity", "plasmaSpeed"]

#Convertir la fecha en formato YYYY-MM-DD HH:MM:SS
df['fecha'] = df.apply(lambda row: datetime(row["year"], 1, 1) + timedelta(days=row["dayOfYear"] - 1, hours=row["hour"]), axis=1)

#Guardar DataFrame como .csv
df = df[["fecha", "solarWindSpeed", "solarWindDensity", "solarWindTemperature"]
df.to_csv(csv_file, index=False)

print("Archivo .csv generado exitosamente.")

#Cargar el archivo .csv a MySQL

#Conexión a la base de datos MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database="viento_solar_db"
)

cursor = db_connection.cursor()

#Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS viento_solar (
        fecha DATETIME,
        plasmaTemperature FLOAT,
        protonDensity FLOAT,
        plasmaSpeed FLOAT
    )
""")

#Cargar los datos desde el archivo csv a MySQL 
load_sql = """
    LOAD DATA LOCAL INFILE '""" + csv_file + """'
    INTO TABLE viento_solar
    FIELDS TERMINATED BY ',' 
    LINES TERMINATED BY '\\n'
    IGNORE 1 ROWS
    (fecha, plasmaTemperature, protonDensity, plasmaSpeed)
"""

cursor.execute(load_sql)
db_connection.commit()

print("Datos cargados a MySQL exitosamente.")

#Cerrar la conexión
cursor.close()
db_connection.close()

