import customtkinter as ctk
from gui.app_account import AccountManagerUI
from gui.app_scraper import ScraperUI
from gui.app_adder import AdderUI


class DashboardApp(ctk.CTk):
    
    def __init__(self, ):
        super().__init__()

        self.account_manager_window = None
        self.scraper_window = None
        self.adder_window = None



        # ======= Apparence globale ======

        self.title("Telebox Dashboard")
        self.geometry("1000x700")
        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("dark-blue") 

        # ======= Menu latéral =======
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=20)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Titre Telebox
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Telebox", 
            font=("Helvetica", 30, "bold"), 
            text_color="#FFFFFF")
        self.logo_label.pack(pady=(40, 20))


        # ====== Boutons du menu (les apps) ======
        button_font = ("Helvetica Neue", 18)


        # Account Manager
        self.account_manager_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Telegram accounts",
            font=button_font,
            command=self.open_account_manager,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6", 
            hover_color="#1e40af"
            )
        self.account_manager_button.pack(pady=10)


        # Proxies Manager - TO DO -
        self.proxy_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Proxies Manager", 
            font=button_font, 
            command=self.open_proxy_manager,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6", 
            hover_color="#1e40af",
            state="enabled")
        self.proxy_button.pack(pady=10)


        # Scraper
        self.scraper_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Scraper", 
            font=button_font, 
            command=self.open_scraper,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6", 
            hover_color="#1e40af")
        self.scraper_button.pack(pady=10)


        # Adder
        self.adder_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Adder", 
            font=button_font, 
            command=self.open_adder,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6", 
            hover_color="#1e40af",
            state="enabled")
        self.adder_button.pack(pady=10)


        # Message Sender - TO DO -
        self.message_sender_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Message Sender", 
            font=button_font, 
            command=self.open_message_sender,
            width=320, height=45, corner_radius=12, 
            fg_color="#3b82f6", 
            hover_color="#1e40af",
            state="enabled")
        self.message_sender_button.pack(pady=10)


        # Sélection des thèmes
        self.mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            font=button_font)
        self.mode_label.pack(pady=(30, 5))

        self.mode_switch = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light"], 
            command=self.change_mode,
            width=320, height=30, corner_radius=12, 
            fg_color="#3b82f6", 
            )
        
        self.mode_switch.set("Select a theme")
        self.mode_switch.pack(pady=(0, 20))


        # Zone principale
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.main_label = ctk.CTkLabel(
            self.main_frame, 
            text="Welcome on Telebox app !", 
            font=("Helvetica Neue", 30, "bold"),
            corner_radius=15,
            text_color="#ffffff")
        self.main_label.pack(pady=20)


    # ======= Méthodes pour ouvrir les fenêtres =======
    def open_account_manager(self):
        """
        Fonction pour ouvrir la fenêtre de gestion des comptes.
        """
        if self.account_manager_window is None or not self.account_manager_window.winfo_exists():
            self.withdraw()
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
            self.withdraw()
            self.scraper_window = ScraperUI()  
            self.scraper_window.protocol("WM_DELETE_WINDOW", self.on_scraper_close)
            self.scraper_window.mainloop()
        



    def open_adder(self):
        """
        Ouvre une seule et unique fenêtre pour adder.
        """
        if self.adder_window is None or not self.adder_button.winfo_exists():
            self.withdraw()
            self.adder_window = AdderUI()
            self.adder_window.protocol("WM_DELETE_WINDOW", self.on_adder_close)
            self.adder_window.mainloop()
        else:
            self.scraper_window.lift()




    def open_message_sender(self):
        self.update_main_frame("Message Sender Interface Coming Soon!")

    def open_proxy_manager(self):
        self.update_main_frame("Proxies Manager Coming Soon!")



    """ Méthode pour changer le mode d'apparence """
    def change_mode(self, mode):
        ctk.set_appearance_mode(mode)

    



    """ Méthodes pour la mise à jour de la main zone """
    def update_main_frame(self, message):
        """Met à jour la zone principale avec un message."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        new_label = ctk.CTkLabel(self.main_frame, text=message, font=("Helvetica Neue", 18), wraplength=500)
        new_label.pack(pady=20)


    def on_account_manager_close(self):
        self.account_manager_window.destroy()
        self.account_manager_window = None
        self.deiconify()

    def on_scraper_close(self):
        self.scraper_window.destroy()
        self.scraper_window = None
        self.deiconify()

    def on_adder_close(self):
        self.adder_window.destroy()
        self.adder_window = None
        self.deiconify()



    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)