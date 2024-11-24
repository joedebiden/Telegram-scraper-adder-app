from __init__ import csv, Tk, asksaveasfilename, GetDialogsRequest, InputPeerEmpty
from .telegram_base import TelegramBase

class Scraper(TelegramBase):
    def __init__(self, session_name='session_name', api_id=None, api_hash=None, phone=None, proxy=None, config_file='account.data', section_name='default'):
        super().__init__(session_name=session_name, api_id=api_id, api_hash=api_hash, phone=phone, proxy=proxy, config_file=config_file, section_name=section_name)

    """Scraping in order :
    connect client
    get groups
    select group
    scraping process
    save file path"""

    def get_groups(self):
        """
        Retourne une liste de groupes et de chaines dispo dans les dialogues de l'utilisateur
        """
        if not self.client.is_user_authorized():
            print("[!] Client not authorized. Connect first.")
            return []
        
        groups = []
        try:
            result = self.client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))
            for chat in result.chats:
                if getattr(chat, 'megagroup', False) or getattr(chat, 'broadcast', False):
                    groups.append(chat)
            print(f"[+] {len(groups)} groups/channels found.")

        except Exception as e:
            print(f"[!] Error while fetching groups: {e}")
        return groups



    def select_group(self, groups):
        """
        Sélectionne un groupe ou une chaîne à partir de la liste.
        """
        if not groups:
            print("[!] No groups available.")
            return None

        print("\n[+] Available Groups:")
        for i, group in enumerate(groups):
            print(f"{i} -> {group.title}")

        try:
            choice = int(input("\n[+] Enter a number to select a group: "))
            if choice < 0 or choice >= len(groups):
                raise ValueError("Invalid choice.")
            return groups[choice]
        except ValueError as e:
            print(f"[!] {e}")
            return None



    def scrape_group_members(self, target_group):
        """
        Scrape les membres d'un groupe target.
        """
        if not self.client.is_user_authorized():
            print("[!] Client not authorized. Connect first.")
            return []

        try:
            print(f"[+] Fetching members from group: {target_group.title}")
            participants = self.client.get_participants(target_group, aggressive=True)
            print(f"[+] {len(participants)} members fetched.")
            return participants
        
        except Exception as e:
            print(f"[!] Error while fetching members: {e}")
            return []



    def save_members_to_file(self, members, group_title):
        """
        Sauvegarde les membres d'un groupe dans un fichier CSV.
        """
        if not members:
            print("[!] No members to save.")
            return

        Tk().withdraw()
        save_path = asksaveasfilename(defaultextension=".csv",
                                      filetypes=[("CSV files", "*.csv")],
                                      title="Choose location to save members.csv")
        if not save_path:
            print("[!] Save operation cancelled.")
            return

        try:
            with open(save_path, "w", encoding="UTF-8") as file:
                writer = csv.writer(file, delimiter=",", lineterminator="\n")
                writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
                for user in members:
                    username = user.username or ""
                    first_name = user.first_name or ""
                    last_name = user.last_name or ""
                    name = (first_name + ' ' + last_name).strip()
                    writer.writerow([username, user.id, user.access_hash, name, group_title, target_group.id])
            print(f"[+] Members saved to {save_path}")
        except Exception as e:
            print(f"[!] Error while saving members: {e}")
