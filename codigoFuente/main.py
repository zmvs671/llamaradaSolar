import os
import sys
import pandas as pd
from modelos.viento_solar import VientoSolar, VientoSolarDetector
import mysql.connector
sys.path.append('./../data')
from data_loader import cargar_datos

def main():
    """
    Función principal
    """
    #Establecer la conexión a la base de datos
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        raise ValueError("La variable de entorno DB_PASSWORD no está configurada. Es necesaria para conectarse con MySQL. Por favor, defínala")

    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="viento_solar_db"
    )

    #Ruta de los archivos
    txt_file = "data/20240507_20240512.txt"
    csv_file = "data/viento_solar.csv"

    #Procesar el archivo .txt y cargar los datos a MySQL
    cargar_datos(txt_file, csv_file)

    #Cargar los datos desde el archivo .csv
    df = pd.read_csv(csv_file)

    #Crear el detector con los umbrales personalizados
    detector = VientoSolarDetector(umbral_velocidad=400, umbral_densidad=5)

    #Detectar los eventos de vientos solares
    eventos = detector.detectar_eventos(df)

    #Cargar los eventos detectados a la base de datos
    for _, row in eventos.iterrows():
        evento = VientoSolar(row['fecha'], row['plasma_temperature'], row['proton_density'], row['plasma_speed'])
        evento.guardar_en_sql(db_connection)

    #Cerrar la conexión a la base de datos
    db_connection.close()
    print("Proceso completado exitosamente.")

if __name__ == "__main__":
    main()
