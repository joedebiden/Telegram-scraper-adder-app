import threading
import time
import asyncio
import customtkinter as ctk
from tkinter import filedialog, messagebox
from features.adder import Adder

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
        self.accounts_label = ctk.CTkLabel(self.left_frame, text="Select Telegram Account:", font=("Arial", 16))
        self.accounts_label.pack(pady=(20, 5))

        # Appel après l'initialisation de log_textbox
        self.accounts_combobox = ctk.CTkComboBox(self.left_frame, values=self.get_available_accounts(), width=300, command=self.on_account_select)
        self.accounts_combobox.pack(pady=(0, 10))

        self.connect_button = ctk.CTkButton(self.left_frame, text="Connect", command=self.connect_account)
        self.connect_button.pack(pady=10)

        self.load_users_button = ctk.CTkButton(self.left_frame, text="Load Users (CSV)", command=self.load_users_sync, state="disabled")
        self.load_users_button.pack(pady=10)


        self.groups_label = ctk.CTkLabel(self.left_frame, text="Select where you want to add members:", font=("Arial", 16))
        self.groups_label.pack(pady=(20, 5))

        self.groups_combobox = ctk.CTkComboBox(
            self.left_frame, 
            values=[], 
            width=300, height=35, corner_radius=12,
            command=self.select_group,
            )
        self.groups_combobox.set("Select a group/channel")
        self.groups_combobox.pack(pady=(5, 5))
        

        self.speed_label = ctk.CTkLabel(self.left_frame, text="Select Speed Mode (1-4):", font=("Arial", 16))
        self.speed_label.pack(pady=(20, 5))
        self.speed_combobox = ctk.CTkComboBox(self.left_frame, values=["Very slow", "Normal", "Fast", "Very fast"], width=100, state="disabled")
        self.speed_combobox.pack(pady=(0, 10))

        self.add_members_button = ctk.CTkButton(self.left_frame, text="Add Members", command=self.start_adding_thread, state="disabled")
        self.add_members_button.pack(pady=20)

        # ====== Frame droite (Terminal/Log) ======
        self.log_textbox = ctk.CTkTextbox(self.right_frame, width=400, height=400)
        self.log_textbox.pack(pady=10, padx=10)

        self.progress_bar = ctk.CTkProgressBar(self.right_frame, width=400)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

    def log_message(self, message):
        if hasattr(self, 'log_textbox'):
            self.log_textbox.insert("end", message + "\n")
            self.log_textbox.yview("end")
        else:
            print(message)

    # fonctionne bien
    def get_available_accounts(self):
        # print(self.adder.list_accounts())
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
        self.selected_account = account_name

    # fonctionne bien
    def connect_account(self):
        if not self.selected_account:
            messagebox.showerror("Error", "Please select an account to connect.")
            return
        try:
            self.adder.section_name = self.selected_account
            self.log_message(f"[INFO] Connecting to account: {self.selected_account}...")
            self.adder.read_account_details()
            self.adder.connect()
            # self.adder.get_account_info()
            self.log_message("[SUCCESS] Connected successfully.")
            self.load_users_button.configure(state="normal")
            self.display_groups()
        except Exception as e:
            self.log_message("[ERROR ] Connection failed...")
            messagebox.showerror("Error", f"Failed to connect: {e}")

    # fonctionne bien 
    async def load_users(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.users = await self.adder.open_file(file_path)
            if self.users is not None: 
                self.log_message(f"[INFO] Loaded {len(self.users)} users from {file_path}.")
                self.groups_combobox.configure(state="normal")
                self.speed_combobox.configure(state="normal")
            else:
                self.log_message("[ERROR] Failed to load users. The file might be empty or invalid.")
        else:
            self.log_message("[ERROR] No file selected.")

    def load_users_sync(self):
        asyncio.run(self.load_users())


    # ne fonctionne pas avec le bouton pour afficher les groupes
    def display_groups(self):
        """Charge et affiche les groupes disponibles du compte connecté."""
        try:
            groups = self.adder.get_groups()
            if groups:
                self.log_message(f"[INFO] Found {len(groups)} groups.")
                self.groups_combobox.configure(values=[group.title for group in groups])
            else:
                self.log_message("[INFO] No groups found for this account.")
        except Exception as e:
            self.log_message(f"[ERROR] Failed to load groups: {e}")

    def select_group(self, group_name):
        """Met à jour le groupe sélectionné."""
        groups = asyncio.run(self.adder.get_groups())
        self.selected_group = next((group for group in groups if group.title == group_name), None)



    def start_adding_thread(self):
        self.add_members_button.configure(state="disabled")
        add_thread = threading.Thread(target=self.add_members)
        add_thread.start()

    def add_members(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._add_members())
        except Exception as e:
            self.log_message(f"[ERROR] Failed to add members: {e}")

        finally:
            self.adder.disconnect()
            self.add_members_button.configure(state="normal")
            self.log_message("[INFO] Disconnected from Telegram.")
    

    async def _add_members(self):
        try:
            group_name = self.groups_combobox.get()
            if not group_name:
                messagebox.showerror("Error", "Please select a group.")
                return
            speed_mode = self.speed_combobox.get()
            if not speed_mode:
                messagebox.showerror("Error", "Please select a speed mode.")
                return
            
            # Appel correct de la coroutine avec await
            groups = await self.adder.get_groups()  

            self.target_group = next((group for group in groups if group.title == group_name), None)
            if not self.target_group:
                self.log_message("[ERROR] Selected group not found.")
                return
            
            speed_delay = self.adder.set_speed_mode(speed_mode)
            self.log_message(f"[INFO] Adding users to group: {group_name} with speed mode: {speed_mode}...")
            
            total_users = len(self.users)
            for i, user in enumerate(self.users):
                await self.adder.add_users(self.target_group, [user], speed_delay)
                self.progress_bar.set((i + 1) / total_users)
                self.update_idletasks()
                self.log_message(f"[INFO] {user} added.")
                
            self.log_message("[SUCCESS] Members added successfully.")
        except Exception as e:
            self.log_message(f"[ERROR] {e}")
