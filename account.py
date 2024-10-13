import configparser
import os
from time import sleep
import random

def banner():
    os.system('cls')
    print(f'''
        
                    ░░      ░░░        ░░        ░░  ░░░░  ░░       ░░
                    ▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒
                    ▓▓      ▓▓▓      ▓▓▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓  ▓▓       ▓▓
                    ███████  ██  ███████████  █████  ████  ██  ███████
                    ██      ███        █████  ██████      ███  ███████
                                                                                                                                            
''')
    
from license_check import check_license
if not check_license():
    exit(1)       


cpass = configparser.RawConfigParser()
if not os.path.exists('config.data'):
    with open('config.data', 'w') as f:
        pass

cpass.read('config.data')


# ====================[FUNCTION DISPLAY & EDIT ACCOUNTS]====================
def display_accounts(config_data='config.data'):
    config = configparser.RawConfigParser()
    config.read(config_data)

    if not config.sections():
        print("[!] No accounts found. Please add an account first.\n")
        sleep(1.5)
        return
    
    print("[+] Telegram Accounts :")
    for i, section in enumerate(config.sections(), 1):
        print(f"{i}. {section}\n")

    choix = input("[*] Enter a number to display the account details : ")
    if choix.lower() == 'q':
        return
    try:
        chosen_section = config.sections()[int(choix) - 1]
    except (ValueError, IndexError):
        print("[!] Invalid choice!")
        sleep(1.5)
        return
    
    print(f"\n[+] Account Details : {chosen_section}")
    account_info = dict(config.items(chosen_section))
    for cle, valeur in account_info.items():
        print(f"{cle}: {valeur}")

    edit = input("\n[+] Edit this account? (y/n): ").lower()
    if edit != 'y':
        return
    
    for cle in account_info.keys():
        new_value = input(f"[+] Enter new value for {cle} (press enter to keep): ")
        if new_value:
            config.set(chosen_section, cle, new_value)

    with open(config_data, 'w') as configfile:
        config.write(configfile)
    print(f"[+] Account '{chosen_section}' updated successfully!")
    sleep(1.5)


# ====================[FUNCTION ADD ACCOUNT]====================
def add_account():
    account_name = len(cpass.sections()) + 1
    section_name = f'account{account_name}'
    
    xid = input("[+] Enter the api ID : ")
    xhash = input("[+] Enter the hash ID : ")
    xphone = input("[+] Enter the phone number : ")
    
    cpass[section_name] = {
        'id': xid,
        'hash': xhash,
        'phone': xphone
    }
    
    with open('config.data', 'w') as configfile:
        cpass.write(configfile)
    print(f"[+] Account '{account_name}' added successfully !\n")
    sleep(1.5)


# ====================[FUNCTION DELETE ACCOUNTS]====================
def delete_account(config_data='config.data'):
    config = configparser.RawConfigParser()
    config.read(config_data)

    if not cpass.sections():
        print("[!] No accounts found.")
        sleep(1.5)
        return
    
    print("[+] Telegram Accounts :")
    for i, section in enumerate(config.sections(), 1):
        print(f"{i}. {section}\n")

    account_section = input("[*] Enter the name of the section to delete the account : ")
    if account_section not in cpass.sections():
        print("[!] It doesn't exist...")
        sleep(1.5)
        return
    
    confirm = input(f"Are you sure you want to delete '{account_section}'? (y/n) : ").lower()
    if confirm == 'y':
        cpass.remove_section(account_section)
        with open('config.data', 'w') as configfile:
            cpass.write(configfile)
        print(f"[+] Account '{account_section}' delete !")
        sleep(1.5)
    else:
        print("[*] Delete cancel.")
        sleep(0.5)


def get_api_details():
    config = configparser.RawConfigParser()
    config.read('config.data')

    if not config.sections():
        print("[!] No accounts found. Please add an account first.\n")
        sleep(1.5)
        return None 
    
    try: 
        api_detail = random.choice(config.sections())
        api_id = config[api_detail]['id']
        api_hash = config[api_detail]['hash']
        phone = config[api_detail]['phone']

        return {
            'account_name': api_detail,
            'api_id': api_id,
            'hash': api_hash,
            'phone': phone
        }
    except KeyError:
        print("[!] Something went wrong! Please check your configuration.\n")
        sleep(1.5)
        return None



# ====================[MAIN MENU]====================
if __name__ == "__main__":
    while True:
        banner()
        print("\n[*] Telegram Account Manager\n")
        print("1. Display or Edit Accounts")
        print("2. Add an Account")
        print("3. Delete an Account")
        print("4. Quit")

        choice = input("Please choose your action (1/2/3/4): ")

        if choice == '1':
            display_accounts()
        elif choice == '2':
            add_account()
        elif choice == '3':
            delete_account()
        elif choice == '4' or choice.lower() == 'q':
            print("Goodbye!")
            break
        else:
            print("[!] Invalid choice!")
            sleep(0.5)


# ==================[END]====================
# Code Create by @Joedebiden on github or Baudelaire for the intime ;) 
# please dont reverse this shit