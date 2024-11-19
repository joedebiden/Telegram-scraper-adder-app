"""
Work very in terminal to use AccountManager class
"""
from ..managers.telegram_account_manager import AccountManager
from __init__ import sleep




# ======================[TEST DE LA CLASSE]==========================
if __name__ == "__main__":
    manager = AccountManager()

    while True:
        print("\n[*] Telegram Account Manager\n")
        print("1. Display Accounts")
        print("2. Add an Account")
        print("3. Edit an Account")
        print("4. Delete an Account")
        print("5. Quit")

        choice = input("Please choose your action (1/2/3/4/5): ")

        if choice == '1':
            accounts = manager.display_accounts()
            if accounts:
                print("\n[+] Existing Accounts:")
                for name, details in accounts.items():
                    print(f"{name}: {details}")
            else:
                print("[!] No accounts found.")

        elif choice == '2':
            section_name = input("[+] Enter the account name: ")
            api_id = input("[+] Enter the API ID: ")
            api_hash = input("[+] Enter the API Hash: ")
            phone = input("[+] Enter the phone number: ")
            add_account = manager.add_account(section_name, api_id, api_hash, phone)
            print(f"[+] Account '{section_name}' added successfully!")

        elif choice == '3':
            account_name = input("[+] Enter the account name to edit: ")
            new_api_id = input("New API ID (leave blank to keep current): ")
            new_api_hash = input("New API Hash (leave blank to keep current): ")
            new_phone = input("New Phone (leave blank to keep current): ")
            updated = manager.edit_account(account_name, {
                'id': new_api_id,
                'hash': new_api_hash,
                'phone': new_phone
            })
            if updated:
                print(f"[+] Account '{account_name}' updated successfully!")
            else:
                print("[!] Account not found.")

        elif choice == '4':
            account_name = input("[+] Enter the account name to delete: ")
            deleted = manager.delete_account(account_name)
            if deleted:
                print(f"[+] Account '{account_name}' deleted successfully!")
            else:
                print("[!] Account not found.")

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("[!] Invalid choice!")
        sleep(1)