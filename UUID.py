#import uuid
#print(uuid.getnode())

import winreg

def get_machine_guid():
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Cryptography"
    )
    value, _ = winreg.QueryValueEx(key, "MachineGuid")
    return value

print(get_machine_guid())