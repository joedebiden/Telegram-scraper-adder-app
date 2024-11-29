import customtkinter as ctk
from gui.app_account import AccountManagerUI

class DashboardApp(ctk.CTk):
    def __init__(self, user_email):
        super().__init__()

        self.title("Telebox Dashboard")
        self.geometry("900x600")
        self.user_email = user_email

        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("blue") 


        # ======= Menu latéral =======
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Titre Telebox
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Telebox", font=("Arial", 24, "bold"))
        self.logo_label.pack(pady=(20, 20))


        # ====== Boutons de fonctionnalités ======

        # Scraper
        self.scraper_button = ctk.CTkButton(self.sidebar_frame, text="Scraper", command=self.open_scraper)
        self.scraper_button.pack(pady=10)

        # Adder
        self.adder_button = ctk.CTkButton(self.sidebar_frame, text="Adder", command=self.open_adder)
        self.adder_button.pack(pady=10)

        # Message Sender
        self.message_sender_button = ctk.CTkButton(self.sidebar_frame, text="Message Sender", command=self.open_message_sender)
        self.message_sender_button.pack(pady=10)

        # Account Manager
        self.account_manager_button = ctk.CTkButton(
            self, 
            text="Gérer les Comptes", 
            command=self.open_account_manager
        )
        self.account_manager_button.pack(pady=20)

        # Proxies Manager
        self.proxy_button = ctk.CTkButton(self.sidebar_frame, text="Proxies Manager", command=self.open_proxy_manager)
        self.proxy_button.pack(pady=10)


        # ===== Theme Switcher =====
        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:")
        self.mode_label.pack(pady=(30, 5))
        self.mode_switch = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light"], command=self.change_mode)
        self.mode_switch.set("Dark")
        self.mode_switch.pack(pady=(0, 20))


        # ======= Zone principale =======
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.main_label = ctk.CTkLabel(self.main_frame, text="Bienvenue sur Telebox !", font=("Arial", 18))
        self.main_label.pack(pady=20)


    # ======= Méthodes pour changer les pages =======
    def open_scraper(self):
        self.update_main_frame("Scraper Interface Coming Soon!")

    def open_adder(self):
        self.update_main_frame("Adder Interface Coming Soon!")

    def open_message_sender(self):
        self.update_main_frame("Message Sender Interface Coming Soon!")

    def open_account_manager(self):
        """
        Ouvre une nouvelle fenêtre pour gérer les comptes.
        """
        account_manager_ui = AccountManagerUI()  # Instancie la classe UI du gestionnaire de comptes
        account_manager_ui.mainloop()

    def open_proxy_manager(self):
        self.update_main_frame("Proxies Manager Coming Soon!")

    def update_main_frame(self, message):
        """Met à jour la zone principale avec un message."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        new_label = ctk.CTkLabel(self.main_frame, text=message, font=("Arial", 18), wraplength=500)
        new_label.pack(pady=20)

    # ======= Méthode pour changer le mode d'apparence =======
    def change_mode(self, mode):
        ctk.set_appearance_mode(mode)