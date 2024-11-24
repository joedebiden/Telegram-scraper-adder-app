import customtkinter

class DashboardApp(customtkinter.CTk):
    def __init__(self, user_name):
        super().__init__()

        self.title("Telebox Dashboard")
        self.geometry("800x600")
        self.resizable(False, False)

        # Couleurs personnalisées
        customtkinter.set_appearance_mode("Dark")  # Mode sombre
        customtkinter.set_default_color_theme("dark-blue")  # Thème bleu sombre

        # --- FRAME LATÉRAL (BARRE LATÉRALE) ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(0, weight=1)

        # Titre
        self.sidebar_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Outils", font=("Arial", 18, "bold")
        )
        self.sidebar_label.grid(row=0, column=0, pady=20)

        # Boutons de navigation
        self.telegram_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Gestion de comptes Telegram", command=self.show_telegram
        )
        self.telegram_button.grid(row=1, column=0, pady=10, padx=20)

        self.proxy_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Gestion de proxy", command=self.show_proxy
        )
        self.proxy_button.grid(row=2, column=0, pady=10, padx=20)

        self.scraper_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Scraper", command=self.show_scraper
        )
        self.scraper_button.grid(row=3, column=0, pady=10, padx=20)

        self.adder_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Adder", command=self.show_adder
        )
        self.adder_button.grid(row=4, column=0, pady=10, padx=20)

        # Bouton déconnexion
        self.logout_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Déconnexion", fg_color="red", command=self.logout
        )
        self.logout_button.grid(row=5, column=0, pady=(40, 10), padx=20)

        # --- ZONE PRINCIPALE (CONTENU) ---
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Message de bienvenue
        self.welcome_label = customtkinter.CTkLabel(
            self.main_frame,
            text=f"Bienvenue, {user_name} !",
            font=("Arial", 24, "bold"),
            anchor="center",
        )
        self.welcome_label.grid(row=0, column=0, pady=20, padx=20)

        # Sous-titre
        self.instruction_label = customtkinter.CTkLabel(
            self.main_frame,
            text="Sélectionnez un outil dans la barre latérale pour commencer.",
            font=("Arial", 16),
        )
        self.instruction_label.grid(row=1, column=0, pady=10)

    # --- MÉTHODES POUR LES BOUTONS ---
    def show_telegram(self):
        self.display_message("Gestion de comptes Telegram")

    def show_proxy(self):
        self.display_message("Gestion de proxy")

    def show_scraper(self):
        self.display_message("Scraper")

    def show_adder(self):
        self.display_message("Adder")

    def display_message(self, message):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        label = customtkinter.CTkLabel(
            self.main_frame, text=message, font=("Arial", 18, "bold")
        )
        label.grid(row=0, column=0, pady=20)

    def logout(self):
        self.destroy()  # Ferme l'application ou retourne au login
