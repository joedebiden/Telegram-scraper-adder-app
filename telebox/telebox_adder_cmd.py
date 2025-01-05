from features.adder import Adder
from tkinter import filedialog

if __name__ == "__main__":

    adder = Adder(session_name='session_name', config_file='account.data')


    available_accounts = adder.list_accounts()
    
    section_name = input("[+] Enter the account name to use: ")
    if section_name not in available_accounts:
        print("[!] Account not found.")
        exit()
    else:
        adder.section_name = section_name
        adder.read_account_details()
    
    adder.connect()
    adder.get_account_info()

    
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        users = adder.open_file(file_path)

    
    groups = adder.get_groups()
    if not groups:
        print("[!] No groups available.")
        adder.disconnect()
        exit()

    target_group = adder.select_group(groups)
    if not target_group:
        print("[!] No group selected.")
        adder.disconnect()
        exit()

    
    print(["Very slow", "Normal", "Fast", "Very fast"])
    inputspeed = input("Select your speed :")
    speed = adder.set_speed_mode(inputspeed)
    if not speed:
        print("[!] Invalid speed.")
        adder.disconnect()
        exit()

 
    adder.add_users(target_group, users, speed)
    

    adder.disconnect()
