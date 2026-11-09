# Projet Pipeline Log Analyzer

## Description
Ce projet analyse des fichiers de logs SSH (auth.log) pour détecter les tentatives d'intrusion et générer un dashboard visuel.

## Fonctionnalités
- Lecture automatique des fichiers de logs (texte brut et gzip `.gz`)
- Extraction des tentatives échouées (Failed password, Invalid user)
- Géolocalisation des adresses IP via l'API IPinfo
- Dashboard Matplotlib avec 3 graphiques :
  1. Tentatives échouées par pays
  2. Connexions réussies par utilisateur
  3. Tentatives avec utilisateurs invalides

## Architecture du projet
- `ingestion/raw.py` : lecture des fichiers de données
- `processing/extract_transform.py` : analyse des logs (regex)
- `processing/geo_location.py` : appel à l'API de géolocalisation
- `logger.py` : configuration des logs (app.log)
- `main.py` : point d'entrée et dashboard

## Installation
1. Cloner le projet
2. Installer les dépendances avec uv :
   uv sync

## Utilisation
Placer les fichiers de logs dans le dossier `data/`, puis lancer :
python main.py

## Auteur
Moumen Youssef - 3ème année