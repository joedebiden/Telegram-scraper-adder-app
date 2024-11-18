# Logique lecture licence in app
import requests
import time

LICENSE_SERVER_URL = "https://telegram-toolbox.online/license/check"


def check_license():
    try:
        with open("license.key", "r") as f:
            license_key = f.read().strip()
   
        response = requests.post(LICENSE_SERVER_URL, json={"license_key": license_key})
        if response.status_code == 200:
            print("License key is valid.")
            return True
        
        else:
            print("Invalid license key. Please contact support: https://telegram-toolbox.online/software/contact-support")
            time.sleep(2)
            return False
        
    except FileNotFoundError:
        print("License file not found. Please run the setup.app again or create a file named 'license.key'...")
        time.sleep(2)
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the license server: {e}")
        time.sleep(2)
        return False


if not check_license():
    time.sleep(2)
    exit(1)       

