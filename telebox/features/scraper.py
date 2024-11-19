from __init__ import csv, Tk, asksaveasfilename
from telegram_base import TelegramBase

class Scraper(TelegramBase):
    def __init__(self, session_name, api_id, api_hash, phone, proxy=None):
        super().__init__(session_name, api_id, api_hash, phone, proxy)



    def scrape_group_members(self, group):
        """
        Scrape les membres d'un groupe donné.
        """
        try:
            print(f"[+] Fetching members from group: {group.title}")
            participants = self.client.get_participants(group, aggressive=True)
            print(f"[+] {len(participants)} members fetched.")
            return participants
        except Exception as e:
            print(f"[!] Error while fetching members: {e}")
            return []



    def save_members_to_file(self, members, group_title):
        """
        Sauvegarde les membres d'un groupe dans un fichier CSV.
        """
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
                    writer.writerow([username, user.id, user.access_hash, name, group_title, group.id])
            print(f"[+] Members saved to {save_path}")
        except Exception as e:
            print(f"[!] Error while saving members: {e}")



    def perform_task(self):
        """Implémente la logique de scraping pour la méthode abstraite."""
        self.connect()
        groups = self.get_groups()
        if not groups:
            print("[!] No groups found.")
            self.disconnect()
            return

        print("[+] Choose a group to scrape members:\n")
        for i, group in enumerate(groups):
            print(f"{i} -> {group.title}")
        try:
            choice = int(input("\n[+] Enter a number: "))
            target_group = groups[choice]
        except (ValueError, IndexError):
            print("[!] Invalid selection.")
            self.disconnect()
            return

        members = self.scrape_group_members(target_group)
        if members:
            self.save_members_to_file(members, target_group.title)
        self.disconnect()
