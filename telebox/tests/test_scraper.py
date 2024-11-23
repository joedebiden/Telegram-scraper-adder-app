"""
Work very in terminal to use scraper class
$ python.exe -m telebox.tests.test_scraper
"""
from ..features.scraper import Scraper
from ..features.telegram_base import TelegramBase

# ======================[TEST DE LA CLASSE]==========================
if __name__ == "__main__":

    scraper = Scraper('session', 12641519, 'b1d9376e2825cf869149f6ba6ced114f', '+33772240484', config_file='account.data')
    scraper.connect()
    scraper.get_account_info() 
    scraper.disconnect()
