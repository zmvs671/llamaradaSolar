class VientoSolar:
    """
    Clase para representar un evento de viento solar y almacenar los datos en una base de datos
    def __init__(self, fecha, temperatura_viento, densidad_viento, velocidad_viento):
        """
        Inicializa la clase VientoSolar con los datos de un evento
        Argumentos:
            fecha(datetime): Fecha y hora del evento
            temperatura_viento(float): Temperatura del viento solar
            densidad_viento(float): Densidad del viento solar
            velocidad_viento(float): Velocidad del viento solar
        """
        self.fecha = fecha
        self.temperatura_viento = temperatura_viento
        self.densidad_viento = densidad_viento
        self.velocidad_viento = velocidad_viento

    def guardar_en_sql(self, db_connection):
        """
        Guarda un evento de viento solar en la base de datos MySQL.
        Argumentos:
            db_connection: Conexión a la base de datos MySQL.
        """
        cursor = db_connection.cursor()
        cursor.execute("""
            INSERT INTO viento_solar (fecha, temperatura_viento, densidad_viento, velocidad_viento)
            VALUES (%s, %s, %s, %s)
        """, (self.fecha, self.temperatura_viento, self.densidad_viento, self.velocidad_viento))
        db_connection.commit()
        cursor.close()
        print(f"Evento de viento solar guardado: {self.fecha}")

class VientoSolarDetector:
    """
    Clase para detectar eventos significativos de viento solar a partir de datos de la actividad solar.
    Atributos:
        umbral_velocidad (float): Umbral de velocidad para considerar un evento significativo.
        umbral_densidad (float): Umbral de densidad para considerar un evento significativo.
    """

    def __init__(self, umbral_velocidad, umbral_densidad):
        """
        Inicializa la clase VientoSolarDetector con los umbrales.
        Argumentos:
            umbral_velocidad(float): Umbral de velocidad.
            umbral_densidad(float): Umbral de densidad.
        """
        self.umbral_velocidad = umbral_velocidad
        self.umbral_densidad = umbral_densidad

    def detectar_eventos(self, df):
        """
        Detecta eventos de viento solar significativos en el DataFrame proporcionado.
        Argumentos:
            df (pd.DataFrame): DataFrame con los datos de viento solar.
        Regresa:
            pd.DataFrame: DataFrame con los eventos detectados.
        """
        eventos = df[(df['velocidad_viento'] > self.umbral_velocidad) & 
                     (df['densidad_viento'] > self.umbral_densidad)]
        return eventos

