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
        response = requests.get('93.127.202.5:5000', proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("[+] Proxy works!")
        else:
            print(f"[-] Proxy failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Proxy test failed: {e}")






import asyncio
from telethon import TelegramClient
import sys
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.sync import TelegramClient 
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

# ==================[ CONFIG READER ]==================

cpass = configparser.RawConfigParser()
cpass.read('config.data')
try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    
    print("[!] something went wrong with config.data file\n")
    sys.exit(1)

# ==================[ CONNECT CLIENT ]===================
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    
    client.sign_in(phone, input('[+] Enter the code: '))



async def test_proxy_telethon(proxy):
    client = TelegramClient('session_name', api_id, api_hash, proxy=proxy)
    
    try:
        await client.connect()
        if await client.is_user_authorized():
            print("[+] Proxy works and user is authorized!")
        else:
            print("[+] Proxy works but user is not authorized!")
        await client.disconnect()
    except ConnectionError:
        print("[-] Failed to connect via proxy")
    except Exception as e:
        print(f"[-] Error during proxy test: {e}")







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
    asyncio.run(test_proxy_telethon(proxy))