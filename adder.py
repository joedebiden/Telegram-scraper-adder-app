from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.sync import TelegramClient 
from telethon.errors import (
    PeerFloodError, 
    UserPrivacyRestrictedError, 
    FloodWaitError, 
    UserNotMutualContactError,
    ChatAdminRequiredError, 
    InputUserDeactivatedError,
    UserKickedError, 
    ChannelPrivateError)
import sys
import csv
import traceback
import time
import random
import configparser
import os


def banner():
    os.system('cls')
    print(r'''

          ______               __                 ______         __        __                     
         /      \             /  |               /      \       /  |      /  |                    
        /$$$$$$  | __    __  _$$ |_     ______  /$$$$$$  |  ____$$ |  ____$$ |  ______    ______  
        $$ |__$$ |/  |  /  |/ $$   |   /      \ $$ |__$$ | /    $$ | /    $$ | /      \  /      \ 
        $$    $$ |$$ |  $$ |$$$$$$/   /$$$$$$  |$$    $$ |/$$$$$$$ |/$$$$$$$ |/$$$$$$  |/$$$$$$  |
        $$$$$$$$ |$$ |  $$ |  $$ | __ $$ |  $$ |$$$$$$$$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
        $$ |  $$ |$$ \__$$ |  $$ |/  |$$ \__$$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |$$$$$$$$/ $$ |      
        $$ |  $$ |$$    $$/   $$  $$/ $$    $$/ $$ |  $$ |$$    $$ |$$    $$ |$$       |$$ |      
        $$/   $$/  $$$$$$/     $$$$/   $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/ $$/       
                                                                                          
                                                                     
          ''')

banner()
cpass = configparser.RawConfigParser()
cpass.read('config.data')

# ====================[API DETAILS]====================
from account import get_api_details
details = get_api_details()

if details:
    account_name = details['account_name']
    api_id = details['api_id']
    api_hash = details['hash']
    phone = details['phone']
    
    print(f"Random account: [{account_name}] \n, API ID: {api_id}\n, Hash: {api_hash}\n, Phone: {phone}\n")

else:
    print("[!] No account details found or error occurred.")
    exit(1) 


# ====================[SWAP ACCOUNT]====================
def swap_account(client, config='config.data'):
    client.disconnect()
    details = get_api_details()

    if details:
        account_name = details['account_name']
        api_id = details['api_id']
        api_hash = details['hash']
        phone = details['phone']

        print(f"[+] Account swapped: [{account_name}]\n, API ID: {api_id}\n, Hash: {api_hash}\n, Phone: {phone}\n")

        new_client = TelegramClient('session_name', api_id, api_hash)

        new_client.connect()
        if not new_client.is_user_authorized():
            new_client.send_code_request(phone)
            new_client.sign_in(phone, input('\n[+] Enter the code sent from Telegram: '))

        print("[*] Successfully connected")
        return new_client
    else:
        print("[!] No account details founds or error occurred during the swap.")
        return None

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
    print("[+] Connected!")
except Exception as e:
    print(f"[!] Error occurred: {e}")



try:
    input_file = sys.argv[1]
except IndexError:
    print("[!] Please enter the file that contains members list => (members.csv or members.txt)")
    input("Press the Enter key to continue...") 
    sys.exit(1)


# ====================[OPEN FILE]====================
users = []
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
        print("[!] Check the file extension and try again (its a commun bug on windows).")
        input("Press the Enter key to continue...")
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
    if n % 48 == 0: 
        print("[!] Waiting for 10 minutes... (every 48 users)...")
        time.sleep(660) 
    try: 
        if mode == 1:
            if 'username' in user and user['username']:
                print(f"Adding {user['username']} to group {target_group.title}")
                user_to_add = client.get_input_entity(user['username'])
            else:
                print(f"[!] Username not found for {user}, skipping...")
                continue

        elif mode == 2:
            user_to_add = client.get_entity(InputPeerUser(user['id'], user['access_hash']))
        else:
            sys.exit("[!] Invalid Mode Selected. Please Try Again.")

        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print(f"Successfully added {user['username'] if mode == 1 else user['id']} to the group.")
        time.sleep(random.randrange(SLEEP_TIME_1, SLEEP_TIME_2))

    except PeerFloodError as e: 
        print("[!] Too many requests to Telegram. PeerFloodError encountered.")
        print(f"Error details: {e}")
        print("[!] Switching to another account...")
        client = swap_account(client)
        if client is None:
            print("\n[!] Failed to swap.")
            continue
        continue
    
    except FloodWaitError as e:
        print(f"[!] FloodWaitError: Telegram is forcing a wait time of {e.seconds} seconds.")
        if e.seconds > 301:
            print("[!] Long wait time detected => switching account...")
            client = swap_account(client)
            if client is None:
                print("\n[!] Failed to swap. Continue without swap")
                continue
            continue
        else:
            time.sleep(e.seconds)
        continue

    except UserPrivacyRestrictedError:
        print("[!] The user's privacy settings do not allow you to do this. Skipping.")
        time.sleep(random.randrange(SLEEP_TIME_1, SLEEP_TIME_2))
        continue

    except UserNotMutualContactError:
        print(f"[!] Cannot add {user['username'] if mode == 1 else user['id']} because they are not a mutual contact. Skipping.")
        continue

    except ChatAdminRequiredError:
        print("[!] You need to be an admin to add users to this group. Skipping.")
        break  # Stop the loop since this is a critical error

    except InputUserDeactivatedError:
        print(f"[!] The user {user['username'] if mode == 1 else user['id']} has deactivated their account. Skipping.")
        continue

    except UserKickedError:
        print(f"[!] The user {user['username'] if mode == 1 else user['id']} was kicked from the group and cannot be re-added.")
        continue

    except ChannelPrivateError:
        print(f"[!] Cannot add user {user['username'] if mode == 1 else user['id']} because the channel is private or restricted.")
        continue

    except ValueError as e:
        print(f"[!] Unexpected error: {e}")
        continue 

    except Exception as e:
        print(f"[!] Unexpected error: {str(e)}")
        traceback.print_exc() 
        continue
