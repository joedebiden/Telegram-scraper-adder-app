"""
Work very in terminal to use scraper class
$ python.exe -m telebox.tests.test_scraper
"""
from ..features.scraper import Scraper
from ..features.telegram_base import TelegramBase

# ======================[TEST DE LA CLASSE]==========================
"""test process in order :
    list telegram account in 'account.data'
    select an account 
    connect client
    get groups
    select group
    scraping process
    save file path"""

if __name__ == "__main__":
    
    scraper = Scraper(session_name='session_name', config_file='account.data')
    available_accounts = scraper.list_accounts()


    section_name = input("[+] Enter the account name to use: ")
    if section_name not in available_accounts:
        print("[!] Account not found.")
    else:
        scraper.section_name = section_name
        scraper.read_account_details()
        
