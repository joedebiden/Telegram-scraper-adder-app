from ..features.checker import DeviceChecker
"""
At telegram-online-tools-apps-builder> path
$ python.exe -m telebox.tests.test_checker
"""


checker = DeviceChecker()

print(f"Device ID: {checker.get_device_id()}")
print(f"Device Fingerprint: {checker.get_device_fingerprint()}")