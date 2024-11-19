"""
Work very in terminal to use ProxyManager class
$ .venv/Scripts/python.exe -m telebox.tests.test_proxy_manager
"""
from ..managers.proxy_manager import ProxyManager
from __init__ import sleep

if __name__ == "__main__":
    proxy_manager = ProxyManager()

    """
    # Ajouter un proxy
    proxy_manager.add_proxy(
        section_name="proxy1",
        proxy_type="socks5",
        addr="127.0.0.1",
        port=8080,
        username="user1",
        password="pass1",
        rdns=True
    )
    # Afficher les proxys
    print(proxy_manager.display_proxies())
    # Modifier un proxy
    proxy_manager.edit_proxy("proxy1", {"port": 9090, "rdns": False})
    # Supprimer un proxy
    proxy_manager.delete_proxy("proxy1")
    # Récupérer un proxy aléatoire
    random_proxy = proxy_manager.get_random_proxy()
    print(random_proxy)
    """

    while True:
        print("\n[*] Proxy Account Manager\n")
        print("1. Display Proxies")
        print("2. Add a Proxy")
        print("3. Edit a Proxy")
        print("4. Delete a Proxy")
        print("5. Quit")

        choice = input("Please choose your action (1/2/3/4/5): ")

        if choice == '1':
            proxies = proxy_manager.display_proxies()
            if proxies:
                print("\n[+] Existing proxy:")
                for name, details in proxies.items():
                    print(f"{name}: {details}")
            else:
                print("[!] No proxy found.")

        elif choice == '2':
            proxy_name = input("[+] Enter the proxy name: ")
            proxy_type = input("[+] Enter the proxy type: ")
            addr = input("[+] Enter the address: ")
            port = input("[+] Enter the port: ")
            username = input("[+] Enter the username (leave blank to skip): ")
            password = input("[+] Enter the password (leave blank to skip): ")
            rdns = input("[+] Enable RDNS? (True/False): ")
            add_account = proxy_manager.add_proxy(proxy_name, proxy_type, addr, port, username, password, rdns)
            print(f"[+] Proxy '{proxy_name}' added successfully!")


        elif choice == '3':
            proxy_name = input("[+] Enter the proxy name to edit: ")
            new_proxy_type = input("New Proxy Type (leave blank to keep current): ")
            new_addr = input("New Address (leave blank to keep current): ")
            new_port = input("New Port (leave blank to keep current): ")
            new_username = input("New Username (leave blank to keep current): ")
            new_password = input("New Password (leave blank to keep current): ")
            new_rdns = input("New RDNS (leave blank to keep current): ")
            updated = proxy_manager.edit_proxy(proxy_name, {
                'proxy_type': new_proxy_type,
                'addr': new_addr,
                'port': new_port,
                'username': new_username,
                'password': new_password,
                'rdns': new_rdns
            })
            if updated:
                print(f"[+] Proxy '{proxy_name}' updated successfully!")
            else:
                print("[!] Proxy not found.")


        elif choice == '4':
            proxy_name = input("[+] Enter the proxy name to delete: ")
            deleted = proxy_manager.delete_proxy(proxy_name)
            if deleted:
                print(f"[+] Proxy '{proxy_name}' deleted successfully!")
            else:
                print("[!] Proxy not found.")

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("[!] Invalid choice!")
        sleep(1)