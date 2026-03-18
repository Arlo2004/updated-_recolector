from meteofrance_api import MeteoFranceClient
import pandas as pd
from datetime import datetime

# Tu diccionario perfecto
ESTACIONES_HERAULT = {
    'BEDARIEUX': {'LAT': 43.639833, 'LON': 3.146, 'ALTI': 373},
    'BEZIERS-COURTADE': {'LAT': 43.334333, 'LON': 3.155, 'ALTI': 25},
    'BEZIERS-VIAS': {'LAT': 43.322, 'LON': 3.352667, 'ALTI': 15},
    'CAMBON-ET-SALVERGUES': {'LAT': 43.622333, 'LON': 2.865333, 'ALTI': 955},
    'CASTANET LE HAUT_SAPC': {'LAT': 43.6675, 'LON': 2.976167, 'ALTI': 424},
    'LA VACQUERIE_SAPC': {'LAT': 43.792, 'LON': 3.457833, 'ALTI': 620},
    'LE CAYLAR_SAPC': {'LAT': 43.867167, 'LON': 3.3085, 'ALTI': 729},
    'LES PLANS': {'LAT': 43.786, 'LON': 3.246167, 'ALTI': 846},
    'LODEVE': {'LAT': 43.730333, 'LON': 3.303167, 'ALTI': 184},
    'LUNAS': {'LAT': 43.695833, 'LON': 3.170667, 'ALTI': 249},
    'MARSEILLAN-INRAE': {'LAT': 43.328333, 'LON': 3.565333, 'ALTI': 1},
    'MARSILLARGUES': {'LAT': 43.633833, 'LON': 4.168, 'ALTI': 4},
    'MONTARNAUD': {'LAT': 43.635833, 'LON': 3.688167, 'ALTI': 148},
    'MONTPELLIER-AEROPORT': {'LAT': 43.576167, 'LON': 3.964667, 'ALTI': 1},
    'MOULES-ET-BAUCELS': {'LAT': 43.948, 'LON': 3.752, 'ALTI': 252},
    'MURVIEL LES BEZIERS': {'LAT': 43.476, 'LON': 3.146, 'ALTI': 140},
    'PEZENAS-TOURBES': {'LAT': 43.437667, 'LON': 3.400333, 'ALTI': 40},
    'PRADES LE LEZ': {'LAT': 43.718333, 'LON': 3.866667, 'ALTI': 69},
    'ROUJAN-INRAE': {'LAT': 43.491667, 'LON': 3.321333, 'ALTI': 73},
    'SETE': {'LAT': 43.397333, 'LON': 3.692167, 'ALTI': 75},
    'SIRAN': {'LAT': 43.3265, 'LON': 2.675167, 'ALTI': 137},
    'SOUMONT': {'LAT': 43.707, 'LON': 3.3475, 'ALTI': 252},
    'ST ANDRE DE SANGONIS': {'LAT': 43.664167, 'LON': 3.507833, 'ALTI': 86},
    'ST JEAN DE MINERVOIS': {'LAT': 43.385667, 'LON': 2.857667, 'ALTI': 258},
    'ST MARTIN DE LONDRES': {'LAT': 43.7795, 'LON': 3.729333, 'ALTI': 214},
    'ST MAURICE-NAVACELLE': {'LAT': 43.841333, 'LON': 3.522333, 'ALTI': 584},
    'VAILHAN': {'LAT': 43.546833, 'LON': 3.299333, 'ALTI': 122},
    'VILLENEUVE-LES-MAG-INRAE': {'LAT': 43.538167, 'LON': 3.853833, 'ALTI': 20},
}

def recolectar_pronostico_meteofrance():
    # Inicializamos el cliente oficial
    client = MeteoFranceClient()
    resultados = []
    
    print("--- CONECTANDO CON MÉTÉO-FRANCE ---")
    
    for nombre, coord in ESTACIONES_HERAULT.items():
        try:
            # Obtenemos el pronóstico para esas coordenadas exactas
            forecast = client.get_forecast(latitude=coord['LAT'], longitude=coord['LON'])
            
            # Extraemos los datos diarios (suele dar los próximos 14 días)
            for day in forecast.daily_forecast:
                # Météo-France devuelve la fecha en formato Unix (timestamp)
                fecha = datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
                
                # Extraemos Temp Max y Min para calcular la Media (TM)
                t_max = day.get('T', {}).get('max')
                t_min = day.get('T', {}).get('min')
                tm = round((t_max + t_min) / 2, 2) if (t_max is not None and t_min is not None) else None
                
                # Extraemos la Lluvia (RR)
                rr = day.get('precipitation', {}).get('24h')

                resultados.append({
                    "FECHA": fecha,
                    "NOM_POSTE": nombre,
                    "LAT": coord['LAT'],
                    "LON": coord['LON'],
                    "ALT": coord['ALTI'],
                    "RR": rr,
                    "TM": tm
                })
            print(f"✓ {nombre}: Datos obtenidos.")
            
        except Exception as e:
            print(f"✗ Error en {nombre}: {e}")

    # Lo convertimos a una tabla limpia y lo guardamos
    df_futuro = pd.DataFrame(resultados)
    df_futuro.to_csv('herault_pronostico_meteofrance.csv', index=False)
    
    print("-" * 40)
    print(f"¡LISTO! Archivo 'herault_pronostico_meteofrance.csv' generado con {len(df_futuro)} filas.")

if __name__ == "__main__":
    recolectar_pronostico_meteofrance()
