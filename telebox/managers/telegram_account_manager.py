from __init__ import configparser, os, random

class AccountManager:
    def __init__(self, config_file='account.data'):
        self.config_file = config_file
        self.config = configparser.RawConfigParser()
        
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                pass
        self.config.read(self.config_file)



    def add_account(self, section_name, api_id, api_hash, phone):
        """
        Ajoute un compte Telegram au fichier de configuration. 
        """
        self.config[section_name] = {
            'id': api_id,
            'hash': api_hash,
            'phone': phone
        }
        self.save_config()
        return section_name



    def display_accounts(self):
        """
        Retourne les comptes sous forme de dictionnaire.
        """
        accounts = {}
        for section in self.config.sections():
            accounts[section] = dict(self.config.items(section))
        return accounts



    def edit_account(self, account_name, new_details):
        """
        Met à jour les détails d'un compte existant.
        """
        if account_name in self.config.sections():
            for key, value in new_details.items():
                if value:  # Ne pas remplacer par des valeurs vides
                    self.config.set(account_name, key, value)
            self.save_config()
            return True
        return False



    def delete_account(self, account_name):
        """
        Supprime un compte du fichier de configuration.
        """
        if account_name in self.config.sections():
            self.config.remove_section(account_name)
            self.save_config()
            return True
        return False



    def get_random_account(self):
        """
        Récupère un compte aléatoire depuis le fichier.
        """
        if self.config.sections():
            section = random.choice(self.config.sections())
            return dict(self.config.items(section))
        return None



    def save_config(self):
        """
        Sauvegarde les modifications dans le fichier de configuration.
        """
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
    