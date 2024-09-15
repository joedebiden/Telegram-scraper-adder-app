import configparser
import os

config = configparser.RawConfigParser()

if not os.path.exists('proxies.ini'):
    with open('proxies.ini', 'w') as f:
        pass
config.read('proxies.ini')



def add_proxy():
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
    print(f"[+] Proxy {section_name} added successfully!\n")

def main():
    print("[!] Proxy Setup")
    while True:
        add_proxy()

        another = input("[+] Add another proxy? (y/n): ").lower()
        if another != 'y':
            break


def test_proxy(proxy):
    import requests
    proxies = {
        'http': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['addr']}:{proxy['port']}",
        'https': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['addr']}:{proxy['port']}"
    }
    try:
        response = requests.get('https://ipinfo.io', proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("[+] Proxy works!")
        else:
            print(f"[-] Proxy failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Proxy test failed: {e}")






if __name__ == '__main__':
    #main()
    proxy = {
    'proxy_type': 'socks5',
    'addr': 'residential.digiproxy.cc',
    'port': 9595,
    'username': 'u1WhTbxkIrSoAiY-res_sc-us_louisiana_Neworleans',
    'password': 'dmucen0uiXuhPHd',
    'rdns': True
    }
    test_proxy(proxy)
    # Appel de la fonction asynchrone
    