from .app_dashboard import DashboardApp
import requests
import customtkinter as ctk

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")

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


    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            self.response_label.configure(text="Please fill in all fields", fg_color="red")
            return
        try:
            response = requests.post(
                "http://93.127.202.5:5002/auth/app",
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                self.response_label.configure(text="Login successful!", fg_color="green")
                data = response.json()
                user_mail = data.get("email")
                self.open_dashboard(user_mail)

                # Proceed to the main application
            else:
                self.response_label.configure(text="Invalid credentials", fg_color="red")
                
        except Exception as e:
            self.response_label.configure(text=f"Error: {e}", fg_color="red")



    def open_dashboard(self, user_email):
        """Ouvre le dashboard après authentification réussie."""
        self.destroy()  # Ferme la fenêtre de login
        dashboard = DashboardApp(user_email)
        dashboard.mainloop()