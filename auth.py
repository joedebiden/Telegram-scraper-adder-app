import configparser
import os
import sys

def banner():
    os.system('cls')
    print(f'''
 ____                  _      _       _
| __ )  __ _ _   _  __| | ___| | __ _(_)_ __ ___
|  _ \ / _` | | | |/ _` |/ _ \ |/ _` | | '__/ _ \,
| |_) | (_| | |_| | (_| |  __/ | (_| | | | |  __/
|____/ \__,_|\__,_|\__,_|\___|_|\__,_|_|_|  \___|
                     _
 _ __  _ __ _____  _(_) ___  ___
| '_ \| '__/ _ \ \/ / |/ _ \/ __|
| |_) | | | (_) >  <| |  __/\__ \¤
| .__/|_|  \___/_/\_\_|\___||___/
|_|
          ''')
    

config = configparser.RawConfigParser()

if not os.path.exists('proxies.ini'):
    with open('proxies.ini', 'w') as f:
        pass
config.read('proxies.ini')



def add_proxy():
    banner()
    proxy_count = len(config.sections()) + 1  # Compter les sections actuelles pour numéroter les proxies
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
    banner()
    print(f"[+] Proxy {section_name} added successfully!\n")


def main():
    banner()
    print("[+] Proxy Setup")
    while True:
        banner()
        add_proxy()

        another = input("[+] Add another proxy? (y/n): ").lower()
        if another != 'y':
            break


def test_proxy(proxy):
    import requests
    import time


    proxies = {
        'http': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['addr']}:{proxy['port']}",
        'https': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['addr']}:{proxy['port']}"
    }
    try:
        response = requests.get('https://ipinfo.io', proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("\n[+] Proxy works!")
            time.sleep(2)
        else:
            print(f"\n[-] Proxy failed with status code: {response.status_code}")
            time.sleep(2)
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Proxy test failed: {e}")
        time.sleep(2)





def display_proxies(proxies_file='proxies.ini'):
    banner()
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
    
    print(f"\n[+] Proxy Number: {chosen_section}")
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

def menu():
    print("\n====== Menu ======\n")
    print("[1]. Add Proxy")
    print("[2]. Test Proxy")
    print("[3]. Display & Edit Proxies")
    print("[4]. Quit")
    choix = input("\n[*] Select your option : ")
    return choix


if __name__ == '__main__':
    while True:
        banner() 
        choix = menu() 
        
        if choix == '1':
            print("\nAdd Proxy...")
            main() 

        elif choix == '2':
            cpass = configparser.RawConfigParser()
            cpass.read('proxies.ini')

            try: #======/ possibility to choose the proxy withou changing manually here/======
                proxy_type = cpass['proxy1']['proxy_type']
                addr = cpass['proxy1']['addr']
                port = cpass['proxy1']['port']
                username = cpass['proxy1']['username']
                password = cpass['proxy1']['password']
                rdns = cpass['proxy1']['rdns']
                proxy = {
                    'proxy_type': proxy_type,
                    'addr': addr,
                    'port': port,
                    'username': username,
                    'password': password,
                    'rdns': rdns
                }
                print(proxy)
                
            except KeyError:
                banner()
                print("\n[!] No Proxies detect in file proxies.ini !!")
                print("\n[!] Please add some proxies first !!")
                sys.exit(1)
            print(f"\n[!] Testing the Proxy : {proxy}...")
            test_proxy(proxy)  


        elif choix == '3':
            print("\n[*] Here your proxies :")
            display_proxies()  

        elif choix == '4' or choix.lower() == 'q':
            print("\n[*] Bye")
            sys.exit(0) 

        else:
            print("\n[/!\] Invalid choice, please try again...")
