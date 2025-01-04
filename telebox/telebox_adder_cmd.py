from features.adder import Adder


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

    # doit choisir un fichier CSV ou TXT contenant les utilisateurs à ajouter
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

    # doit pouvoir choisir la vitesse d'ajout
    speed = adder.set_speed_mode(mode="Fast")
    if not speed:
        print("[!] Invalid speed.")
        adder.disconnect()
        exit()

 
    adder.add_users(target_group, users, speed)
    

    adder.disconnect()
