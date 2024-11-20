"""
Work very in terminal to use AccountManager class
$ python -m telebox.tests.test_scraper
"""
from features.scraper import Scraper
from features.telegram_base import TelegramBase

# ======================[TEST DE LA CLASSE]==========================
if __name__ == "__main__":
    
    telegram_connect = TelegramBase()
    acc_details = telegram_connect.read_account_details()
    print(f"test {acc_details}")
    
