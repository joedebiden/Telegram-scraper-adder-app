import customtkinter as ctk
from ..managers.telegram_account_manager import AccountManager

class AccountManagerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telebox - Account Manager")
        self.geometry("800x600")

        self.AccountManager = AccountManager()

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

        self.accounts_list = ctk.CTkTextbox(self.accounts_frame, wrap="word")
        self.accounts_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_button = ctk.CTkButton(self.accounts_frame, text="Afficher les Comptes", command=self.display_accounts)
        self.refresh_button.pack(pady=10)

        # Cadre pour la suppression des comptes
        self.delete_frame = ctk.CTkFrame(self, corner_radius=10)
        self.delete_frame.pack(pady=20, padx=20, fill="x")

        self.label_delete = ctk.CTkLabel(self.delete_frame, text="Nom du compte à supprimer:")
        self.label_delete.pack(side="left", padx=10)
        self.entry_delete = ctk.CTkEntry(self.delete_frame, placeholder_text="Nom du compte")
        self.entry_delete.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self.delete_frame, text="Supprimer Compte", command=self.delete_account)
        self.delete_button.pack(side="left", padx=10)


    # ======= Méthodes liées aux Boutons =======
    def add_account(self):
        """Ajoute un compte via l'interface graphique."""
        section = self.entry_section.get()
        api_id = self.entry_api_id.get()
        api_hash = self.entry_api_hash.get()
        phone = self.entry_phone.get()

        if section and api_id and api_hash and phone:
            try:
                self.manager.add_account(section, api_id, api_hash, phone)
                self.show_message(f"Compte {section} ajouté avec succès.")
                self.clear_entries()
            except Exception as e:
                self.show_message(f"Erreur : {e}")
        else:
            self.show_message("Veuillez remplir tous les champs.")

    def display_accounts(self):
        """Affiche les comptes dans la zone de texte."""
        accounts = self.manager.display_accounts()
        self.accounts_list.delete("1.0", "end")
        if accounts:
            for section, details in accounts.items():
                account_details = f"Compte: {section}\n"
                for key, value in details.items():
                    account_details += f"  {key}: {value}\n"
                account_details += "\n"
                self.accounts_list.insert("end", account_details)
        else:
            self.accounts_list.insert("end", "Aucun compte enregistré.")

    def delete_account(self):
        """Supprime un compte via l'interface graphique."""
        section = self.entry_delete.get()
        if section:
            success = self.manager.delete_account(section)
            if success:
                self.show_message(f"Compte {section} supprimé avec succès.")
                self.display_accounts()
            else:
                self.show_message(f"Compte {section} introuvable.")
            self.entry_delete.delete(0, "end")
        else:
            self.show_message("Veuillez entrer le nom du compte à supprimer.")

    def show_message(self, message):
        """Affiche un message d'information."""
        ctk.CTkMessagebox.show_info(title="Message", message=message)

    def clear_entries(self):
        """Efface les champs d'entrée après un ajout."""
        self.entry_section.delete(0, "end")
        self.entry_api_id.delete(0, "end")
        self.entry_api_hash.delete(0, "end")
        self.entry_phone.delete(0, "end")