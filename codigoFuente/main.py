import os
import argparse
import sys
import pandas as pd
import mysql.connector
import getpass
from modelos.viento_solar import VientoSolar, VientoSolarDetector
from modelos.graficar import graficar_datos
sys.path.append('./../data')
from data_loader import cargar_datos

def main():
    """
    Función principal
    """
    #Solicitar al usuario que ingrese la contraseña de MySQL
    contrasenia = getpass.getpass("Ingrese la contrasenia de MySQL: ")
    
    #Establecer la variable de entorno con la contraseña
    os.environ["DB_PSSWORD"] = contrasenia

    #Establecer la conexión a la base de datos
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        raise ValueError("La variable de entorno DB_PASSWORD no está configurada. Es necesaria para conectarse con MySQL. Por favor, defínala")

    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="viento_solar_db",
	allow_local_infile=True
    )
    #Configurando argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Procesamiento y análisisd de datos de viento solar")
    parser.add_argument("txt_file", type=str, help="Ingrese la ruta del archivo .txt con los datos de viento solar")
    args = parser.parse_args()

    #Verificación de existencia del archivo
    if not os.path.exists(args.txt_file):
        print(f"Error: El archivo {args.txt_file} no existe")
        return
    
    #Definir el archivo CSV de salida
    csv_file = "./../data/viento_solar.csv"

    #Cargar datos y convertir a SQL
    cargar_datos(args.txt_file, csv_file)

    print(f"Datos procesados y guardados en {csv_file}. Generando gráficos...")
    #Llamar a la función para graficar los datos
    graficar_datos(csv_file) 

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
