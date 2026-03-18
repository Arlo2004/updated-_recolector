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
    plt.figure(figsize=(10, 6))
    
    # Lluvia
    ax1 = plt.gca()
    ax1.bar(df['FECHA'], df['RR'], color='blue', alpha=0.6)
    ax1.set_ylabel('Lluvia (mm)', color='blue')
    
    # Temperatura Invertida
    ax2 = ax1.twinx()
    ax2.plot(df['FECHA'], df['TM'], color='red', marker='o', linewidth=2)
    ax2.set_ylabel('Temperatura Media (°C)', color='red')
    ax2.invert_yaxis()
    
    # EL TÍTULO CAMBIA POR CADA CIUDAD AUTOMÁTICAMENTE
    plt.title(f"Pronóstico de Riesgo - {nombre}", fontsize=14, fontweight='bold')
    
    if not os.path.exists('graficos'):
        os.makedirs('graficos')
        
    plt.savefig(f'graficos/{nombre}.png')
    plt.close()

def main():
    client = MeteoFranceClient()
    datos_completos = []
    
    for nombre, coord in ESTACIONES.items():
        try:
            pronostico = client.get_forecast(latitude=coord['LAT'], longitude=coord['LON'])
            datos_ciudad = []
            
            for dia in pronostico.daily_forecast:
                fecha = datetime.fromtimestamp(dia['dt']).strftime('%d/%m/%Y')
                t_max = dia.get('T', {}).get('max', 0)
                t_min = dia.get('T', {}).get('min', 0)
                tm = round((t_max + t_min) / 2, 2)
                rr = dia.get('precipitation', {}).get('24h', 0)
                
                fila = {
                    "NOMBRE": nombre,
                    "LAT": coord['LAT'],
                    "LON": coord['LON'],
                    "ALTI": coord['ALTI'],
                    "FECHA": fecha,
                    "RR": rr,
                    "TM": tm
                }
                datos_ciudad.append(fila)
                datos_completos.append(fila)
                
            df_ciudad = pd.DataFrame(datos_ciudad)
            crear_grafico(nombre, df_ciudad)
            
        except Exception as e:
            pass # Si una ciudad falla, sigue con la siguiente sin detenerse

    # Guarda el archivo de datos general
    pd.DataFrame(datos_completos).to_csv('datos_pronostico.csv', index=False)

if __name__ == "__main__":
    main()
