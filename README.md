# Pipeline d'Acquisition de Données Météorologiques - Hérault

Ce dépôt implémente un système automatisé d'extraction et de structuration de données climatiques pour la surveillance des risques de Retrait-Gonflement des Argiles (RGA) dans le département de l'Hérault, France.

# Spécifications du Système

## 1. Extraction des Données (Backend)
Le cœur du système est un script Python (recolector.py) qui interagit avec l'API officielle de Météo-France. Le processus comprend :

* Segmentation Géographique : Surveillance de 28 stations via des coordonnées GPS et altitudes spécifiques.
* Variables de Contrôle : 
    * RR : Précipitations accumulées sur 24h (mm).
    * TM : Température Moyenne quotidienne calculée par la moyenne arithmétique des extrêmes (Tmax, Tmin).
* Horizon Temporel : Prévisions dynamiques à 7 jours.

#2. Automatización et Sécurité
Le flux de données est géré par GitHub Actions avec les protocoles suivants :

* Programmation : Exécution quotidienne automatisée (Cron Job).
* Résilience : Implémentation d'un système de tentatives (retries) avec délais programmés pour pallier les erreurs réseau ou la saturation de l'API.
* Persistance : Mise à jour automatique du fichier herault_pronostico_meteofrance.csv sur la branche principale.

 Estructura de Sortie (Dataset)

Le fichier CSV généré contient les colonnes suivantes :
* FECHA : Format ISO 8601 (YYYY-MM-DD).
* NOM_POSTE : Identifiant de la station.
* LAT / LON / ALT : Paramètres géographiques de la station.
* RR : Millimètres de précipitations.
* TM : Température moyenne en degrés Celsius.

Dépendances
* Python 3.9+
* meteofrance-api
* pandas
