from __init__ import configparser, os

class AccountManager():
    # constructeur
    def __init__(self, config_file='accounts.data'):
        self.config_file = config_file
        self.config = configparser.RawConfigParser()
        
        # Initialiser le fichier de configuration s'il n'existe pas
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                pass

        self.config.read(self.config_file)
    
    

    # add account in file (or sqlite db ?)
    def add_account(self, api_id, api_hash, phone):
        section_name = f"account{len(self.config.sections()) + 1}"
        self.config[section_name] = {
            'id': api_id,
            'hash': api_hash,
            'phone': phone
        }
        self.save_config()
        return section_name

    def edit_account():
        return
    
    def delete_account():
        return
    
    def display_accounts():
        return
    
    