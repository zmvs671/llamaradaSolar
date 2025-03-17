import os
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

def cargar_datos(txt_file, csv_file):
    """
    Procesa el archivo .txt, lo convierte a formato .csv y lo carga en la base de datos MySQL
    Argumentos:
        txt_file(str): Ruta del archivo .txt con los datos de viento solar
        csv_file(str): Ruta del archivo .csv donde se guardarán los datos procesados
    """
    #Verifica que la variable de entorno DB_PASSWORD esté configurada
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        raise ValueError("La variable de entorno DB_PASSWORD para usar SQL no está configurada. Establezca la variable de entorno antes de ejecutar el código.")

    #Leer el archivo .txt con pandas separando por espacios
    df = pd.read_csv(txt_file, delim_whitespace=True)

    #Definir nombres de columnas
    df.columns = ["year", "day_of_year", "hour_of_day", "plasma_temperature", "proton_density", "plasma_speed"]

    #Convertir la fecha en formato YYYY-MM-DD HH:MM:SS
    df['fecha'] = df.apply(lambda row: datetime(int(row["year"]), 1, 1) + timedelta(days=int(row["day_of_year"]) - 1, hours=int(row["hour_of_day"])), axis=1)

    #Guardar DataFrame como .csv
    df = df[["fecha", "plasma_temperature", "proton_density", "plasma_speed"]]
    df.to_csv(csv_file, index=False)

    print("Archivo .csv generado exitosamente.")

    #Cargar el archivo .csv a MySQL
    cargar_a_sql(csv_file, db_password)

def cargar_a_sql(csv_file, db_password):
    """
    Carga los datos desde un archivo .csv a la base de datos MySQL
    Argumentos
        csv_file(str): Ruta del archivo .csv que contiene los datos
        db_password(str): Contraseña de la base de datos MySQL
    """
    #Conexión a la base de datos MySQL
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="viento_solar_db",
	allow_local_infile=True
    )

    cursor = db_connection.cursor()

    #Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viento_solar (
            fecha DATETIME,
            plasma_temperature FLOAT,
            proton_density FLOAT,
            plasma_speed FLOAT
        )
    """)

    #Cargar los datos desde el archivo .csv a MySQL
    load_sql = """
        LOAD DATA LOCAL INFILE '""" + csv_file + """'
        INTO TABLE viento_solar
        FIELDS TERMINATED BY ',' 
        LINES TERMINATED BY '\\n'
        IGNORE 1 ROWS
        (fecha, plasma_temperature, proton_density, plasma_speed)
    """

    cursor.execute(load_sql)
    db_connection.commit()

    print("Datos cargados a MySQL exitosamente")

    #Cerrar la conexión
    cursor.close()
    db_connection.close()

