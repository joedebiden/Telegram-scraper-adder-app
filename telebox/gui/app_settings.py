import requests
import customtkinter as ctk
from tkinter import messagebox

class UserSettings(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("800x550")

        


        # Frame pour les paramètres utilisateur
        self.settings_frame = ctk.CTkFrame(self, corner_radius=10)
        self.settings_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Nom d'utilisateur
        self.username_label = ctk.CTkLabel(self.settings_frame, text="Username:")
        self.username_label.pack(anchor="w", padx=10, pady=5)
        self.username_entry = ctk.CTkEntry(self.settings_frame, placeholder_text="Enter your username")
        self.username_entry.pack(fill="x", padx=10, pady=5)

        # Email
        self.email_label = ctk.CTkLabel(self.settings_frame, text="Email:")
        self.email_label.pack(anchor="w", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(self.settings_frame, placeholder_text="Enter your email")
        self.email_entry.pack(fill="x", padx=10, pady=5)

        # Mot de passe
        self.password_label = ctk.CTkLabel(self.settings_frame, text="Password:")
        self.password_label.pack(anchor="w", padx=10, pady=5)
        self.password_entry = ctk.CTkEntry(self.settings_frame, show="*", placeholder_text="Enter your password")
        self.password_entry.pack(fill="x", padx=10, pady=5)

        # Bouton pour sauvegarder les paramètres
        self.save_button = ctk.CTkButton(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_button.pack(pady=20)

    def save_settings(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Simuler la sauvegarde des paramètres
        try:
            # Ajoutez ici la logique pour sauvegarder les paramètres utilisateur
            # Par exemple, envoyer une requête POST à un serveur
            # response = requests.post("https://example.com/api/save_settings", json={"username": username, "email": email, "password": password})
            # if response.status_code == 200:
            #     messagebox.showinfo("Success", "Settings saved successfully")
            # else:
            #     messagebox.showerror("Error", "Failed to save settings")

            # Pour l'instant, afficher un message de succès simulé
            messagebox.showinfo("Success", "Settings saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

