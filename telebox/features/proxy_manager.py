from __init__ import configparser, os, random


class ProxyManager:
    def __init__(self, config_file='proxies.ini'):
        """
        Initialise le gestionnaire de proxy en vérifiant la présence du fichier de configuration.
        """
        self.config_file = config_file
        self.config = configparser.RawConfigParser()

        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                pass
        self.config.read(self.config_file)



    def add_proxy(self, section_name, proxy_type, addr, port, username=None, password=None, rdns=True):
        """
        Ajoute un proxy au fichier de configuration.
        """
        self.config[section_name] = {
            'proxy_type': proxy_type,
            'addr': addr,
            'port': str(port),
            'username': username or 'None',
            'password': password or 'None',
            'rdns': rdns
        }
        self.save_config()  
        return section_name



    def display_proxies(self):
        """
        Retourne les proxys sous forme de dictionnaire.
        """
        proxies = {}
        for section in self.config.sections():
            proxies[section] = dict(self.config.items(section))
        return proxies



    def edit_proxy(self, proxy_name, new_details):
        """
        Met à jour les détails d'un proxy existant.
        """
        if proxy_name in self.config.sections():
            for key, value in new_details.items():
                if value:  # Ne pas remplacer par des valeurs vides
                    self.config.set(proxy_name, key, str(value))
            self.save_config()
            return True
        return False



    def delete_proxy(self, proxy_name):
        """
        Supprime un proxy du fichier de configuration.
        """
        if proxy_name in self.config.sections():
            self.config.remove_section(proxy_name)
            self.save_config()
            return True
        return False



    def get_random_proxy(self):
        """
        Récupère un proxy aléatoire depuis le fichier.
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
