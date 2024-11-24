"""
Work very in terminal to use scraper class
$ python.exe -m telebox.tests.test_adder
"""
from ..features.adder import Adder
from ..features.telegram_base import TelegramBase

# ======================[TEST DE LA CLASSE]==========================
"""test process in order :
    list telegram account in 'account.data'
    select an account 
    connect client
    open file with users
    get groups
    select group
    choosing method (id or username)
    choosing speed process
    add users"""

if __name__ == "__main__":
    
    adder = Adder(session_name='session_name', config_file='account.data')
    available_accounts = adder.list_accounts()

    section_name = input("[+] Enter the account name to use: ")
    if section_name not in available_accounts:
        print("[!] Account not found.")
    else:
        adder.section_name = section_name
        adder.read_account_details()

    adder.connect()
    adder.get_account_info()