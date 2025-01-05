import customtkinter as ctk
from tkinter import filedialog, messagebox
from features.adder import Adder  
import subprocess

class AdderUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Telebox - Adder")
        self.geometry("1200x600")


        # Initialisation de l'instance Adder
        self.adder = Adder(session_name='session_name', config_file='account.data')

        # Variables
        self.users = []
        self.selected_account = None
        self.selected_user = None
        self.target_group = None

        # ====== Interface principale ======
        # Conteneurs pour layout
        self.left_frame = ctk.CTkFrame(self, width=400)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, width=400)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ====== Frame gauche (Commandes) ======
        # Liste des comptes disponibles
        self.accounts_label = ctk.CTkLabel(self.left_frame, text="Select Telegram Account:", font=("Arial", 16))
        self.accounts_label.pack(pady=(20, 5))
        self.accounts_combobox = ctk.CTkComboBox(self.left_frame, values=self.get_available_accounts(), width=300, command=self.on_account_select)
        self.accounts_combobox.pack(pady=(0, 10))

        # Bouton pour se connecter
        self.connect_button = ctk.CTkButton(self.left_frame, text="Connect", command=self.connect_account)
        self.connect_button.pack(pady=10)

        # Chargement des utilisateurs (CSV)
        self.load_users_button = ctk.CTkButton(self.left_frame, text="Load Users (CSV)", command=self.load_users,
                                               state="disabled")
        self.load_users_button.pack(pady=10)

        # Afficher les groupes/channels
        self.load_groups_button = ctk.CTkButton(self.left_frame, text="Load Groups", command=self.load_groups,state="disabled")
        self.load_groups_button.pack(pady=10)

        self.groups_label = ctk.CTkLabel(self.left_frame, text="Select Group/Channel:", font=("Arial", 16))
        self.groups_label.pack(pady=(20, 5))

        self.groups_combobox = ctk.CTkComboBox(self.left_frame, values=[], width=300, state="disabled")
        self.groups_combobox.pack(pady=(0, 10))


        # Ajouter les membres
        self.speed_label = ctk.CTkLabel(self.left_frame, text="Select Speed Mode (1-4):", font=("Arial", 16))
        self.speed_label.pack(pady=(20, 5))
        self.speed_combobox = ctk.CTkComboBox(self.left_frame, values=["Very slow", "Normal", "Fast", "Very fast"], width=100, state="disabled")
        self.speed_combobox.pack(pady=(0, 10))

        self.add_members_button = ctk.CTkButton(self.left_frame, text="Add Members", command=self.add_members, state="disabled")
        self.add_members_button.pack(pady=20)


        # ====== Frame droite (Terminal/Log) ======
        self.log_textbox = ctk.CTkTextbox(self.right_frame, width=400, height=500)
        self.log_textbox.pack(pady=10, padx=10)


        # bouton ouvrir terminal
        self.terminal_button = ctk.CTkButton(self.right_frame, text="Open Terminal", command=self.open_terminal)
        self.terminal_button.pack(pady=20, padx=20)


    def log_message(self, message):
        """Ajoute un message à la zone de log."""
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.yview("end")



    def get_available_accounts(self):
        """Récupère les comptes disponibles depuis la méthode Adder."""
        try:
            accounts = self.adder.list_accounts()
            if accounts:
                return accounts
            else:
                self.log_message("[ERROR] No accounts available.")
                return []
        except Exception as e:
            self.log_message(f"[ERROR] Failed to fetch accounts: {e}")
            return []
        
    

    def on_account_select(self, account_name):
        """Déclenché lorsque l'utilisateur sélectionne un compte."""
        self.selected_account = account_name


    def connect_account(self):
        """Se connecte au compte sélectionné."""
        if not self.selected_account:
            messagebox.showerror("Error", "Please select an account to connect.")
            return

        try:
            self.adder.section_name = self.selected_account
            self.log_message(f"[INFO] Connecting to account: {self.selected_account}...")
            self.adder.read_account_details()
            self.adder.connect()
            self.adder.get_account_info()
            self.log_message("[SUCCESS] Connected successfully.")
            self.load_users_button.configure(state="normal")
            self.load_groups_button.configure(state="normal")

        except Exception as e:
            self.log_message("[ERROR] Connection failed...")
            messagebox.showerror("Error", f"Failed to connect: {e}")



    def load_users(self):
        """Charge les utilisateurs à partir d'un fichier CSV."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.users = self.adder.open_file(file_path)
            self.log_message(f"[INFO] Loaded {len(self.users)} users from {file_path}.")
            self.speed_combobox.configure(state="normal")
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
            self.add_members_button.configure(state="normal")
        else:
            self.log_message("[ERROR] No groups available.")



    def add_members(self):
        """Ajoute les membres au groupe sélectionné.""" 
        try:
            group_name = self.groups_combobox.get()
            if not group_name:
                messagebox.showerror("Error", "Please select a group.")
                return

            speed_mode = self.speed_combobox.get()
            if not speed_mode:
                messagebox.showerror("Error", "Please select a speed mode.")
                return

            groups = self.adder.get_groups()
            self.target_group = next((group for group in groups if group.title == group_name), None)

            if not self.target_group:
                self.log_message("[ERROR] Selected group not found.")
                return

            speed_delay = self.adder.set_speed_mode(speed_mode)
            if not speed_delay:
                self.log_message("[ERROR] Invalid speed mode.")
                return

            self.log_message(f"[INFO] Adding users to group: {group_name} with speed mode: {speed_mode} (delay: {speed_delay})...")
            self.adder.add_users(self.target_group, self.users, speed_delay)
            self.log_message("[SUCCESS] Members added successfully.")

        except Exception as e:
            self.log_message(f"[ERROR] {e}")
        finally:
            self.adder.disconnect()
            self.log_message("[INFO] Disconnected.")


    def open_terminal(self):
        try: 
            subprocess.run("start cmd", shell=True)
            self.log_message("[INFO] Terminal launched successfully.")
        except Exception as e:
            self.log_message(f"[ERROR] Failed to open terminal: {e}")