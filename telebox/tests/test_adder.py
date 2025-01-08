"""
Work very well in terminal to use adder class
Put you in telebox directory and run this command:
$ python.exe -m tests.test_adder
"""
from features.adder import Adder
from features.telegram_base import TelegramBase

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

    users = adder.open_file(input_file='users/demo.csv')
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

    
    # speed mode (1-5)
    speed = adder.set_speed_mode(mode="Fast")
    if not speed:
        print("[!] Invalid speed.")
        adder.disconnect()
        exit()

    # en parametre: le groupe cible, les utilisateurs, la méthode et la vitesse
    adder.add_users(target_group, users, speed)
    adder.disconnect()


