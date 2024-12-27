import customtkinter as ctk
from tkinter import messagebox
from features.scraper import Scraper

class ScraperUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telebox - Scraper")
        self.geometry("800x550")

        # Initialisation de la classe Scraper
        self.scraper = Scraper(config_file="account.data")

        # Variables pour stocker les choix utilisateur
        self.selected_account = None
        self.selected_group = None

        # Interface utilisateur
        self.create_account_ui()
        self.create_group_ui()
        self.display_accounts()



    def create_account_ui(self):
        """Création de l'UI pour gérer les comptes Telegram."""
        frame = ctk.CTkFrame(self, width=180, corner_radius=20)
        frame.pack(side="left", fill="y", padx=10, pady=10)

        label = ctk.CTkLabel(frame, text="Available Accounts:", font=("Helvetica", 18))
        label.pack(anchor="w", padx=5, pady=5)

        self.account_listbox = ctk.CTkComboBox(frame, values=[], command=self.select_account)
        self.account_listbox.pack(fill="x", padx=5, pady=5)

        connect_button = ctk.CTkButton(frame, text="Connect to Account", command=self.connect_account)
        connect_button.pack(fill="x", padx=5, pady=5)



    def create_group_ui(self):
        """Création de l'UI pour afficher et sélectionner les groupes."""
        frame = ctk.CTkFrame(self, width=400, height=130, corner_radius=17)
        frame.pack(pady=10)
        frame.pack_propagate(False)

        label = ctk.CTkLabel(frame, text="Available Groups:", font=("Arial", 16))
        label.pack(anchor="center", pady=10)

        self.group_listbox = ctk.CTkComboBox(
            frame, 
            values=[], 
            command=self.select_group,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6"
            )
        self.group_listbox.pack(fill="x", padx=5, pady=5)

        scrape_button = ctk.CTkButton(
            frame, 
            text="Scrape Group", 
            command=self.scrape_group,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6"
            )
        scrape_button.pack(fill="x", padx=5, pady=5)

    def display_accounts(self):
        """Charge et affiche les comptes disponibles."""
        try:
            available_accounts = self.scraper.list_accounts()
            if available_accounts:
                self.account_listbox.configure(values=available_accounts)
            else:
                messagebox.showerror("Error", "No accounts found in 'account.data'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")

    def select_account(self, account_name):
        """Met à jour le compte sélectionné."""
        self.selected_account = account_name

    def connect_account(self):
        """Se connecte au compte sélectionné."""
        if not self.selected_account:
            messagebox.showerror("Error", "Please select an account to connect.")
            return

        try:
            self.scraper.section_name = self.selected_account
            self.scraper.read_account_details()
            self.scraper.connect()
            self.scraper.get_account_info()

            messagebox.showinfo("Success", f"Connected to {self.selected_account}")
            self.display_groups()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def display_groups(self):
        """Charge et affiche les groupes disponibles du compte connecté."""
        try:
            groups = self.scraper.get_groups()
            if groups:
                self.group_listbox.configure(values=[group.title for group in groups])
            else:
                messagebox.showinfo("Info", "No groups found for this account.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load groups: {e}")



    def select_group(self, group_name):
        """Met à jour le groupe sélectionné."""
        groups = self.scraper.get_groups()
        self.selected_group = next((group for group in groups if group.title == group_name), None)



    def scrape_group(self):
        """Lance le scraping du groupe sélectionné."""
        if not self.selected_group:
            messagebox.showerror("Error", "Please select a group to scrape.")
            return

        try:
            members = self.scraper.scrape_group_members(self.selected_group)
            if members:
                messagebox.showinfo("Success", f"Scraping completed. {len(members)} members found.")
                self.scraper.save_members_to_file(members, self.selected_group.title)
            else:
                messagebox.showinfo("Info", "No members found in the selected group.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape group: {e}")
