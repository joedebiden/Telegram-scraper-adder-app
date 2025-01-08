import configparser
import os
import sys
from time import sleep

from codes.old_license_check import check_license
if not check_license():
    sleep(2)
    exit(1) 

def banner():
    os.system('cls')
    print(r'''
                ._______ .______  ._______   ____   ____.___ ._______.________
                : ____  |: __   \ : .___  \  \   \_/   /: __|: .____/|    ___/
                |    :  ||  \____|| :   |  |  \___ ___/ | : || : _/\ |___    \.
                |   |___||   :  \ |     :  |  /   _   \ |   ||   /  \|       /
                |___|    |   |___\ \_. ___/  /___/ \___\|   ||_.: __/|__:___/ 
                         |___|       :/                 |___|   :/      :                                                                           
''')
    

config = configparser.RawConfigParser()

if not os.path.exists('proxies.ini'):
    with open('proxies.ini', 'w') as f:
        pass
config.read('proxies.ini')


# ====================[FUNCTION ADD PROXY]====================
def add_proxy():
    proxy_count = len(config.sections()) + 1  
    section_name = f'proxy{proxy_count}'
    
    proxy_type = input("[+] Enter Proxy Type (socks5/socks4/http): ").lower()
    addr = input("[+] Enter Proxy Host: ")
    port = input("[+] Enter Proxy Port: ")
    username = input("[+] Enter Proxy Username (optional): ") or 'None'
    password = input("[+] Enter Proxy Password (optional): ") or 'None'
    rdns = input("[+] Use Remote DNS? (True/False): ").capitalize() or 'True'
    
    # ajout de "section" pour un proxy
    config[section_name] = {
        'proxy_type': proxy_type,
        'addr': addr, #address
        'port': port,
        'username': username,
        'password': password,
        'rdns': rdns #remote dns, true = géré par le serveur, false = géré par le client
    }

    # Écrire dans le fichier proxies.ini
    with open('proxies.ini', 'w') as configfile:
        config.write(configfile)
    print(f"[+] Proxy {section_name} added successfully!\n")


# ====================[FUNCTION MAIN]====================
def main():
    banner()
    print("[+] Proxy Setup")
    while True:
        banner()
        add_proxy()

        another = input("[+] Add another proxy? (y/n): ").lower()
        if another != 'y':
            break


# ====================[FUNCTION TEST PROXY (HTTP REQUESTS)]====================
def test_proxy(proxy): 
    import requests
    #pip install requests[socks]

    proxies = {
        'http': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['addr']}:{proxy['port']}",
        'https': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['addr']}:{proxy['port']}" 
    }
    
    try:
        response = requests.get('https://ipinfo.io', proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("\n[+] Proxy works!")
            input("Press the Enter key to continue...") 
            
        else:
            print(f"\n[-] Proxy failed with status code: {response.status_code}\n")
            input("Press the Enter key to continue...") 
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Proxy test failed: {e}\n")
        input("Press the Enter key to continue...") 
    


# ====================[FUNCTION TEST DIRECT CONNECTION]====================
def test_direct_connection():
    import requests
    try:
        response = requests.get('https://ipinfo.io', timeout=5)
        if response.status_code == 200:
            print("\n[+] Direct connection works! Your IP:", response.json()["ip"])
        else:
            print(f"\n[-] Direct connection failed with status code: {response.status_code}\n")
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Direct connection test failed: {e}\n")
# test_direct_connection()
# input("Press the Enter key to continue...")



# ====================[FUNCTION DISPLAY & EDIT PROXIES DETAILS]====================
def display_proxies(proxies_file='proxies.ini'):
    config = configparser.ConfigParser()
    config.read(proxies_file)

    if not config.sections():
        print("[!] No proxies found!")
        return
    print("[+] Lists of proxies (q = quit):")
    for i, section in enumerate(config.sections(), 1):
        print(f"{i}. {section}\n")
        
    choix = input("[+] Enter a number to view proxy details : ")
    if choix.lower() == 'q':
        return
    try:
        chosen_section = config.sections()[int(choix) - 1]
    except (ValueError, IndexError):
        print("[!] Invalid choice!")
        return
    
    print(f"\n[+] Proxy Number: {chosen_section}\n")
    proxy_info = dict(config.items(chosen_section))
    for cle, valeur in proxy_info.items():
        print(f"{cle}: {valeur}")
    
    edit = input("\n[+] Edit this proxy? (y/n): ").lower()
    if edit != 'y':
        return

    for cle in proxy_info.keys():
        new_value = input(f"[+] Enter new value for {cle} (press enter to keep): ")
        if new_value:
            config.set(chosen_section, cle, new_value)

    with open(proxies_file, 'w') as configfile:
        config.write(configfile)

    print(f"[+] Proxy from {chosen_section} updated successfully!")    


# ====================[MENU]====================
def menu():
    print("\n====== Menu ======\n")
    print("[1]. Add Proxy")
    print("[2]. Test Proxy")
    print("[3]. Display & Edit Proxies")
    print("[4]. Quit")
    choix = input("\n[*] Select your option : ")
    return choix


# ==================[MAIN APP]====================
if __name__ == '__main__':
    while True:
        banner() 
        choix = menu() 
        # ============[choice 1]============
        if choix == '1':
            print("\nAdd Proxy...")
            main() 

        # ============[choice 2]============
        elif choix == '2':
            cpass = configparser.RawConfigParser()
            cpass.read('proxies.ini')

            if not config.sections():
                print("\n[!] No proxies found!")
                quit()
            print("[+] Lists of proxies (q = quit):")
            for i, section in enumerate(config.sections(), 1):
                print(f"{i}. {section}\n")
            choix = input("[+] Enter a number to test the proxy : ")
            if choix.lower() == 'q':
                quit()
            try:
                chosen_section = config.sections()[int(choix) - 1]
            except (ValueError, IndexError):
                print("[!] Invalid choice!")
                quit()
            
            print(f"[+] The proxy you choose to test the connexion: {chosen_section}")

            try:
                proxy_type = cpass[chosen_section]['proxy_type']
                addr = cpass[chosen_section]['addr']
                port = cpass[chosen_section]['port']
                username = cpass[chosen_section]['username']
                password = cpass[chosen_section]['password']
                rdns = cpass[chosen_section]['rdns']
                proxy = {
                    'proxy_type': proxy_type,
                    'addr': addr,
                    'port': port,
                    'username': username,
                    'password': password,
                    'rdns': rdns
                }
                #print(proxy)
            
            except KeyError:
                banner()
                print("\n[!] Bad Proxy config detect in file proxies.ini !!")
                print("[!] Please add again proxy or edit the file (be carefull) !!")
                sys.exit(1)

            print(f"[!] Testing the {chosen_section}...")
            test_proxy(proxy)  

        # ============[choice 3]============
        elif choix == '3':
            print("\n[*] Here your proxies :")
            display_proxies()  

        # ============[choice 4]============
        elif choix == '4' or choix.lower() == 'q':
            print("[*] Bye")
            sys.exit(0) 

        else:
            print("\n[!] Invalid choice, please try again...")

# ==================[END]====================
# Code Create by @Joedebiden on github or Baudelaire for the intime ;) 
# please dont reverse this shit