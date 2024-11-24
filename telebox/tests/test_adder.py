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
        exit()
    else:
        adder.section_name = section_name
        adder.read_account_details()

    adder.connect()
    adder.get_account_info()

    users = adder.open_file()
    if users:
        for user in users:
            print(user)

    groups = adder.get_groups()
    if not groups: 
        print("[!] No groups available.")
        adder.disconnect()
        exit()

    target_group = adder.select_group(groups)
    if not target_group:
        print("[!] No group selected.")
        adder.disconnect()
        exit()

    # by id or username 
    method = adder.choose_method()
    if not method:
        print("[!] Invalid method.")
        adder.disconnect()
        exit()
    
    # speed mode (1-5)
    speed = adder.set_speed_mode(mode=3)
    if not speed:
        print("[!] Invalid speed.")
        adder.disconnect()
        exit()

    add_members = adder.add_users(target_group, method, speed)
    if not add_members:
        print("[!] Error while adding members.")
        adder.disconnect()
        exit()


