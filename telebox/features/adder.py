from __init__ import csv, sleep, randint, GetDialogsRequest, InputPeerEmpty, InviteToChannelRequest, InputPeerUser, PeerFloodError, FloodWaitError
from .telegram_base import TelegramBase

class Adder(TelegramBase):
    
    def __init__(self, session_name='session_name', api_id=None, api_hash=None, phone=None, proxy=None, config_file='account.data', section_name='default'):
        super().__init__(session_name=session_name, api_id=api_id, api_hash=api_hash, phone=phone, proxy=proxy, config_file=config_file, section_name=section_name)

    """Adding in order :
    connect client
    open file with users
    get groups
    select group
    choosing method (id or username)
    choosing speed process
    add users
    """


    def open_file(self, input_file=None):
        """
        Ouvre un fichier CSV contenant les utilisateurs à ajouter.
        """
        users = []
        try:
            if input_file.endswith('.csv'):
                try: 
                    with open(input_file, encoding='UTF-8') as f:
                        rows = csv.reader(f, delimiter=",",lineterminator="\n")
                        next(rows, None)
                        for row in rows:
                            user = {}
                            user['username'] = row[0]
                            user['id'] = int(row[1])
                            user['access_hash'] = int(row[2])
                            user['name'] = row[3]
                            users.append(user)

                except FileNotFoundError as e:
                    print("[!] File not found.")
                    return None
                
                except Exception as e:
                    print(f"[!] Error reading file: {e}")
                    return None
                
            elif input_file.endwith('.txt'):
                try:
                    with open(input_file, 'r') as f:
                        for line in f:
                            user = {}
                            user['username'] = line.strip()
                            users.append(user)

                except FileNotFoundError as e:
                    print("[!] File not found.")
                    return None
                
                except Exception as e:
                    print(f"[!] Error reading file: {e}")
                    return None
                
            else:
                print("[!] Invalid file format. Use .csv or .txt. Please retry again.")
                return None
                
        except Exception as e:
            print(f"[!] An error occured: {e}")
            return None



    def get_groups(self):
        """
        Retourne une liste de groupes et de chaines dispo dans les dialogues de l'utilisateur
        """
        if not self.client.is_user_authorized():
            print("[!] Client not authorized. Connect first.")
            return []
        
        groups = []
        try:
            result = self.client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))
            for chat in result.chats:
                if getattr(chat, 'megagroup', False) or getattr(chat, 'broadcast', False):
                    groups.append(chat)
            print(f"[+] {len(groups)} groups/channels found.")

        except Exception as e:
            print(f"[!] Error while fetching groups: {e}")
        return groups
    


    def select_group(self, groups):
        """
        Sélectionne un groupe ou une chaîne à partir de la liste.
        """
        if not groups:
            print("[!] No groups available.")
            return None

        print("\n[+] Available Groups:")
        for i, group in enumerate(groups):
            print(f"{i} -> {group.title}")

        try:
            choice = int(input("\n[+] Enter a number to select a group: "))
            if choice < 0 or choice >= len(groups):
                raise ValueError("Invalid choice.")
            return groups[choice]
        except ValueError as e:
            print(f"[!] Error selecting group: {e}")
            return None
        


    def choose_method(self):
        """
        Choisissez la méthode pour ajouter les utilisateurs.
        """
        print("\n[+] Choose method to add users:")
        print("1 -> By ID")
        print("2 -> By Username")
        try:
            choice = int(input("\n[+] Enter a number to select a method: "))
            if choice < 1 or choice > 2:
                raise ValueError("Invalid choice.")
            return choice
        except ValueError as e:
            print(f"[!] Error selecting method: {e}")
            return None
        


    def set_speed_mode(self, mode):
            modes = {
                1: (150, 180),  # Night Mode
                2: (60, 80),    # Normal Mode
                3: (20, 35),    # Fast Mode
                4: (1, 5)       # Aggressive Mode
            }
            self.sleep_time = modes.get(mode, (60, 80))
            print(f"[+] Speed mode set to {mode}: Sleep time {self.sleep_time}")



    def add_users(self, target_group, users, choice):
        """
        Ajoute les utilisateurs à un groupe.
        """
        for user in users:
            try:
                if choice == 1:
                    user_to_add = self.client.get_entity(InputPeerUser(user['id'], user['access_hash']))

                if not user.get('id') and not user.get('username'):
                        print("[!] Skipping user with missing ID and username.")
                        continue
                
                else:
                    if 'username' in user and user['username']:
                        print(f"[+] Adding {user['username']} to group {target_group.title}...")
                        user_to_add = self.client.get_entity(user['username'])
                    else:
                        print(f"[!] Username not found for user: {user['id']}")
                        continue

                try:
                    self.client(InviteToChannelRequest(target_group, [user_to_add]))
                    print(f"Successfully added {user['username'] if choice == 1 else user['id']} to the group.")
                    sleep(randint(self.sleep_time[0], self.sleep_time[1]))

                except PeerFloodError as e: 
                    print("[!] Too many requests to Telegram. PeerFloodError encountered.")
                    print(f"Error details: {e}")                    
                    continue
                
                except FloodWaitError as e:
                    print(f"[!] FloodWaitError: Telegram is forcing a wait time of {e.seconds} seconds.")
                    sleep(e.seconds)
                    continue
                
            except Exception as e:
                print(f"[!] Error adding user: {e}")
                return None