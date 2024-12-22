import requests
import customtkinter as ctk
from tkinter import messagebox



class UserSettings(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("800x550")

        
        # ====== Interface principale ======
        # Conteneurs pour layout
        self.left_frame = ctk.CTkFrame(self, width=100)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, width=300)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ====== Frame gauche (Commandes) ======
        # Liste des comptes disponibles
        

        self.logo_label = ctk.CTkLabel(self.left_frame, text="Settings", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.info_button = ctk.CTkButton(self.left_frame, text="User Info", command=self.show_user_info)
        self.info_button.grid(row=1, column=0, padx=20, pady=10)

        # self.license_button = ctk.CTkButton(self.left_frame, text="Check your subscriptions", command=self.show_license_page)
        # self.license_button.grid(row=2, column=0, padx=20, pady=10)

        self.password_button = ctk.CTkButton(self.left_frame, text="Change Password", command=self.show_password_page)
        self.password_button.grid(row=3, column=0, padx=20, pady=10)

        self.about_button = ctk.CTkButton(self.left_frame, text="Contact Support", command=self.open_website)
        self.about_button.grid(row=4, column=0, padx=20, pady=10)



        # Charge les infos utilisateur dès le lancement
        self.show_user_info()

    def show_user_info(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.right_frame, text="Your informations", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=20)

        # Requête POST pour récupérer la licence
        try: # mettre cooldown
            response = requests.post(
                "http://93.127.202.5:5002/auth/your_infos",
                json={
                    "user_id": "1" # Remplacer par l'ID de l'utilisateur
                    }  
            )

            if response.status_code == 200:
                user_data = response.json()
                email = user_data.get("email", "N/A")
                phone = user_data.get("phone", "N/A")
                license_key = user_data.get("license_key", "N/A")
                transaction_amount = user_data.get("total_transaction_amount", "N/A")
                subscription_plan = user_data.get("subscription_plan", "N/A")

                ctk.CTkLabel(self.right_frame, text=f"Your email: {email}").grid(row=1, column=0, pady=10)
                ctk.CTkLabel(self.right_frame, text=f"Your phone: {phone}").grid(row=2, column=0, pady=10)
                ctk.CTkLabel(self.right_frame, text=f"License key: {license_key}").grid(row=3, column=0, pady=10)
                ctk.CTkLabel(self.right_frame, text=f"Transaction amount: {transaction_amount}").grid(row=4, column=0, pady=10)
                ctk.CTkLabel(self.right_frame, text=f"Subscription plan: {subscription_plan}").grid(row=5, column=0, pady=10)
            else:
                ctk.CTkLabel(self.right_frame, text="Failed to display your information").grid(row=6, column=0, pady=10)

        except Exception as e:
            ctk.CTkLabel(self.right_frame, text=f"Error: {e}").grid(row=6, column=0, pady=10)




    def show_password_page(self):
        import webbrowser
        webbrowser.open("https://telegram-toolbox.online/auth/reset_request")


    def clear_main_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()


    def open_website(self):
        import webbrowser
        webbrowser.open("https://telegram-toolbox.online/software/contact-support")

