#llamaradaSolar

#Detector de eventos de viento solar  

Este proyecto analiza datos de viento solar, detectando eventos significativos basados en umbrales de velocidad y densidad. Se utilizan datos en formato `.txt`, los cuales son procesados y almacenados en una base de datos MySQL.

##Acciones
- Procesa archivos `.txt` de viento solar y los convierte a `.csv`.  
- Almacena los datos en una base de datos MySQL.  
- Detecta eventos de viento solar basados en umbrales de velocidad y densidad.  

##Instalación
- Se recomienda crear un entorno virtual antes de instalar los paquetes.
- Ejecute el archivo `requeriments.txt` de la siguiente manera:
  pip install -r requirements.txt
- Asegúrese de tener MySQL instalado y en ejecución.
- Previo a la ejecución, configure la variable de entorno DB_PASSWORD con su contraseña de MySQL de la siguiente manera
  export DB_PASSWORD="escriba_su_contraseña"

##Ejecución
Ejecute en su terminal los scripts `data_loader.py` y `main.py` en ese orden, de la siguiente manera: 
  python3 data_loader.py
  python3 main.py
