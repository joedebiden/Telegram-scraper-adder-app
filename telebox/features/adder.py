from __init__ import (
    csv, 
    Tk, 
    sleep, 
    asyncio,
    askopenfilename, 
    randint, 
    GetDialogsRequest, 
    InputPeerEmpty, 
    InviteToChannelRequest, 
    InputPeerUser, 
    PeerFloodError, 
    FloodWaitError, 
    UserPrivacyRestrictedError, 
    UserNotMutualContactError, 
    ChatAdminRequiredError, 
    InputUserDeactivatedError, 
    UserKickedError, 
    ChannelPrivateError, 
    traceback 
    )
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


    def open_file(self, input_file):
        """
        Ouvre un fichier CSV ou TXT contenant les utilisateurs à ajouter.
        """
        if not input_file:
            Tk().withdraw()
            input_file = askopenfilename(
                title = "Select file",
                filetype = [("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
        
        if not input_file:
            print("[!] No file selected.")
            return None
        
        users = []
        try:
            if input_file.endswith('.csv'):
                try: 
                    with open(input_file, encoding='UTF-8') as f:
                        rows = csv.reader(f, delimiter=",",lineterminator="\n")
                        next(rows, None)
                        for row in rows:
                            try:
                                user = {
                                    'username': row[0],
                                    'id' : int(row[1]),
                                    'access_hash' : int(row[2]),
                                    'name' : row[3]
                                }
                                users.append(user)
                                
                            except (IndexError, ValueError) as e:
                                print(f"[!] Skipping invalid row: {row} | Error: {e}")

                except FileNotFoundError as e:
                    print("[!] File not found.")
                    return None
                
                except Exception as e:
                    print(f"[!] Error reading file: {e}")
                    return None
                
            elif input_file.endswith('.txt'):
                try:
                    with open(input_file, 'r', encoding='UTF-8  ') as f:
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
        
        return users


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
            method = int(input("\n[+] Enter a number to select a group: "))
            if method < 0 or method >= len(groups):
                raise ValueError("Invalid choice.")
            return groups[method]
        except ValueError as e:
            print(f"[!] Error selecting group: {e}")
            return None



    def set_speed_mode(self, mode):
            speed_modes = {
                "Very slow": (150, 180),
                "Normal": (60, 80),
                "Fast": (20, 35),
                "Very fast": (1, 5) 
            }
            if mode in speed_modes:
                sleep_time = speed_modes[mode]
                print(f"[+] Speed mode set to {mode}.")
                return sleep_time
            else:
                print("[!] Invalid speed mode.")
                return None



    def add_users(self, target_group, users, sleep_time):
        """
        Ajoute les utilisateurs à un groupe.
        :param target_group: Groupe cible (entité Telegram)
        :param users: Liste des utilisateurs à ajouter
        :param method: Méthode utilisée (1 pour ID, 2 pour username)
        :param sleep_time: Tuple pour le délai entre chaque ajout
        """
        if not users:
            print("[!] No users to add. Aborting...")
            return
        
        for user in users:
            try:
                if not user.get('id') and not user.get('username'):
                    print("[!] Skipping user with missing ID and username.")
                    continue
                
                if user.get('username'):    # Try adding with username first
                    try:
                        print(f"[+] Adding user by username: {user['username']} to group {target_group.title}...")
                        user_to_add = self.client.get_entity(user['username'])
                        
                    except Exception as e:
                        print(f"[!] Error resolving username {user['username']}: {e}")
                        continue
                
                else:   # Else with ID and access_hash
                    try:
                        print(f"[+] Adding user by ID: {user['id']} to group {target_group.title}...")
                        user_to_add = self.client.get_entity(InputPeerUser(int(user['id']), int(user['access_hash'])))
                    except ValueError as e:
                        print(f"[!] Invalid ID or access_hash for user: {user}. Error: {e}")
                        continue
                    except Exception as e:
                        print(f"[!] Error resolving ID {user['id']}: {e}")
                        continue

                try:
                    self.client(InviteToChannelRequest(target_group, [user_to_add]))
                    print(f"Successfully added {user['id']} to the group.")
                    sleep(randint(sleep_time[0], sleep_time[1]))

                except PeerFloodError:
                    print("[!] Too many requests. PeerFloodError encountered.")
                    break

                except FloodWaitError as e:
                    print(f"[!] FloodWaitError: Telegram requires waiting {e.seconds} seconds.")
                    sleep(e.seconds)
                    continue

                except UserPrivacyRestrictedError:
                    print("[!] The user's privacy settings do not allow you to do this. Skipping.")
                    sleep(randint(sleep_time[0], sleep_time[1]))
                    continue

                except UserNotMutualContactError:
                    print(f"[!] Cannot add {user['username']} because they are not a mutual contact. Skipping.")
                    sleep(2)
                    continue
                except ChatAdminRequiredError:
                    print("[!] You need to be an admin to add users to this group. Skipping.")
                    break  # Stop the loop since this is a critical error
                except InputUserDeactivatedError:
                    print(f"[!] The user {user['username']} has deactivated their account. Skipping.")
                    continue
                except UserKickedError:
                    print(f"[!] The user {user['username']} was kicked from the group and cannot be re-added.")
                    continue
                except ChannelPrivateError:
                    print(f"[!] Cannot add user {user['username']} because the channel is private or restricted.")
                    continue
                except ValueError as e:
                    print(f"[!] Unexpected error: {e}")
                    continue 
                except Exception as e:
                    print(f"[!] Unexpected error: {str(e)}")
                    traceback.print_exc() 
                    continue
                
            except Exception as e:
                print(f"[!] Error adding user: {e}")
                continue
