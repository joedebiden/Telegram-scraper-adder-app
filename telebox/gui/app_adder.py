import customtkinter as ctk
from tkinter import filedialog, messagebox
from features.adder import Adder  # Import de votre classe Adder


class AdderUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Telebox - Adder")
        self.geometry("800x600")


        # Initialisation de l'instance Adder
        self.adder = Adder(session_name='session_name', config_file='account.data')

        # Variables
        self.users = []
        self.selected_account = None
        self.selected_user = None
        self.target_group = None

        # ====== Interface principale ======
        # Liste des comptes disponibles
        self.accounts_label = ctk.CTkLabel(self, text="Select Telegram Account:", font=("Arial", 16))
        self.accounts_label.pack(pady=(20, 5))

        self.accounts_combobox = ctk.CTkComboBox(self, values=[], width=300)
        self.accounts_combobox.pack(pady=(0, 10))


        # Bouton pour se connecter
        self.connect_button = ctk.CTkButton(self, text="Connect", command=self.connect_account)
        self.connect_button.pack(pady=10)

        # Zone de texte pour afficher la progression
        self.log_textbox = ctk.CTkTextbox(self, width=600, height=200)
        self.log_textbox.pack(pady=20)

        # Chargement des utilisateurs (CSV)
        self.load_users_button = ctk.CTkButton(self, text="Load Users (CSV)", command=self.load_users, state="disabled")
        self.load_users_button.pack(pady=10)

        # Afficher les groupes/channels
        self.groups_label = ctk.CTkLabel(self, text="Select Group/Channel:", font=("Arial", 16))
        self.groups_label.pack(pady=(20, 5))

        self.groups_combobox = ctk.CTkComboBox(self, values=[], width=300, state="disabled")
        self.groups_combobox.pack(pady=(0, 10))

        self.load_groups_button = ctk.CTkButton(self, text="Load Groups", command=self.load_groups, state="disabled")
        self.load_groups_button.pack(pady=10)

        # Ajouter les membres
        self.speed_label = ctk.CTkLabel(self, text="Select Speed Mode (1-5):", font=("Arial", 16))
        self.speed_label.pack(pady=(20, 5))

        self.speed_combobox = ctk.CTkComboBox(self, values=["1", "2", "3", "4", "5"], width=100, state="disabled")
        self.speed_combobox.pack(pady=(0, 10))

        self.add_members_button = ctk.CTkButton(self, text="Add Members", command=self.add_members, state="disabled")
        self.add_members_button.pack(pady=20)

        # Fermeture de l'application
        self.exit_button = ctk.CTkButton(self, text="Close", command=self.quit)
        self.exit_button.pack(pady=10)



    def log_message(self, message):
        """Ajoute un message à la zone de log."""
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.yview("end")



    def select_account(self, account_name):
        """Met à jour le compte sélectionné."""
        self.selected_account = account_name

    def connect_account(self):
        """Se connecte au compte sélectionné."""
        if not self.selected_account:
            messagebox.showerror("Error", "Please select an account to connect.")
            return

        try:
            self.adder.section_name = self.selected_account
            self.log_message(f"[INFO] Connecting to account: {self.selected_account}...")
            if self.adder.connect() & self.adder.read_account_details() & self.adder.get_account_info():
                self.log_message("[SUCCESS] Connected successfully.")
                self.load_users_button.configure(state="normal")
                self.load_groups_button.configure(state="normal")
            else:
                self.log_message("[ERROR] Failed to connect.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")



    def load_users(self):
        """Charge les utilisateurs à partir d'un fichier CSV."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.users = self.adder.open_file(file_path)
            self.log_message(f"[INFO] Loaded {len(self.users)} users from {file_path}.")
        else:
            self.log_message("[ERROR] No file selected.")

    def load_groups(self):
        """Charge les groupes/channels disponibles."""
        self.log_message("[INFO] Loading groups/channels...")
        groups = self.adder.get_groups()

        if groups:
            group_names = [group.title for group in groups]
            self.groups_combobox.configure(values=group_names, state="normal")
            self.log_message("[SUCCESS] Groups loaded successfully.")
        else:
            self.log_message("[ERROR] No groups available.")

    def add_members(self):
        """Ajoute les membres au groupe sélectionné."""
        group_name = self.groups_combobox.get()
        if not group_name:
            messagebox.showerror("Error", "Please select a group.")
            return

        speed_mode = self.speed_combobox.get()
        if not speed_mode:
            messagebox.showerror("Error", "Please select a speed mode.")
            return

        # Trouver le groupe sélectionné
        groups = self.adder.get_groups()
        self.target_group = next((group for group in groups if group.title == group_name), None)

        if not self.target_group:
            self.log_message("[ERROR] Selected group not found.")
            return

        self.log_message(f"[INFO] Adding users to group: {group_name} with speed mode: {speed_mode}...")
        self.adder.set_speed_mode(int(speed_mode))
        self.adder.add_users(self.target_group, self.users, int(speed_mode))
        self.log_message("[SUCCESS] Members added successfully.")

        # Déconnexion après ajout
        self.adder.disconnect()
        self.log_message("[INFO] Disconnected.")
