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

        self.label_section = ctk.CTkLabel(self.add_frame, text="Name account:")
        self.label_section.pack(side="left", padx=10)
        self.entry_section = ctk.CTkEntry(self.add_frame, placeholder_text="Choose unique name")
        self.entry_section.pack(side="left", padx=10)

        self.label_api_id = ctk.CTkLabel(self.add_frame, text="API ID:")
        self.label_api_id.pack(side="left", padx=10)
        self.entry_api_id = ctk.CTkEntry(self.add_frame, placeholder_text="API ID")
        self.entry_api_id.pack(side="left", padx=10)

        self.label_api_hash = ctk.CTkLabel(self.add_frame, text="API Hash:")
        self.label_api_hash.pack(side="left", padx=10)
        self.entry_api_hash = ctk.CTkEntry(self.add_frame, placeholder_text="API Hash")
        self.entry_api_hash.pack(side="left", padx=10)

        self.label_phone = ctk.CTkLabel(self.add_frame, text="Phone:")
        self.label_phone.pack(side="left", padx=10)
        self.entry_phone = ctk.CTkEntry(self.add_frame, placeholder_text="phone number")
        self.entry_phone.pack(side="left", padx=10)

        self.add_button = ctk.CTkButton(self.add_frame, text="Add account", command=self.add_account)
        self.add_button.pack(side="left", padx=10)

        # Cadre pour l'affichage des comptes
        self.accounts_frame = ctk.CTkFrame(self, corner_radius=10)
        self.accounts_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # cadre défilant pour la liste des comptes
        self.accounts_list_frame = ctk.CTkScrollableFrame(self.accounts_frame)
        self.accounts_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # cadre pour les boutons d'action
        self.footer_frame = ctk.CTkFrame(self, corner_radius=10)
        self.footer_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        self.select_all_button = ctk.CTkButton(self.footer_frame, text="Select all", command=self.select_all)
        self.select_all_button.pack(side="left", padx=10)

        self.refresh_button = ctk.CTkButton(self.footer_frame, text="Refresh", command=self.display_accounts)
        self.refresh_button.pack(side='left', pady=10)

        self.delete_selected_button = ctk.CTkButton(self.footer_frame, text="Remove Selected", command=self.delete_selected_accounts)
        self.delete_selected_button.pack(side="right", padx=10)

        self.display_accounts()


    # ======= Méthodes liées aux Boutons =======
    def add_account(self):
        """Ajoute un compte via l'interface graphique."""
        section = self.entry_section.get()
        api_id = self.entry_api_id.get()
        api_hash = self.entry_api_hash.get()
        phone = self.entry_phone.get()

        if section and api_id and api_hash and phone:
            try:
                self.AccountManager.add_account(section, api_id, api_hash, phone) 
                self.show_message(f"Account {section}added successfull.")
                self.clear_entries()
                self.display_accounts()
            except Exception as e:
                self.show_message(f"Error : {e}")
        else:
            self.show_message("Please complete all fields.")



    def validate_inputs(self, section, api_id, api_hash, phone):
        """Valide les entrées de l'utilisateur."""
        return all([section.strip(), api_id.strip(), api_hash.strip(), phone.strip()])



    def display_accounts(self):
        """Affiche les comptes et leurs détails dans une zone formatée."""
        accounts = self.AccountManager.display_accounts()

        for widget in self.accounts_list_frame.winfo_children():
            widget.destroy()
        self.checkboxes.clear()

        if accounts:
            for section, details in accounts.items():
                account_frame = ctk.CTkFrame(self.accounts_list_frame, corner_radius=10, fg_color="transparent")
                account_frame.pack(fill="x", padx=10, pady=5)

                var = ctk.IntVar()  
                checkbox = ctk.CTkCheckBox(account_frame, text=section, variable=var)
                checkbox.grid(row=0, column=0, sticky="w", padx=10)
                self.checkboxes[section] = var

                # Détails : API ID, API Hash, Téléphone
                row = 1
                for key, value in details.items():
                    label_key = ctk.CTkLabel(account_frame, text=f"{key}:")
                    label_key.grid(row=row, column=0, sticky="w", padx=20, pady=2)
                    entry_value = ctk.CTkEntry(account_frame, width=200)
                    entry_value.insert(0, value)
                    entry_value.configure(state="readonly") # a changer pour avoir la modification
                    entry_value.grid(row=row, column=1, sticky="w", padx=20, pady=2)
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
            for account in selected_accounts:
                self.AccountManager.delete_account(account)  
            self.show_message(f"{len(selected_accounts)} successfully deleted account(s).")
            self.display_accounts() 



    def show_message(self, message):
        """Affiche une boîte de dialogue avec CustomTkinter."""
        messagebox.showinfo("Message ", message)



    def clear_entries(self):
        """Efface les champs d'entrée après un ajout."""
        self.entry_section.delete(0, "end")
        self.entry_api_id.delete(0, "end")
        self.entry_api_hash.delete(0, "end")
        self.entry_phone.delete(0, "end")