from telebox.managers.telegram_account_manager import AccountManager
# from telebox.features.scraper import Scraper
# from telebox.features.adder import Adder





if __name__ == "__main__":
    manager = AccountManager()

    # test erreur display accounts
    """
    accounts = manager.display_accounts()
    if accounts:
        print("\n[+] Existing Accounts:")
        for name, details in accounts.items():
            print(f"{name}: {details}")
    else:
        print("[!] No accounts found.")
    """

    section_name = manager.add_account(12641519, "b1d9376e2825cf869149f6ba6ced114f", +33772240484)
    print(f"[+] Account '{section_name}' added successfully!")

    # test affichage compte 
    """
    accounts = manager.display_accounts()
    if accounts:
        print("\n[+] Existing Accounts:")
        for name, details in accounts.items():
            print(f"{name}: {details}")
    else:
        print("[!] No accounts found.")
    """