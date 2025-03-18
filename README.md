# llamaradaSolar
**Autor:** Silvia Viridiana Maldonado Zamora

# Detector de eventos de viento solar  

Este proyecto analiza datos de viento solar, detectando eventos significativos basados en umbrales de velocidad y densidad de plasma. Se utilizan datos en formato `.txt` extraídos de [OMNIWeb Data Explorer](https://omniweb.gsfc.nasa.gov/form/dx1.html) los cuales son procesados y almacenados en una base de datos MySQL, además de mostrar de manera gráfica la variación de la Temperatura de plasma $[K]$, Densidad de protones $[N/cm^3]$ y Velocidad de plasma $[km/s]$ a través de la escala temporal.

## Acciones
- Procesa archivos `.txt` de viento solar y los convierte a `.csv`.  
- Almacena los datos en una base de datos MySQL.  
- Detecta eventos de viento solar basados en umbrales de velocidad y densidad.  

## Instalación
- Se recomienda crear un entorno virtual antes de instalar los paquetes.
- Ejecute el archivo `requeriments.txt` de la siguiente manera:
  pip install -r requirements.txt
- Asegúrese de tener MySQL instalado
- Cree la base de datos `viento_solar_db` en MySQL con:
  CREATE DATABASE viento_solar_db;
- Ejecute la siguiente línea en MySQL desde terminal para permitir que la base se actualice:
  SET GLOBAL local_infile = 1;

## Ejecución
- Previo a la ejecución, configure la variable de entorno DB_PASSWORD con su contraseña de MySQL de la siguiente manera
  export DB_PASSWORD="escriba_su_contraseña"
- Ejecute en su terminal el script `main.py` indicando la ruta del archivo `.txt` que contiene los datos, de la siguiente manera:
  python3 main.py `.\ruta\archivo.txt`
