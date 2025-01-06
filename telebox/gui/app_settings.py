import requests
import customtkinter as ctk
from tkinter import messagebox
from features.checker import RateLimiter


class UserSettings(ctk.CTk):
    def __init__(self, user_email):
        super().__init__()
        self.title("Telebox - Settings")
        self.geometry("800x550")
        self.user_email = user_email
        
        # ====== Interface principale ======
        # Conteneurs pour layout
        self.left_frame = ctk.CTkFrame(self, width=200)
        self.left_frame.pack(side="left", fill="both", padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, width=600)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        

        # ====== Frame gauche (Commandes) ======
     
        self.logo_label = ctk.CTkLabel(self.left_frame, text="Settings", font=ctk.CTkFont("Helvetica Neue", size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.info_button = ctk.CTkButton(
            self.left_frame, 
            text="User Info", 
            command=self.show_user_info,
            width=220, height=35, corner_radius=10, 
            font=("Helvetica Neue", 16),
            fg_color="#3b82f6", 
            hover_color="#1e40af"
            )
        self.info_button.grid(row=1, column=0, padx=20, pady=10)

        # self.license_button = ctk.CTkButton(self.left_frame, text="Check your subscriptions", command=self.show_license_page)
        # self.license_button.grid(row=2, column=0, padx=20, pady=10)

        self.password_button = ctk.CTkButton(
            self.left_frame, 
            text="Change Password", 
            command=self.show_password_page,
            width=220, height=35, corner_radius=10, 
            font=("Helvetica Neue", 16),
            fg_color="#3b82f6", 
            hover_color="#1e40af"
            )
        self.password_button.grid(row=3, column=0, padx=20, pady=10)

        self.about_button = ctk.CTkButton(
            self.left_frame, 
            text="Contact Support", 
            command=self.open_website,
            width=220, height=35, corner_radius=10, 
            font=("Helvetica Neue", 16),
            fg_color="#3b82f6", 
            hover_color="#1e40af"
            )
        self.about_button.grid(row=4, column=0, padx=20, pady=10)


        self.show_user_info()


    def show_user_info(self):
        self.clear_main_frame()

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=0)
        self.right_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(self.right_frame, text="Your informations", font=ctk.CTkFont("Helvetica Neue", size=20, weight="bold")).grid(row=0, column=1, pady=20)

        try: 
            response = requests.post(
                "http://93.127.202.5:5002/auth/your_infos",
                json={
                    "user_email": self.user_email 
                    })
            if response.status_code == 200:
                user_data = response.json()
                email = user_data.get("email", "N/A")
                license_key = user_data.get("license_key", "N/A")
                transaction_amount = user_data.get("total_transaction_amount", "N/A")
                subscription_plan = user_data.get("subscription_plan", "N/A")

                self.create_copiable_entry("Your email:", email, 1)
                self.create_copiable_entry("License key:", license_key, 2)
                self.create_copiable_entry("Transaction amount:", f"{transaction_amount} €", 3)
                self.create_copiable_entry("Subscription plan:", subscription_plan, 4)
            else:
                ctk.CTkLabel(self.right_frame, text="Failed to display your information", font=("Helvetica Neue", 16),).grid(row=5, column=1, pady=10)

        except Exception as e:
            ctk.CTkLabel(self.right_frame, text="Error with server connection...", font=("Helvetica Neue", 16)).grid(row=5, column=1, pady=10)



    def create_copiable_entry(self, label_text, value, row):
        """Crée un label (titre) et un champ CTkEntry en readonly"""
        ctk.CTkLabel(self.right_frame, text=label_text, font=("Helvetica Neue", 16)).grid(row=row, column=0, pady=10, sticky="e")
        entry = ctk.CTkEntry(self.right_frame, width=250)
        entry.grid(row=row, column=1, pady=10, padx=10, sticky="w")
        
        entry.insert(0, value)
        entry.configure(state='readonly')  # Empêche la modification tout en permettant la copie



    def show_password_page(self):
        """Méthode pour changer son mot de passe"""
        self.clear_main_frame()

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=0)
        self.right_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            self.right_frame, 
            text="Change Your Password", 
            font=ctk.CTkFont("Helvetica Neue", size=20, weight="bold")
        ).grid(row=0, column=1, pady=20)

        # Champs pour valider l'ancien mot de passe
        ctk.CTkLabel(self.right_frame, text="Current Password:").grid(row=1, column=0, pady=10, sticky="e")
        self.current_password_entry = ctk.CTkEntry(self.right_frame)
        self.current_password_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # Champs pour entrer le nouveau mot de passe
        ctk.CTkLabel(self.right_frame, text="New Password:").grid(row=2, column=0, pady=10, sticky="e")
        self.new_password_entry = ctk.CTkEntry(self.right_frame, show="*")
        self.new_password_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        ctk.CTkLabel(self.right_frame, text="Confirm New Password:").grid(row=3, column=0, pady=10, sticky="e")
        self.confirm_password_entry = ctk.CTkEntry(self.right_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Bouton pour valider le changement
        ctk.CTkButton(
            self.right_frame, 
            text="Update Password", 
            command=self.change_password,
            width=220, height=35, corner_radius=10, 
            font=("Helvetica Neue", 16),
            fg_color="#3b82f6", 
            hover_color="#1e40af"
        ).grid(row=4, column=1, pady=20)



    def change_password(self):
        """Valider l'ancien mot de passe et changer le mot de passe"""
        email = self.user_email
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        # Étape 1 : Valider le mot de passe actuel
        response = requests.post(
            "http://93.127.202.5:5002/auth/validate_password",
            json={"user_email": email, "current_password": current_password}
        )
        if response.status_code != 200:
            messagebox.showerror("Error", "Invalid current password!")
            return

        # Étape 2 : Mettre à jour le mot de passe
        response = requests.post(
            "http://93.127.202.5:5002/auth/update_password",
            json={"user_email": email, "new_password": new_password}
        )
        if response.status_code == 200:
            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed to update password: {response.json().get('error', 'Unknown error')}")



    def clear_main_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()


    def open_website(self):
        import webbrowser
        webbrowser.open("https://telegram-toolbox.online/software/contact-support")
