import json
import os
import requests
from logger import logger

CACHE_FILE = "geo_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur de lecture du cache : {e}")
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4)
    except Exception as e:
        logger.error(f"Erreur de sauvegarde du cache : {e}")

def resolve_ips_to_countries(unique_ips):
    cache = load_cache()
    ip_to_country = {}
    new_entries = False

    for ip in unique_ips:
        if ip in cache:
            ip_to_country[ip] = cache[ip]
        else:
            try:
                url = f"https://ipinfo.io/{ip}/json"
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    country = response.json().get("country", "Inconnu")
                else:
                    country = "Inconnu"
            except Exception:
                country = "Inconnu"
            
            cache[ip] = country
            ip_to_country[ip] = country
            new_entries = True

    if new_entries:
        save_cache(cache)

    return ip_to_country