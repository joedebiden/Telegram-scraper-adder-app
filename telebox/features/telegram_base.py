from __init__ import ABC, abstractmethod, TelegramClient, configparser

"""
Abstract base class for Telegram clients.
"""

class TelegramBase(ABC):

    def __init__(self, session_name='session_name', api_id=None, api_hash=None, phone=None, proxy=None, config_file='account.data', section_name=None):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.proxy = proxy
        self.client = None
        self.config_file = config_file
        self.section_name = section_name



    def list_accounts(self):
        """
        Affiche la liste des sections disponibles dans le fichier de configuration.
        """
        config = configparser.RawConfigParser()
        config.read(self.config_file)
        sections = config.sections()
        print("[+] Available accounts:")
        for section in sections:
            print(f" - {section}")
        return sections



    def read_account_details(self):
        """
        Lit les détails de l'API (api_id, api_hash, phone) depuis le fichier de config.
        """
        config = configparser.RawConfigParser()
        try: 
            config.read(self.config_file)

            if self.section_name not in config:
                raise KeyError(f"Section '{self.section_name}' not found...")
            
            print(f"[DEBUG] Keys in section '{self.section_name}': {config[self.section_name].keys()}")

            self.api_id = config[self.section_name]['api_id']
            self.api_hash = config[self.section_name]['api_hash']
            self.phone = config[self.section_name]['phone']

            print(f"[+] Account details loaded from section '{self.section_name}':")
            print(f"    api_id: {self.api_id}")
            print(f"    api_hash: {self.api_hash}")
            print(f"    phone: {self.phone}")

        except KeyError as e:
            print(f"[!] Error reading config file '{self.config_file}' section '{self.section_name}': {e}")
            raise
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
            raise



    def connect(self):
        """
        Connecte le client Telegram. Si non autorisé, demande un code pour l'authentification.
        """
        try:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash, proxy=self.proxy)
            self.client.connect()

            if not self.client.is_user_authorized():
                print("[!] Client not authorized. Requesting code...")
                self.client.send_code_request(self.phone)
                code = input('[+] Enter the code sent from Telegram: ')
                self.client.sign_in(self.phone, code)

            print("[+] Connected successfully.")

        except Exception as e:
            print(f"[!] Connection error: {e}")
            raise



    def disconnect(self):
        """Déconnecte le client de Telegram"""
        if self.client:
            self.client.disconnect()
            print("[+] Disconnected.")


    def get_account_info(self):
        """
        Affiche les informations du compte actuellement connecté.
        """
        if self.client and self.client.is_user_authorized():
            me = self.client.get_me()
            print(f"[+] Account Info: Username = {me.username}, Phone = {me.phone}, Name = {me.first_name} {me.last_name}")
        else:
            print("[!] Client is not authorized.")