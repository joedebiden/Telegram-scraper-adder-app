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

    async def open_file(self, input_file):
        if not input_file:
            Tk().withdraw()
            input_file = askopenfilename(
                title="Select file",
                filetype=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )

        if not input_file:
            print("[!] No file selected.")
            return None

        users = []
        try:
            if input_file.endswith('.csv'):
                try:
                    async with asyncio.to_thread(open, input_file, encoding='UTF-8') as f:
                        rows = csv.reader(f, delimiter=",", lineterminator="\n")
                        next(rows, None)
                        for row in rows:
                            try:
                                user = {
                                    'username': row[0],
                                    'id': int(row[1]),
                                    'access_hash': int(row[2]),
                                    'name': row[3]
                                }
                                users.append(user)
                            except (IndexError, ValueError) as e:
                                print(f"[!] Skipping invalid row: {row} | Error: {e}")

                except FileNotFoundError:
                    print("[!] File not found.")
                    return None
                except Exception as e:
                    print(f"[!] Error reading file: {e}")
                    return None

            elif input_file.endswith('.txt'):
                try:
                    async with asyncio.to_thread(open, input_file, 'r', encoding='UTF-8') as f:
                        for line in f:
                            user = {'username': line.strip()}
                            users.append(user)

                except FileNotFoundError:
                    print("[!] File not found.")
                    return None
                except Exception as e:
                    print(f"[!] Error reading file: {e}")
                    return None

            else:
                print("[!] Invalid file format. Use .csv or .txt. Please retry again.")
                return None

        except Exception as e:
            print(f"[!] An error occurred: {e}")
            return None

        return users

    async def get_groups(self):
        if not await self.client.is_user_authorized():
            print("[!] Client not authorized. Connect first.")
            return []

        groups = []
        try:
            result = await self.client(GetDialogsRequest(
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

    async def add_users(self, target_group, users, sleep_time):
        if not users:
            print("[!] No users to add. Aborting...")
            return

        for user in users:
            try:
                if not user.get('id') and not user.get('username'):
                    print("[!] Skipping user with missing ID and username.")
                    continue

                try:
                    if user.get('username'):
                        print(f"[+] Resolving username: {user['username']}")
                        user_to_add = await self.client.get_entity(user['username'])
                    else:
                        print(f"[+] Resolving ID: {user['id']}")
                        user_to_add = await self.client.get_entity(InputPeerUser(int(user['id']), int(user['access_hash'])))
                except Exception as e:
                    print(f"[!] Error resolving user {user.get('username') or user['id']}: {e}")
                    continue

                try:
                    await self.client(InviteToChannelRequest(target_group, [user_to_add]))
                    print(f"[+] Successfully added {user.get('username') or user['id']} to the group.")
                    await asyncio.sleep(randint(sleep_time[0], sleep_time[1]))

                except PeerFloodError:
                    print("[!] Too many requests. PeerFloodError encountered.")
                    break
                except FloodWaitError as e:
                    print(f"[!] FloodWaitError: Wait {e.seconds} seconds.")
                    await asyncio.sleep(e.seconds)
                    continue
                except Exception as e:
                    print(f"[!] Unexpected error: {str(e)}")
                    traceback.print_exc()
                    continue

            except Exception as e:
                print(f"[!] Error adding user: {e}")
                continue
