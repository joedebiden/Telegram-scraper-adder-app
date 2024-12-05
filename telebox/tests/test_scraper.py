"""
Work very in terminal to use scraper class
$ python.exe -m tests.test_scraper
"""
from features.scraper import Scraper


# ======================[TEST DE LA CLASSE]==========================
"""test process in order :
    list telegram account in 'account.data'
    select an account 
    connect client
    get groups
    select group
    scraping process
    save file path"""

if __name__ == "__main__":
    
    scraper = Scraper(session_name='session_name', config_file='account.data')
    available_accounts = scraper.list_accounts()


    section_name = input("[+] Enter the account name to use: ")
    if section_name not in available_accounts:
        print("[!] Account not found.")
    else:
        scraper.section_name = section_name
        scraper.read_account_details()

    scraper.connect()
    scraper.get_account_info()

    groups = scraper.get_groups()
    if not groups: 
        print("[!] No groups available.")
        scraper.disconnect()
        exit()

    target_group = scraper.select_group(groups)
    if not target_group:
        print("[!] No group selected.")
        scraper.disconnect()
        exit()

    members = scraper.scrape_group_members(target_group)
    if not members:
        print("[!] No members found.")
        scraper.disconnect()
        exit()
    
    scraper.save_members_to_file(members, target_group.title)

    scraper.disconnect()