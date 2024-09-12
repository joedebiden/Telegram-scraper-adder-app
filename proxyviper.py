import configparser
import random
import socks

# Lire les configurations de proxy depuis le fichier
proxy_config = configparser.ConfigParser()
proxy_config.read('proxies.ini')

# Sélectionner un proxy aléatoire
proxy_sections = proxy_config.sections()
selected_proxy = random.choice(proxy_sections)

proxy = (
    socks.SOCKS5, 
    proxy_config[selected_proxy]['host'], 
    int(proxy_config[selected_proxy]['port']),
    True,  # Socks5 avec authentification
    proxy_config[selected_proxy].get('username'), 
    proxy_config[selected_proxy].get('password')
)
