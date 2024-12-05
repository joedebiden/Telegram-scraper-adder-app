import customtkinter as ctk
from tkinter import messagebox
from features.scraper import Scraper

class ScraperUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Telegram Scraper")
        self.geometry("1200x600")

        # Scraper instance
        self.scraper = Scraper()

        # Dictionaries for checkboxes
        self.account_vars = {}  # Checkboxes for accounts
        self.group_vars = {}    # Checkboxes for groups

        # Frames
        self.account_frame = ctk.CTkFrame(self, corner_radius=10)
        self.account_frame.pack(fill="x", padx=20, pady=10)

        self.group_frame = ctk.CTkFrame(self, corner_radius=10)
        self.group_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.action_frame = ctk.CTkFrame(self, corner_radius=10)
        self.action_frame.pack(fill="x", padx=20, pady=10)

        # UI Elements
        self.create_account_ui()
        self.create_group_ui()
        self.create_action_ui()

        # Load accounts initially
        self.display_accounts()



    def create_account_ui(self):
        """UI for managing accounts."""
        account_label = ctk.CTkLabel(self.account_frame, text="Available Accounts")
        account_label.pack(anchor="w", padx=10)

        self.account_list_frame = ctk.CTkFrame(self.account_frame, fg_color="transparent")
        self.account_list_frame.pack(fill="x", pady=5)

        self.connect_button = ctk.CTkButton(self.account_frame, text="Connect", command=self.connect_account)
        self.connect_button.pack(side="left", padx=10, pady=5)



    def create_group_ui(self):
        """UI for displaying and selecting groups."""
        group_label = ctk.CTkLabel(self.group_frame, text="Available Groups/Channels")
        group_label.pack(anchor="w", padx=10)

        self.group_list_frame = ctk.CTkFrame(self.group_frame, fg_color="transparent")
        self.group_list_frame.pack(fill="both", expand=True, pady=5)



    def create_action_ui(self):
        """UI for actions like scraping and saving."""
        self.scrape_button = ctk.CTkButton(self.action_frame, text="Scrape Selected Groups", command=self.scrape_selected_groups)
        self.scrape_button.pack(side="left", padx=10, pady=5)

        self.save_button = ctk.CTkButton(self.action_frame, text="Save to File", command=self.save_to_file)
        self.save_button.pack(side="left", padx=10, pady=5)



    def display_accounts(self):
        """Display available accounts."""
        accounts = self.scraper.list_accounts()

        for widget in self.account_list_frame.winfo_children():
            widget.destroy()

        self.account_vars.clear()
        for account in accounts:
            var = ctk.IntVar()
            checkbox = ctk.CTkCheckBox(self.account_list_frame, text=account, variable=var)
            checkbox.pack(anchor="w", padx=10)
            self.account_vars[account] = var



    def connect_account(self):
        """Connect to the selected Telegram account."""
        selected_account = [account for account, var in self.account_vars.items() if var.get() == 1]

        if len(selected_account) != 1:
            messagebox.showerror("Error", "Please select exactly one account to connect.")
            return

        account_name = selected_account[0]
        try:
            # self.scraper.load_account(account_name)
            self.scraper.connect()
            messagebox.showinfo("Success", f"Connected to account: {account_name}")
            # self.get_groups()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")



    def display_groups(self):
        """Display available groups/channels."""
        groups = self.scraper.get_groups()

        for widget in self.group_list_frame.winfo_children():
            widget.destroy()

        self.group_vars.clear()
        for group in groups:
            var = ctk.IntVar()
            checkbox = ctk.CTkCheckBox(self.group_list_frame, text=group.title, variable=var)
            checkbox.pack(anchor="w", padx=10)
            self.group_vars[group] = var



    def scrape_selected_groups(self):
        """Scrape selected groups."""
        selected_groups = [group for group, var in self.group_vars.items() if var.get() == 1]

        if not selected_groups:
            messagebox.showerror("Error", "Please select at least one group to scrape.")
            return

        try:
            self.scraped_data = {}
            for group in selected_groups:
                members = self.scraper.scrape_group_members(group)
                self.scraped_data[group.title] = members
            messagebox.showinfo("Success", "Scraping completed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape groups: {e}")



    def save_to_file(self):
        """Save scraped data to a file."""
        if not hasattr(self, 'scraped_data') or not self.scraped_data:
            messagebox.showerror("Error", "No data to save. Scrape groups first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Group", "Username", "User ID", "Name"])
                for group, members in self.scraped_data.items():
                    for member in members:
                        username = member.username or ""
                        name = f"{member.first_name or ''} {member.last_name or ''}".strip()
                        writer.writerow([group, username, member.id, name])
            messagebox.showinfo("Success", f"Data saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")


