from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import os, sys
import configparser
import csv
from time import sleep


def banner():
    os.system('cls')
    print(f'''
  ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  ▓█████  ██▀███  
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░          ░░   ░   ░   ▒   ░░          ░     ░░   ░ 
      ░  ░ ░         ░           ░  ░            ░  ░   ░     
         ░                                                    
''')

# ==================[ CONFIG READER ]==================

cpass = configparser.RawConfigParser()
cpass.read('config.data')
banner()


# ====================[API DETAILS]====================
from setup import get_api_details
details = get_api_details()

if details:
    account_name = details['account_name']
    api_id = details['api_id']
    api_hash = details['hash']
    phone = details['phone']
    
    print(f"Random [{account_name}] choosen\n, API ID: {api_id}\n, Hash: {api_hash}\n, Phone: {phone}\n")

else:
    print("[!] No account details found or error occurred.")
    exit(1) 


# ====================[PROXY DETAILS]====================
from auth import main, display_proxies


print("[!] Wanna use some proxies? (y/n)\n")
proxy_choice = input("Input: ").lower()
if proxy_choice != 'y':
    client = TelegramClient('session_name', api_id, api_hash)
    pass

else:
    display_proxies()
    proxy_selection = input("[+] Please inter the section number of the proxy : ")
    config = configparser.ConfigParser()
    config.read('proxies.ini')
    try:
        chosen_section = config.sections()[int(proxy_selection) - 1]
        proxy_type = config[chosen_section]['proxy_type']
        addr = config[chosen_section]['addr']
        port = config[chosen_section]['port']
        username = config[chosen_section]['username']
        password = config[chosen_section]['password']
        rdns = config[chosen_section]['rdns']

        # Créer le dictionnaire pour le proxy
        proxy = {
            'proxy_type': proxy_type,
            'addr': addr,
            'port': port,
            'username': username,
            'password': password,
            'rdns': rdns
        }

        # Connexion à Telegram en utilisant le proxy sélectionné
        client = TelegramClient('session_name', api_id, api_hash, proxy=proxy)

    except (ValueError, IndexError, KeyError):
        print("[!] Bad selection for the proxies.")



# ====================[START CLIENT]====================
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input('[+] Enter the code sent from Telegram (to connect your account): '))   



# ==================[ GET GROUPS ]===================
chats = []
last_date = None
chunk_size = 200    
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup==True: 
            groups.append(chat) # +elif chat.broadcast==True: // to add channels
    except:
        continue 


# ==================[ SELECT GROUP ]===================
banner()
print('[+] Choose a group to scrape members:\n')
i=0
for g in groups:
    print('{'+str(i)+'}-> ' + g.title)
    i+=1
g_index=input('\n[+] Enter a Number: ')
target_group=groups[int(g_index)]


# ==================[ SCRAPING PROCESS ]=================
print('[+] Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
print('[+] Saving In file...')


# ==================[ SAVE TO FILE ]=================
Tk().withdraw()
save_path = asksaveasfilename(defaultextension=".csv",
                              filetypes=[("CSV files", "*.csv")],
                              title="Choose location to save members.csv")

if save_path:
    with open(save_path, "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            username = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
    print('[+] Members scraped successfully.\n')
else:
    print('[!] Save operation was cancelled.')
