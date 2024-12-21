import uuid
import platform
import hashlib
import os

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
                serial = "unknown"
        except Exception:
            serial = "unknown"

        unique_data = f"{system_info}|{serial}".encode("utf-8")
        return hashlib.sha256(unique_data).hexdigest()


    