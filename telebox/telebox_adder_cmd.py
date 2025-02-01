from features.adder import Adder
from tkinter import filedialog
import os
from time import sleep


def banner():
    os.system('cls')
    print(r'''
          ______               __                 ______         __        __                     
         /      \             /  |               /      \       /  |      /  |                    
        /$$$$$$  | __    __  _$$ |_     ______  /$$$$$$  |  ____$$ |  ____$$ |  ______    ______  
        $$ |__$$ |/  |  /  |/ $$   |   /      \ $$ |__$$ | /    $$ | /    $$ | /      \  /      \ 
        $$    $$ |$$ |  $$ |$$$$$$/   /$$$$$$  |$$    $$ |/$$$$$$$ |/$$$$$$$ |/$$$$$$  |/$$$$$$  |
        $$$$$$$$ |$$ |  $$ |  $$ | __ $$ |  $$ |$$$$$$$$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
        $$ |  $$ |$$ \__$$ |  $$ |/  |$$ \__$$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |$$$$$$$$/ $$ |      
        $$ |  $$ |$$    $$/   $$  $$/ $$    $$/ $$ |  $$ |$$    $$ |$$    $$ |$$       |$$ |      
        $$/   $$/  $$$$$$/     $$$$/   $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/ $$/       

                                                                    by @Bodelaire
                                                                    https://telegram-toolbox.online/
          ''')



if __name__ == "__main__":

    adder = Adder(session_name='session_name', config_file='account.data')


    while True:
        banner()

        available_accounts = adder.list_accounts()
        if not available_accounts:
            print("[?] There is no account in your file, please take time to add an account...")
            sleep(2)
            break
        
        section_name = input("[+] Enter the account name to use: ")
        if section_name not in available_accounts:
            print("[!] Account not found. Restarting...")
            sleep(2)
            continue

        
        adder.section_name = section_name
        adder.read_account_details()
        
        try:
            adder.connect()
            adder.get_account_info()
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            sleep(1)
            continue

        print("[+] Please select a list of users to add in your group")
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            print("[!] No list of users detected. Restarting...")
            adder.disconnect()
            sleep(1)
            continue

        users = adder.open_file(file_path)

        groups = adder.get_groups()
        if not groups:
            print("[!] No groups available. Restarting...")
            adder.disconnect()
            sleep(1)
            continue

        target_group = adder.select_group(groups)
        if not target_group:
            print("[!] No group selected. Restarting...")
            adder.disconnect()
            continue

        
        print(["Very slow", "Normal", "Fast", "Very fast"])
        inputspeed = input("Select your speed :")
        speed = adder.set_speed_mode(inputspeed)
        if not speed:
            print("[!] Invalid speed. Restarting...")
            adder.disconnect()
            sleep(1)
            continue

    
        adder.add_users(target_group, users, speed)
        
        adder.disconnect()

        retry = input("[?] Do you want to run again? (yes/no): ")
        if retry.lower() !='yes':
            sleep(1)
            break
