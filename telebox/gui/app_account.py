import customtkinter as ctk
from tkinter import messagebox
from managers.telegram_account_manager import AccountManager

class AccountManagerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telebox - Account Manager")
        self.geometry("1200x600")

        self.AccountManager = AccountManager()
        self.checkboxes = {}  

        # ===== Interface =====
        # section ajout de compte
        self.add_frame = ctk.CTkFrame(self, corner_radius=10)
        self.add_frame.pack(pady=20, padx=20, fill="x")

        self.label_section = ctk.CTkLabel(self.add_frame, text="Nom du compte:")
        self.label_section.pack(side="left", padx=10)
        self.entry_section = ctk.CTkEntry(self.add_frame, placeholder_text="Nom unique")
        self.entry_section.pack(side="left", padx=10)

        self.label_api_id = ctk.CTkLabel(self.add_frame, text="API ID:")
        self.label_api_id.pack(side="left", padx=10)
        self.entry_api_id = ctk.CTkEntry(self.add_frame, placeholder_text="API ID")
        self.entry_api_id.pack(side="left", padx=10)

        self.label_api_hash = ctk.CTkLabel(self.add_frame, text="API Hash:")
        self.label_api_hash.pack(side="left", padx=10)
        self.entry_api_hash = ctk.CTkEntry(self.add_frame, placeholder_text="API Hash")
        self.entry_api_hash.pack(side="left", padx=10)

        self.label_phone = ctk.CTkLabel(self.add_frame, text="Téléphone:")
        self.label_phone.pack(side="left", padx=10)
        self.entry_phone = ctk.CTkEntry(self.add_frame, placeholder_text="Numéro de téléphone")
        self.entry_phone.pack(side="left", padx=10)

        self.add_button = ctk.CTkButton(self.add_frame, text="Ajouter Compte", command=self.add_account)
        self.add_button.pack(side="left", padx=10)

        # Cadre pour l'affichage des comptes
        self.accounts_frame = ctk.CTkFrame(self, corner_radius=10)
        self.accounts_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.accounts_list_frame = ctk.CTkFrame(self.accounts_frame)
        self.accounts_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.select_all_button = ctk.CTkButton(self.accounts_frame, text="Tout Sélectionner", command=self.select_all)
        self.select_all_button.pack(side="left", padx=10)

        self.delete_selected_button = ctk.CTkButton(
            self.accounts_frame, text="Supprimer Sélectionnés", command=self.delete_selected_accounts
        )
        self.delete_selected_button.pack(side="right", padx=10)

        # Charger les comptes au démarrage
        self.display_accounts()

        """ Cadre pour la suppression des comptes
        self.delete_frame = ctk.CTkFrame(self, corner_radius=10)
        self.delete_frame.pack(pady=20, padx=20, fill="x")

        self.label_delete = ctk.CTkLabel(self.delete_frame, text="Nom du compte à supprimer:")
        self.label_delete.pack(side="left", padx=10)
        self.entry_delete = ctk.CTkEntry(self.delete_frame, placeholder_text="Nom du compte")
        self.entry_delete.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self.delete_frame, text="Supprimer Compte", command=self.delete_account)
        self.delete_button.pack(side="left", padx=10)
        """

    # ======= Méthodes liées aux Boutons =======
    def add_account(self):
        """Ajoute un compte via l'interface graphique."""
        manager = AccountManager() 
        section = self.entry_section.get()
        api_id = self.entry_api_id.get()
        api_hash = self.entry_api_hash.get()
        phone = self.entry_phone.get()

        if section and api_id and api_hash and phone:
            try:
                manager.add_account(section, api_id, api_hash, phone) 
                self.show_message(f"Account {section}added successfull.")
                self.clear_entries()
                self.display_accounts()
            except Exception as e:
                self.show_message(f"Error : {e}")
        else:
            self.show_message("Please complete all fields.")



    def display_accounts(self):
        """Affiche les comptes et leurs détails dans une zone formatée."""
        for widget in self.accounts_list_frame.winfo_children():
            widget.destroy()  # Réinitialise le contenu

        manager = AccountManager()
        accounts = manager.display_accounts()

        if accounts:
            for section, details in accounts.items():
                # Cadre pour chaque compte
                account_frame = ctk.CTkFrame(self.accounts_list_frame, corner_radius=10, fg_color="transparent")
                account_frame.pack(fill="x", padx=10, pady=5)

                # Titre : Nom du compte avec checkbox
                var = ctk.IntVar()  # Variable pour la checkbox
                checkbox = ctk.CTkCheckBox(account_frame, text=section, variable=var)
                checkbox.grid(row=0, column=0, sticky="w", padx=10)
                self.checkboxes[section] = var

                # Détails : API ID, API Hash, Téléphone
                row = 1
                for key, value in details.items():
                    label = ctk.CTkLabel(account_frame, text=f"{key}: {value}")
                    label.grid(row=row, column=0, sticky="w", padx=20, pady=2)
                    row += 1
        else:
            label = ctk.CTkLabel(self.accounts_list_frame, text="No account found.")
            label.pack(anchor="center", padx=10, pady=10)


    def select_all(self):
        """Sélectionne toutes les checkboxes."""
        for var in self.checkboxes.values():
            var.set(1)



    def delete_selected_accounts(self):
        """Supprime les comptes sélectionnés avec confirmation."""
        selected_accounts = [name for name, var in self.checkboxes.items() if var.get() == 1]
        if not selected_accounts:
            self.show_message("No account selected for deletion.")
            return

        # Confirmation
        confirm = messagebox.askyesno("Confirm", f"Do you want to remove {len(selected_accounts)} account(s) ?")
        if confirm:
            manager = AccountManager()
            for account in selected_accounts:
                manager.delete_account(account)  
            self.show_message(f"{len(selected_accounts)} successfully deleted account(s).")
            self.display_accounts() 



    def show_message(self, message):
        """Crée une boîte de dialogue avec CustomTkinter."""
        messagebox = ctk.CTkToplevel(self)
        messagebox.geometry("300x200")
        messagebox.grab_set()  # Empêche l'utilisateur d'interagir avec la fenêtre principale.

        label = ctk.CTkLabel(messagebox, text=message, wraplength=350, justify="center")
        label.pack(pady=20, padx=20)

        button = ctk.CTkButton(messagebox, text="OK", command=messagebox.destroy)
        button.pack(pady=10)



    def clear_entries(self):
        """Efface les champs d'entrée après un ajout."""
        self.entry_section.delete(0, "end")
        self.entry_api_id.delete(0, "end")
        self.entry_api_hash.delete(0, "end")
        self.entry_phone.delete(0, "end")