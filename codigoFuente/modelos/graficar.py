import pandas as pd
import matplotlib.pyplot as plt

def graficar_datos(csv_file):
    """Genera gráficos de velocidad, densidad y temperatura del viento solar"""
    df = pd.read_csv(csv_file)

    #Convertir fecha a formato datetime
    df["fecha"] = pd.to_datetime(df["fecha"])

    #Crear la figura y los subgráficos
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    #Graficar Velocidad del Viento Solar
    axes[0].plot(df["fecha"], df["plasma_speed"], label="Velocidad", color="blue")
    axes[0].set_ylabel("Velocidad (km/s)")
    axes[0].legend()
    
    #Graficar Densidad del Viento Solar
    axes[1].plot(df["fecha"], df["proton_density"], label="Densidad", color="green")
    axes[1].set_ylabel("Densidad (cm³)")
    axes[1].legend()
    
    #Graficar Temperatura del Viento Solar
    axes[2].plot(df["fecha"], df["plasma_temperature"], label="Temperatura", color="red")
    axes[2].set_ylabel("Temperatura (K)")
    axes[2].set_xlabel("Fecha")
    axes[2].legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
