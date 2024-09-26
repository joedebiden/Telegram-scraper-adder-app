from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

def banner():
    os.system('cls')
    print(f'''
            .▄▄ ·  ▄▄▄· ▄▄▄· • ▌ ▄ ·.     • ▌ ▄ ·. ▄▄▄ ..▄▄ · .▄▄ ·  ▄▄▄·  ▄▄ • ▄▄▄ .▄▄▄  
            ▐█ ▀. ▐█ ▄█▐█ ▀█ ·██ ▐███▪    ·██ ▐███▪▀▄.▀·▐█ ▀. ▐█ ▀. ▐█ ▀█ ▐█ ▀ ▪▀▄.▀·▀▄ █·
            ▄▀▀▀█▄ ██▀·▄█▀▀█ ▐█ ▌▐▌▐█·    ▐█ ▌▐▌▐█·▐▀▀▪▄▄▀▀▀█▄▄▀▀▀█▄▄█▀▀█ ▄█ ▀█▄▐▀▀▪▄▐▀▀▄ 
            ▐█▄▪▐█▐█▪·•▐█ ▪▐▌██ ██▌▐█▌    ██ ██▌▐█▌▐█▄▄▌▐█▄▪▐█▐█▄▪▐█▐█ ▪▐▌▐█▄▪▐█▐█▄▄▌▐█•█▌
             ▀▀▀▀ .▀    ▀  ▀ ▀▀  █▪▀▀▀    ▀▀  █▪▀▀▀ ▀▀▀  ▀▀▀▀  ▀▀▀▀  ▀  ▀ ·▀▀▀▀  ▀▀▀ .▀  ▀
''')
    
# ==================[ CONFIG READER ]==================

cpass = configparser.RawConfigParser()
cpass.read('config.data')
banner()

# ====================[API DETAILS]====================
from account import get_api_details
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
from auth import display_proxies


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
        port = int(config[chosen_section]['port'])
        username = config[chosen_section]['username']
        password = config[chosen_section]['password']


        if proxy_type != 'socks5':
            print("[!] Only socks5 proxy supported.")
            
        else:
            proxy = (proxy_type, addr, port, username, password)

            # connect client with proxy
            client = TelegramClient(
                'session_name',
                api_id,
                api_hash,
                #connection=ConnectionTcpAbridged, 
                proxy=proxy
            )

    except (ValueError, IndexError, KeyError):
        print("[!] Bad selection.")



# ====================[START CLIENT]====================
try:
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('[+] Enter the code sent from Telegram: '))
    print("[+] Connected successful !")
except Exception as e:
    print(f"[!] Error occurred: {e}")


try:
    input_file = sys.argv[1]
except IndexError:
    print("[!] Use like => python adder.py members.csv or members.txt")
    sys.exit(1)



# ====================[OPEN FILE]====================
users = []
try:
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)
except FileNotFoundError:
    print("[!] File not found")
    sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(1)
        

# ===================[SPEED MODES]===============
def presentation():
        print("Before choosing the group, you need to select a mode to message members.\n")
        print("There are 3 modes available: \n")
        print("[1] -> Night Mode (Perfect to take all the night to message members)")
        print("[2] -> Normal Mode")
        print("[3] -> Aggressive Mode (Really not recommended)\n")

def power():
    modes = {
        1: {'name': 'Night Mode', 'SLEEP_TIME_1': 130, 'SLEEP_TIME_2': 150},
        2: {'name': 'Normal Mode', 'SLEEP_TIME_1': 50, 'SLEEP_TIME_2': 70},
        3: {'name': 'Aggressive Mode', 'SLEEP_TIME_1': 20, 'SLEEP_TIME_2': 35}
    }
    presentation()
    while True:
        try:
            mode_selected = int(input("[-] Enter the mode: "))
            if mode_selected in modes:
                mode = modes[mode_selected]
                confirm = input(f'[+] {mode["name"]} selected, are you sure you want to continue? (y/n): ').lower()
                if confirm == 'y':
                    return mode['SLEEP_TIME_1'], mode['SLEEP_TIME_2']
                banner()
                presentation()
            else:
                print("[!] Invalid Mode Selected. Please try again.")
        except ValueError:
            print("[!] Invalid input. Please enter a number (1/2/3).")
SLEEP_TIME_1, SLEEP_TIME_2 = power()



# ==================[MESSAGE MEMBERS]=====================

print("\n [1] send sms by id ")
print(" [2] send sms by username \n")
mode = int(input("Choice : "))
message = input("[+] Enter Your Message : ")

for user in users:
    if mode == 2:
        if user['username'] == "":
            continue
        receiver = client.get_input_entity(user['username'])
    elif mode == 1:
        receiver = InputPeerUser(user['id'],user['access_hash'])
    else:
        print("[!] Invalid Mode. Exiting.")
        client.disconnect()
        sys.exit()
    try:
        print("[+] Sending Message to:", user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("[+] Waiting {} seconds".format(SLEEP_TIME_1))
        time.sleep(random.randrange(SLEEP_TIME_1, SLEEP_TIME_2))
    except PeerFloodError:
        print("[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("[!] Error:", e)
        print("[!] Trying to continue...")
        continue
    
client.disconnect()
banner()
print("Done. Message sent to all users.")
