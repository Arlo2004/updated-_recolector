import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from meteofrance_api import MeteoFranceClient
from datetime import datetime

# Tus 28 estaciones con LAT, LON y ALTI
ESTACIONES = {
    'BEDARIEUX': {'LAT': 43.6398, 'LON': 3.146, 'ALTI': 373},
    'BEZIERS-COURTADE': {'LAT': 43.3343, 'LON': 3.155, 'ALTI': 25},
    'BEZIERS-VIAS': {'LAT': 43.322, 'LON': 3.3526, 'ALTI': 15},
    'CAMBON-ET-SALVERGUES': {'LAT': 43.6223, 'LON': 2.8653, 'ALTI': 955},
    'CASTANET LE HAUT_SAPC': {'LAT': 43.6675, 'LON': 2.9761, 'ALTI': 424},
    'LA VACQUERIE_SAPC': {'LAT': 43.792, 'LON': 3.4578, 'ALTI': 620},
    'LE CAYLAR_SAPC': {'LAT': 43.8671, 'LON': 3.3085, 'ALTI': 729},
    'LES PLANS': {'LAT': 43.786, 'LON': 3.2461, 'ALTI': 846},
    'LODEVE': {'LAT': 43.7303, 'LON': 3.3031, 'ALTI': 184},
    'LUNAS': {'LAT': 43.6958, 'LON': 3.1706, 'ALTI': 249},
    'MARSEILLAN-INRAE': {'LAT': 43.3283, 'LON': 3.5653, 'ALTI': 1},
    'MARSILLARGUES': {'LAT': 43.6338, 'LON': 4.168, 'ALTI': 4},
    'MONTARNAUD': {'LAT': 43.6358, 'LON': 3.6881, 'ALTI': 148},
    'MONTPELLIER-AEROPORT': {'LAT': 43.5761, 'LON': 3.9646, 'ALTI': 1},
    'MOULES-ET-BAUCELS': {'LAT': 43.948, 'LON': 3.752, 'ALTI': 252},
    'MURVIEL LES BEZIERS': {'LAT': 43.476, 'LON': 3.146, 'ALTI': 140},
    'PEZENAS-TOURBES': {'LAT': 43.4376, 'LON': 3.4003, 'ALTI': 40},
    'PRADES LE LEZ': {'LAT': 43.7183, 'LON': 3.8666, 'ALTI': 69},
    'ROUJAN-INRAE': {'LAT': 43.4916, 'LON': 3.3213, 'ALTI': 73},
    'SETE': {'LAT': 43.3973, 'LON': 3.6921, 'ALTI': 75},
    'SIRAN': {'LAT': 43.3265, 'LON': 2.6751, 'ALTI': 137},
    'SOUMONT': {'LAT': 43.707, 'LON': 3.3475, 'ALTI': 252},
    'ST ANDRE DE SANGONIS': {'LAT': 43.6641, 'LON': 3.5078, 'ALTI': 86},
    'ST JEAN DE MINERVOIS': {'LAT': 43.3856, 'LON': 2.8576, 'ALTI': 258},
    'ST MARTIN DE LONDRES': {'LAT': 43.7795, 'LON': 3.7293, 'ALTI': 214},
    'ST MAURICE-NAVACELLE': {'LAT': 43.8413, 'LON': 3.5223, 'ALTI': 584},
    'VAILHAN': {'LAT': 43.5468, 'LON': 3.2993, 'ALTI': 122},
    'VILLENEUVE-LES-MAG-INRAE': {'LAT': 43.5381, 'LON': 3.8538, 'ALTI': 20}
}



def crear_grafico(nombre, df):
    # Configuración de estilo
    plt.figure(figsize=(10, 6), dpi=100)
    sns.set_style("white") # Fondo limpio sin rayas grises pesadas

    # Eje para la Lluvia (Barras Azules hacia arriba)
    plt.bar(df['FECHA'], df['RR'], color='#4a90e2', label='Lluvia (Gonflement)', zorder=2)

    # Eje para la Temperatura (Barras Naranjas hacia abajo)
    # Multiplicamos por -1 para que bajen desde el centro
    plt.bar(df['FECHA'], df['TM'] * -1, color='#ff9f43', label='Stress Térmico (Contracción)', zorder=2)

    # Línea de equilibrio (El "0")
    plt.axhline(0, color='red', linewidth=1.5, linestyle='-', zorder=3)

    # Ajustes de ejes
    plt.title(f"MONITOR DE RIESGO INFRAESTRUCTURA: {nombre}", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Hinchamiento (mm)  /  Contracción (°C)", fontsize=10, fontweight='bold')
    
    # Limpiar el eje X
    plt.xticks(rotation=45, ha='right', fontsize=9)
    
    # Eliminar bordes innecesarios
    sns.despine(left=True, bottom=True)
    
    # Añadir una leyenda elegante
    plt.legend(loc='upper left', frameon=False, fontsize=9)

    # Ajuste final de márgenes para que no se corten las fechas
    plt.tight_layout()

    if not os.path.exists('graficos'):
        os.makedirs('graficos')
        
    plt.savefig(f'graficos/{nombre}.png', facecolor='white')
    plt.close()
