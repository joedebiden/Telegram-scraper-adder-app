import configparser
import os

config_file = 'config.data'

if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        f.write('')

cpass = configparser.ConfigParser()
cpass.read(config_file)


# ====================[FUNCTION DISPLAY ACCOUNTS]====================
def display_accounts():
    if len(cpass.sections()) == 0:
        print("[!] No accounts found")
    else:
        print("[*] Comptes Telegram disponibles :")
        for index, section in enumerate(cpass.sections(), 1):
            print(f"{index}. {section}")


# ====================[FUNCTION ADD ACCOUNT]====================
def add_account():
    account_name = input("[+] Nom du compte : ")
    if account_name in cpass.sections():
        print("[!] Ce compte existe déjà. Choisissez un autre nom.")
        return
    
    cpass.add_section(account_name)
    xid = input("[+] Entrez l'API ID : ")
    xhash = input("[+] Entrez le hash ID : ")
    xphone = input("[+] Entrez le numéro de téléphone : ")
    
    cpass.set(account_name, 'id', xid)
    cpass.set(account_name, 'hash', xhash)
    cpass.set(account_name, 'phone', xphone)
    
    with open(config_file, 'w') as configfile:
        cpass.write(configfile)
    print(f"[+] Compte '{account_name}' ajouté avec succès !")


# ====================[FUNCTION EDIT ACCOUNT]====================
def modify_account():
    display_accounts()
    account_name = input("[*] Entrez le nom du compte à modifier : ")
    if account_name not in cpass.sections():
        print("[!] Ce compte n'existe pas.")
        return

    xid = input(f"[+] Entrez le nouvel API ID (actuel : {cpass.get(account_name, 'id')}): ") or cpass.get(account_name, 'id')
    xhash = input(f"[+] Entrez le nouvel hash ID (actuel : {cpass.get(account_name, 'hash')}): ") or cpass.get(account_name, 'hash')
    xphone = input(f"[+] Entrez le nouveau numéro de téléphone (actuel : {cpass.get(account_name, 'phone')}): ") or cpass.get(account_name, 'phone')
    
    cpass.set(account_name, 'id', xid)
    cpass.set(account_name, 'hash', xhash)
    cpass.set(account_name, 'phone', xphone)
    
    with open(config_file, 'w') as configfile:
        cpass.write(configfile)
    print(f"[+] Compte '{account_name}' modifié avec succès !")


# ====================[FUNCTION DELETE ACCOUNTS]====================
def delete_account():
    display_accounts()
    account_name = input("[*] Entrez le nom du compte à supprimer : ")
    if account_name not in cpass.sections():
        print("[!] Ce compte n'existe pas.")
        return
    
    confirm = input(f"Êtes-vous sûr de vouloir supprimer le compte '{account_name}' ? (oui/non) : ").lower()
    if confirm == 'oui':
        cpass.remove_section(account_name)
        with open(config_file, 'w') as configfile:
            cpass.write(configfile)
        print(f"[+] Compte '{account_name}' supprimé avec succès !")
    else:
        print("[*] Suppression annulée.")



# ====================[MAIN MENU]====================
while True:
    print("\n[*] Gestion des comptes Telegram")
    print("1. Afficher les comptes")
    print("2. Ajouter un compte")
    print("3. Modifier un compte")
    print("4. Supprimer un compte")
    print("5. Quitter")

    choice = input("Choisissez une option (1-5) : ")

    if choice == '1':
        display_accounts()
    elif choice == '2':
        add_account()
    elif choice == '3':
        modify_account()
    elif choice == '4':
        delete_account()
    elif choice == '5':
        print("[*] Quitter le programme.")
        break
    else:
        print("[!] Choix invalide. Veuillez réessayer.")




'''
with open('config.data', 'w') as f:
    f.write('')
print("[*] Please connect you to https://my.telegram.org/ \n")
cpass = configparser.RawConfigParser()
cpass.add_section('cred')
xid = input("[+] enter api ID : ")
cpass.set('cred', 'id', xid)
xhash = input("[+] enter hash ID : ")
cpass.set('cred', 'hash', xhash)
xphone = input("[+] enter phone number : ")
cpass.set('cred', 'phone', xphone)
setup = open('config.data', 'w')
cpass.write(setup)
setup.close()
print("[+] setup complete !")
'''
# ==================[END]====================
# Code Create by @Joedebiden on github or Baudelaire for the intime ;) 
# please dont reverse this shit