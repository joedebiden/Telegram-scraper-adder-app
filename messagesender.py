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
 _                     _      _       _ 
| |__   __ _ _   _  __| | ___| | __ _(_)_ __ ___
| '_ \ / _` | | | |/ _` |/ _ \ |/ _` | | '__/ _ \,
| |_) | (_| | |_| | (_| |  __/ | (_| | | | |  __/
|_.__/ \__,_|\__,_|\__,_|\___|_|\__,_|_|_|  \___|

 _       _
| |_ ___| | ___  __ _ _ __ __ _ _ __ ___
| __/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \,
| ||  __/ |  __/ (_| | | | (_| | | | | | |
 \__\___|_|\___|\__, |_|  \__,_|_| |_| |_|
                |___/
                    _
 ___  ___ _ __   __| | ___ _ __
/ __|/ _ \ '_ \ / _` |/ _ \ '__|
\__ \  __/ | | | (_| |  __/ |
|___/\___|_| |_|\__,_|\___|_|
''')
    
cpass = configparser.RawConfigParser()
cpass.read('config.data')

# ====================[API DETAILS]=====================
try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
except KeyError:
    banner()
    print("[!] Run python setup.py first !!\n")
    sys.exit(1)


client = TelegramClient(phone, api_id, api_hash)
    

# ====================[START CLIENT]====================
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input('[+] Enter the code sent from Telegram (to connect your account): '))   
banner()

# ajout gestion des erreurs
try:
    input_file = sys.argv[1]
except IndexError:
    print("[!] Use like => python messagesender.py members.csv")
    sys.exit(1)
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
