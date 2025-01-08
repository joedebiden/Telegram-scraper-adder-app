from .app_dashboard import DashboardApp
from features.checker import DeviceChecker
import requests
import customtkinter as ctk


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telebox - Login")
        self.geometry("400x500")
        self.configure(bg="#1e1e2f")  # Fond sombre moderne

        # Récupère l'identifiant unique de l'appareil
        self.device_checker = DeviceChecker()
        self.device_id = self.device_checker.get_device_fingerprint()
        self.last_login = self.device_checker.get_date()

        # Titre
        self.title_label = ctk.CTkLabel(self, text="Welcome Back!", font=("Helvetica", 28, "bold"), text_color="#FFFFFF")
        self.title_label.pack(pady=(20, 10))

        # Champ Email
        self.email_label = ctk.CTkLabel(self, text="Email", font=("Helvetica", 16), text_color="#FFFFFF")
        self.email_label.pack(pady=(20, 5))
        self.email_entry = ctk.CTkEntry(self, width=280, height=35, corner_radius=10)
        self.email_entry.pack(pady=5)

        # Champ Mot de Passe
        self.password_label = ctk.CTkLabel(self, text="Password", font=("Helvetica", 16), text_color="#FFFFFF")
        self.password_label.pack(pady=(20, 5))
        self.password_entry = ctk.CTkEntry(self, show="*", width=280, height=35, corner_radius=10)
        self.password_entry.pack(pady=5)

        # Bouton de Connexion
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, width=280, height=40, corner_radius=10, fg_color="#3b82f6", hover_color="#1e40af")
        self.login_button.pack(pady=(20, 10))


        # Message de Réponse
        self.response_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14), text_color="#ff4b5c")
        self.response_label.pack()

        # Lien en cas de problème de connexion
        self.help_label = ctk.CTkLabel(self, text="Forgot Password?", font=("Helvetica", 14, "underline"), text_color="#3b82f6", cursor="hand2")
        self.help_label.pack(pady=(20, 10))
        self.help_label.bind("<Button-1>", lambda e: self.open_website())

        # Lien direction création de compte
        self.register_label = ctk.CTkLabel(self, text="Don't have an account?", font=("Helvetica", 14), text_color="#3b82f6", cursor="hand2")
        self.register_label.pack(pady=(20, 10))
        self.register_label.bind("<Button-1>", lambda e: self.register_link())

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            self.response_label.configure(text="Please fill in all fields")
            return
        try:
            response = requests.post(
                "https://telegram-toolbox.online/auth/app_login",
                json={
                    "email": email,
                    "password": password,
                    "device_id": self.device_id,
                    "last_login": self.last_login
                }
            )
            if response.status_code == 200:
                self.response_label.configure(text="Login successful!", text_color="#00ff00")
                data = response.json()
                user_mail = data.get("email")
                self.open_dashboard(user_mail)

            elif response.status_code == 403:
                self.response_label.configure(text="Device not recognized. Contact support.")

            else:
                self.response_label.configure(text="Invalid credentials")

        except Exception as e:
            self.response_label.configure(text=f"Error: {e}")

    def open_website(self):
        import webbrowser
        webbrowser.open("https://telegram-toolbox.online/auth/reset_request")

    def register_link(self):
        import webbrowser
        webbrowser.open("https://telegram-toolbox.online/auth/register")

    def open_dashboard(self, user_email):
        """Ouvre le dashboard après authentification réussie."""
        self.destroy()
        dashboard = DashboardApp(user_email)
        dashboard.mainloop()
