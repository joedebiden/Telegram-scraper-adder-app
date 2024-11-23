from __init__ import ABC, abstractmethod, TelegramClient, GetDialogsRequest, InputPeerEmpty, configparser

"""
Abstract base class for Telegram clients.
"""
class TelegramBase(ABC):
    def __init__(self, session_name, api_id, api_hash, phone=None, proxy=None, config_file='account.data'):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.proxy = proxy
        self.client = None
        self.read_account_details(config_file)


    # Méthode incorecte ! Utiliser les méthodes dans la telegram_account_manager 
    def read_account_details(self, config_file):
        """
        Lit les détails de l'API (api_id, api_hash, phone) depuis un fichier de configuration.
        """
        config = configparser.RawConfigParser()
        try:
            config.read(config_file)
            self.api_id = int(config['default']['api_id'])
            self.api_hash = config['default']['api_hash']
            self.phone = config['default']['phone']
            print(f"[+] Account details loaded: Phone = {self.phone}")
        except Exception as e:
            print(f"[!] Error reading config file '{config_file}': {e}")
            raise



    def connect(self):
        """
        Connecte le client Telegram. Si non autorisé, demande un code pour l'authentification.
        """
        try:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash, proxy=self.proxy)
            self.client.connect()
            if not self.client.is_user_authorized():
                self.client.send_code_request(self.phone)
                self.client.sign_in(self.phone, input('[+] Enter the code sent from Telegram: '))
        except Exception as e:
            print(f"[!] Connection error: {e}")
            raise



    def disconnect(self):
        """Déconnecte le client Telegram."""
        if self.client:
            self.client.disconnect()



    def get_groups(self):
        """
        Retourne une liste de groupes et de chaînes disponibles dans les dialogues de l'utilisateur.
        """
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
        except Exception as e:
            print(f"[!] Error while fetching groups: {e}")
        return groups
