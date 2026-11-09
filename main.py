import os
import sys
from collections import Counter
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from logger import logger
from ingestion import raw
from processing import extract_transforme
from processing import geo_location

def afficher_dashboard(country_counts, successful_users, invalid_users):
    """Génère un dashboard avec 3 graphiques côte à côte."""
    # Création de la figure avec 1 ligne et 3 colonnes
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Dashboard d'Analyse des Logs ", fontsize=16, fontweight='bold')

    # Graphique 1 : Top 10 Échecs par Pays
    top_countries = country_counts.most_common(10)
    if top_countries:
        countries, counts = zip(*top_countries)
        axes[0].bar(countries, counts, color='#1f77b4')
        axes[0].set_title("Top 10 : Échecs par Pays")
        axes[0].set_ylabel("Nombre d'échecs")
        axes[0].tick_params(axis='x', rotation=45)
    else:
        axes[0].text(0.5, 0.5, "Aucune donnée", ha='center', va='center')
        axes[0].set_title("Top 10 : Échecs par Pays")

    # Graphique 2 : Top 10 Invalid Users
    top_invalid = invalid_users.most_common(10)
    if top_invalid:
        users_inv, counts_inv = zip(*top_invalid)
        axes[1].bar(users_inv, counts_inv, color='#d62728')
        axes[1].set_title("Top 10 : Utilisateurs Invalides")
        axes[1].tick_params(axis='x', rotation=45)
    else:
        axes[1].text(0.5, 0.5, "Aucune donnée", ha='center', va='center')
        axes[1].set_title("Top 10 : Utilisateurs Invalides")

    # Graphique 3 : Connexions Réussies
    if successful_users:
        top_success = successful_users.most_common(10)
        users_succ, counts_succ = zip(*top_success)
        axes[2].bar(users_succ, counts_succ, color='#2ca02c')
        axes[2].set_title("Connexions Réussies par Utilisateur")
        axes[2].tick_params(axis='x', rotation=45)
    else:
        # Si aucune connexion n'a réussi (ce qui est votre cas actuel)
        axes[2].text(0.5, 0.5, "Aucune connexion\nSSH réussie détectée", ha='center', va='center', fontsize=12, color='green')
        axes[2].set_title("Connexions Réussies par Utilisateur")
        axes[2].axis('off') # Cache les axes car il n'y a pas de barres

    plt.tight_layout()
    plt.show()

def main():
    logger.info("Démarrage de l'analyse des journaux...")
    
    lines = list(raw.read_log_files("./data"))
    if not lines:
        logger.warning("Aucune ligne lue. Vérifiez le dossier ./data.")
        return

    logger.info(f"Total de lignes analysées : {len(lines)}")

    # Extraction des données
    failed_ips_list = extract_transforme.extract_failed_ip_counts(lines)
    successful_users_list = extract_transforme.extract_successful_users(lines)
    invalid_users_list = extract_transforme.extract_invalid_user_attempts(lines)

    failed_ip_counts = Counter(failed_ips_list)
    successful_users = Counter(successful_users_list)
    invalid_users = Counter(invalid_users_list)

    unique_ips = list(failed_ip_counts.keys())
    ip_to_country = geo_location.resolve_ips_to_countries(unique_ips)

    country_counts = Counter()
    for ip, count in failed_ip_counts.items():
        country = ip_to_country.get(ip, "Inconnu")
        if country != "Inconnu":  # <-- On ignore les Inconnus
            country_counts[country] += count

    # Affichage dans la console
    print("\n" + "="*50 + "\n 1. TENTATIVES ÉCHOUÉES PAR PAYS\n" + "="*50)
    for country, count in country_counts.most_common(15):
        print(f"{country:<15} | {count}")

    print("\n" + "="*50 + "\n 2. TENTATIVES RÉUSSIES PAR USER\n" + "="*50)
    if successful_users:
        for user, count in successful_users.most_common():
            print(f"{user:<20} | {count}")
    else:
        print("Aucune connexion SSH réussie détectée.")

    print("\n" + "="*50 + "\n 3. TENTATIVES ÉCHOUÉES AVEC INVALID USER (TOP 15)\n" + "="*50)
    for user, count in invalid_users.most_common(15):
        print(f"{user:<25} | {count}")

    # Lancement du dashboard graphique
    afficher_dashboard(country_counts, successful_users, invalid_users)
    
    logger.info("Analyse terminée.")

if __name__ == "__main__":
    main()