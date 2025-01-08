import uuid
import platform
import requests
import hashlib
import os
from datetime import datetime
import pytz
import time
from functools import wraps

class DeviceChecker:
    """
    L'objectif de cette classe et de retourner un device id pour le stocker côté serveur et ainsi assurer l'utilisation unique du software.
    Pour un bon device id il faut:
    Combinez plusieurs sources (adresse MAC, numéro de série, CPU, etc.).
    Hachez les données avec une fonction comme SHA256 pour éviter de stocker des informations en clair.
    """

    def get_device_id(self):
        """Retourne un identifiant unique pour l'appareil"""
        return uuid.getnode()

    

    def get_device_fingerprint(self):
        """Retourne une empreinte numérique unique pour l'appareil"""
        system_info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
        }
        # Numéro de série du disque dur (Windows/Linux/Mac)
        try:
            if system_info["os"] == "Windows":
                serial = os.popen("wmic diskdrive get SerialNumber").read().strip()
            elif system_info["os"] == "Linux":
                serial = os.popen("sudo hdparm -I /dev/sda | grep Serial").read().strip()
            elif system_info["os"] == "Darwin":  # macOS
                serial = os.popen("system_profiler SPHardwareDataType | grep Serial").read().strip()
            else:
                try:
                    serial = os.popen("sudo dmidecode -s system-serial-number").read().strip()
                    if not serial:
                        serial = os.popen("cat /sys/class/dmi/id/product_serial").read().strip()
                except Exception:
                    serial = "unknown"
        except Exception:
            serial = "unknown"
        
        unique_data = f"{system_info}|{serial}".encode("utf-8")
        return hashlib.sha256(unique_data).hexdigest()


    def get_date(self):
        """Retourne la date en France"""
        paris_tz = pytz.timezone('Europe/Paris') 
        Fr_current_date = datetime.now(paris_tz)

        return Fr_current_date.isoformat() # permet de le rendre serializable en JSON
    


    def check_lisense_inapp(self):
        """Vérifie si la licence est valide dans l'application"""
        response = requests.post("http://93.127.202.5:5002/license/check-inapp", json={
            "device_id": self.get_device_fingerprint(),
        })
        if response.status_code == 200:
            return True
        else:
            return False
    



class RateLimiter():
    
    def rate_limited(max_per_minute):
        """
        Cette méthode permet de limiter le nombre de requêtes 
        par minute elle s'implémente en utilisant un décorateur    
        """
        min_interval = 60.0 / float(max_per_minute)
        def decorator(func):
            last_time_called = [0.0]
            @wraps(func)
            def rate_limited_function(*args, **kwargs):
                elapsed = time.time() - last_time_called[0]
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                last_time_called[0] = time.time()
                return func(*args, **kwargs)
            return rate_limited_function
        return decorator


