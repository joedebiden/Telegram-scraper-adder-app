from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from dotenv import load_dotenv
import os, sys
import configparser
import csv

load_dotenv()

# linux terminal edition 
def banner():
    os.system('clear')
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

 ___  ___ _ __ __ _ _ __   ___ _ __
/ __|/ __| '__/ _` | '_ \ / _ \ '__|
\__ \ (__| | | (_| | |_) |  __/ |
|___/\___|_|  \__,_| .__/ \___|_|
                   |_|
''')

# ==================[ CONFIG READER ]==================

cpass = configparser.RawConfigParser()
cpass.read('config.data') #change parce que j'ai mis les dosssiers dans le folder
try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    banner()
    print("[!] run python setup.py -c first !!\n")
    sys.exit(1)

# ==================[ CONNECT CLIENT ]===================
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input('[+] Enter the code: '))


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
# without tkinter to get saving file in terminal
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
print('[+] Members scraped successfully.\n')
print('[+] Carefull the file saved automatically and replace the members.csv (so it remove if you dont change the name or the path)\n')
