import requests

LICENSE_SERVER_URL = "http://93.127.202.5:5000/check-license"


def check_license():
    try:
        with open("license.key", "r") as f:
            license_key = f.read().strip()
   
        response = requests.post(LICENSE_SERVER_URL, json={"license_key": license_key})
        if response.status_code == 200:
            print("License key is valid.")
            return True
        
        else:
            print("Invalid license key. Please contact support.")
            return False
        
    except FileNotFoundError:
        print("License file not found. Please run the setup.app again or create a file named 'license.key'...")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the license server: {e}")
        return False


if not check_license():
    exit(1)       

