from __init__ import InputPeerEmpty
from pyrogram import Client



class TelegramBase:
    def __init__(self, session_name, proxy=None):
        self.session_name = session_name
        self.proxy = proxy
        self.client = None

    # for connecting to telegram need api_id, api_hash, phone (maybe add them in parameter) ?
    def connect(self):
        from telethon import TelegramClient
        try:
            self.client = TelegramClient(self.session_name, api_id, api_hash, proxy=self.proxy)
            self.client.connect()
            if not self.client.is_user_authorized():
                self.client.send_code_request(phone)
                self.client.sign_in(phone, input('[+] Enter the code sent from Telegram: '))
        except Exception as e:
            print(f"[!] Error occurred: {e}")


    def disconnect(self):
        if self.client:
            self.client.disconnect()
    

    # get all groups and channels
    def get_groups(self):
        chats = []
        groups = []
        result = self.client.get_dialogs(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0
        )
        chats.extend(result.chats)
        for chat in chats:
            try:
                if chat.megagroup:
                    groups.append(chat)
                elif chat.broadcast:
                    groups.append(chat)
            except:
                continue
        return groups