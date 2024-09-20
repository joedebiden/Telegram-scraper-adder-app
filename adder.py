from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.sync import TelegramClient 
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import sys
import csv
import traceback
import time
import random
import configparser
import os


def banner():
    os.system('cls')
    print(f'''
 ____                  _      _       _
| __ )  __ _ _   _  __| | ___| | __ _(_)_ __ ___
|  _ \ / _` | | | |/ _` |/ _ \ |/ _` | | '__/ _ \,
| |_) | (_| | |_| | (_| |  __/ | (_| | | | |  __/
|____/ \__,_|\__,_|\__,_|\___|_|\__,_|_|_|  \___|
    _         _          _       _     _
   / \  _   _| |_ ___   / \   __| | __| | ___ _ __
  / _ \| | | | __/ _ \ / _ \ / _` |/ _` |/ _ \ '__|
 / ___ \ |_| | || (_) / ___ \ (_| | (_| |  __/ |
/_/   \_\__,_|\__\___/_/   \_\__,_|\__,_|\___|_|          

          ''')

cpass = configparser.RawConfigParser()
cpass.read('config.data')

# ====================[API DETAILS]====================
try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
except KeyError:
    banner()
    print("[!] Run python setup.py first !!\n")
    sys.exit(1)


# ====================[PROXY DETAILS]====================
from auth import main, test_proxy, display_proxies, add_proxy

banner()
print("[!] Wanna use some proxies? (y/n)\n")
proxy_choice = input("Input: ").lower()
if proxy_choice != 'y':
    client = TelegramClient('session_name', api_id, api_hash)
    pass

else:
    proxy = main()
    client = TelegramClient('session_name', api_id, api_hash, proxy=proxy)


## need to work on this part 
# je dois implémenter mon application et pas que le main, demande a gpt


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
    print("[!] Use like => python adder.py members.csv or members.txt")
    sys.exit(1)
users = []


# ====================[OPEN FILE]====================
#new task, check the file before processing

try:
    if input_file.endswith('.csv'):
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

    elif input_file.endswith('.txt'):
        with open(input_file, encoding='UTF-8') as f:
            for line in f:
                user = {}
                username = line.strip()
                user['username'] = username
                users.append(user)

    else:
        print("[!] Unsupported file format. Please use a CSV or TXT file.")
        sys.exit(1)
except FileNotFoundError:
    print("[!] File not found")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)


chats = []
last_date = None
chunk_size = 200
groups = []


# ===================[SPEED MODES]===============
def presentation():
        print("Before choosing the group, you need to select a mode to add members.\n")
        print("There are 3 modes available: \n")
        print("[1] -> Night Mode (Perfect to take all the night to add members)")
        print("[2] -> Normal Mode")
        print("[3] -> Aggressive Mode (Really not recommended)\n")
        print("[4] -> Idiot Mode (You're a real idiot if you choose this mode)\n")

def power():
    #dictionnaire
    modes = {
        1: {'name': 'Night Mode', 'SLEEP_TIME_1': 150, 'SLEEP_TIME_2': 180},
        2: {'name': 'Normal Mode', 'SLEEP_TIME_1': 60, 'SLEEP_TIME_2': 80},
        3: {'name': 'Aggressive Mode', 'SLEEP_TIME_1': 20, 'SLEEP_TIME_2': 35},
        4: {'name': 'Idiot Mode', 'SLEEP_TIME_1': 1, 'SLEEP_TIME_2': 5}
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
            print("[!] Invalid input. Please enter a number (1/2/3/4).")
# Appel de la fonction power et récupération des valeurs
SLEEP_TIME_1, SLEEP_TIME_2 = power()

# ====================[GET GROUPS]====================

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True: # groups
            groups.append(chat)
        elif chat.broadcast == True: # channels
            groups.append(chat)
    except:
        continue

# ====================[CHOOSING GROUP]====================

i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1
g_index = input("\nChoose a group to add members. Enter a Number: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)


print("[1] add member by username\n[2] add member by ID ")
mode = int(input("Input : ")) 

# ====================[ADD MEMBERS]====================
n = 0
for user in users:
    n += 1
    if n % 50 == 0: 
        time.sleep(300) 
    try: 
        #print("Adding {}".format(user['id']))

        if mode == 1:
            if 'username' in user and user['username']:
                print(f"Adding {user['username']} to group {target_group.title}")
                user_to_add = client.get_input_entity(user['username'])
            else:
                print(f"[!] Username not found for {user}")
                continue

        elif mode == 2:
            user_to_add = client.get_entity(InputPeerUser(user['id'], user['access_hash']))
        else:
            sys.exit("[!] Invalid Mode Selected. Please Try Again.")

        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting...\n")
        time.sleep(random.randrange(SLEEP_TIME_1, SLEEP_TIME_2))

    #mon pire cauchemar
    except PeerFloodError as e: #to do a better error handling !
        # Capture and print all details related to the PeerFloodError
        print("[!] Getting Flood Error from telegram.")
        print(f"Error details: {e}")  # Print the error message
        print(f"Error arguments: {e.args}")  # Print the arguments of the exception
        time.sleep(random.randrange(SLEEP_TIME_1, SLEEP_TIME_2))
        
    # except FloodWaitError as e: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! to do 

    except UserPrivacyRestrictedError:
        print("[!] The user's privacy settings do not allow you to do this. Skipping.")
        time.sleep(random.randrange(SLEEP_TIME_1, SLEEP_TIME_2))

    except:
        traceback.print_exc()
        print("[!] Unexpected Error")
        continue
