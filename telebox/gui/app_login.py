from .app_dashboard import DashboardApp
from features.checker import DeviceChecker
import requests
import customtkinter as ctk


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")

        # Récupère l'identifiant unique de l'appareil
        self.device_checker = DeviceChecker()
        self.device_id = self.device_checker.get_device_fingerprint()
        self.last_login = self.device_checker.get_date()

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_label.pack(pady=10)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.response_label = ctk.CTkLabel(self, text="")
        self.response_label.pack()
        
        # only for dev (remove in production)
        self.godmode_button = ctk.CTkButton(self, text="Godmode", command=self.open_dashboard(user_email="dev"))
        self.godmode_button.pack(pady=5)

    # code coté client (de l'application)
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            self.response_label.configure(text="Please fill in all fields", fg_color="red")
            return
        try: # mettre cooldown
            response = requests.post(
                "http://93.127.202.5:5002/auth/app",
                json={
                        "email": email, 
                        "password": password,
                        "device_id": self.device_id,
                        "last_login": self.last_login
                      }
            )
            if response.status_code == 200:
                self.response_label.configure(text="Login successful!", fg_color="green")
                data = response.json()
                user_mail = data.get("email")
                self.open_dashboard(user_mail)

            elif response.status_code == 403:
                self.response_label.configure(text="Device not recognized. Contact support.", fg_color="red")

            else:
                self.response_label.configure(text="Invalid credentials", fg_color="red")
                
        except Exception as e:
            self.response_label.configure(text=f"Error: {e}", fg_color="red")



    def open_dashboard(self, user_email):
        """Ouvre le dashboard après authentification réussie."""
        self.destroy()
        dashboard = DashboardApp(user_email)
        dashboard.mainloop()