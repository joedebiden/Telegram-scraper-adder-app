"""
Work very in terminal to use scraper class
$ python.exe -m telebox.tests.test_scraper
"""
from ..features.scraper import Scraper
from ..features.telegram_base import TelegramBase

# ======================[TEST DE LA CLASSE]==========================
if __name__ == "__main__":
    try:
        # Demander à l'utilisateur de fournir la section du compte à utiliser
        section_name = input("[+] Enter the section name for the account: ").strip()

        # Initialiser la classe Scraper avec les informations fournies
        scraper = Scraper(session_name="session", config_file="account.data", section_name=section_name)

        print("\n[+] Attempting to connect to Telegram...")
        scraper.connect()  # Connecter le compte Telegram

        # Afficher les informations du compte connecté
        scraper.get_account_info()

    except Exception as e:
        print(f"[!] An error occurred during testing: {e}")
    finally:
        # Déconnexion en fin de processus
        scraper.disconnect()
        print("[+] Disconnected from Telegram.")