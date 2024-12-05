import customtkinter as ctk
from gui.app_account import AccountManagerUI
from gui.app_scraper import ScraperUI

class DashboardApp(ctk.CTk):
    
    def __init__(self, user_email):
        super().__init__()

        self.user_email = user_email
        self.account_manager_window = None
        self.scraper_window = None

        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("blue") 


        # ======= Zone principale =======
        self.title("Telebox Dashboard")
        self.geometry("900x600")

        # ======= Menu latéral =======
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Titre Telebox
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Telebox", font=("Arial", 24, "bold"))
        self.logo_label.pack(pady=(20, 20))


        # ====== Boutons de fonctionnalités ======

        # Account Manager
        self.account_manager_button = ctk.CTkButton(self.sidebar_frame, text="Telegram accounts", command=self.open_account_manager)
        self.account_manager_button.pack(pady=10)

        # Proxies Manager
        self.proxy_button = ctk.CTkButton(self.sidebar_frame, text="Proxies Manager", command=self.open_proxy_manager)
        self.proxy_button.pack(pady=10)

        # Scraper
        self.scraper_button = ctk.CTkButton(self.sidebar_frame, text="Scraper", command=self.open_scraper)
        self.scraper_button.pack(pady=10)

        # Adder
        self.adder_button = ctk.CTkButton(self.sidebar_frame, text="Adder", command=self.open_adder)
        self.adder_button.pack(pady=10)

        # Message Sender
        self.message_sender_button = ctk.CTkButton(self.sidebar_frame, text="Message Sender", command=self.open_message_sender)
        self.message_sender_button.pack(pady=10)


        # ===== Theme Switcher =====
        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:")
        self.mode_label.pack(pady=(30, 5))
        self.mode_switch = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light"], command=self.change_mode)
        self.mode_switch.set("Dark")
        self.mode_switch.pack(pady=(0, 20))


        # ======= Zone principale =======
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.main_label = ctk.CTkLabel(self.main_frame, text="Welcome on Telebox app !", font=("Arial", 18))
        self.main_label.pack(pady=20)


    # ======= Méthodes pour changer les pages =======
    def open_account_manager(self):
        """
        Fonction pour ouvrir la fenêtre de gestion des comptes.
        """
        if self.account_manager_window is None or not self.account_manager_window.winfo_exists():
            self.account_manager_window = AccountManagerUI()  
            self.account_manager_window.protocol("WM_DELETE_WINDOW", self.on_account_manager_close)
            self.account_manager_window.mainloop()
        else:
            self.account_manager_window.lift()



    def open_scraper(self):
        """
        Ouvre une seule unique fenêtre pour scraper.
        """
        if self.scraper_window is None or not self.scraper_window.winfo_exists():
            self.scraper_window = ScraperUI()  
            self.scraper_window.protocol("WM_DELETE_WINDOW", self.on_scraper_close)
            self.scraper_window.mainloop()
        else:
            self.scraper_window.lift()



    def open_adder(self):
        self.update_main_frame("Adder Interface Coming Soon!")

    def open_message_sender(self):
        self.update_main_frame("Message Sender Interface Coming Soon!")

    def open_proxy_manager(self):
        self.update_main_frame("Proxies Manager Coming Soon!")

    def on_account_manager_close(self):
        self.account_manager_window.destroy()
        self.account_manager_window = None
    def on_scraper_close(self):
        self.scraper_window.destroy()
        self.scraper_window = None

    def update_main_frame(self, message):
        """Met à jour la zone principale avec un message."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        new_label = ctk.CTkLabel(self.main_frame, text=message, font=("Arial", 18), wraplength=500)
        new_label.pack(pady=20)

    # ======= Méthode pour changer le mode d'apparence =======
    def change_mode(self, mode):
        ctk.set_appearance_mode(mode)