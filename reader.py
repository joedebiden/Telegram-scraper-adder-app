import requests
import sys


LICENSE_SERVER_URL = "http://93.127.202.5:5000/check-license"

def verify_license(license_key):
    
    response = requests.post(LICENSE_SERVER_URL, json={"license_key": license_key})
    
    if response.status_code == 200:
        print("Licence validée, accès autorisé.")
    else:
        print("Licence non valide. Accès refusé.")
        sys.exit(1) 

if __name__ == "__main__":
    
    license_key = input("Entrez votre clé de licence : ")
    
    
    verify_license(license_key)

    #  12345-FGHIJ-6789
    print("Lancement de l'application...")

