import configparser

with open('config.data', 'w') as f:
    f.write('')
print("[*] Please connect you to https://my.telegram.org/ \n")
cpass = configparser.RawConfigParser()
cpass.add_section('cred')
xid = input("[+] enter api ID : ")
cpass.set('cred', 'id', xid)
xhash = input("[+] enter hash ID : ")
cpass.set('cred', 'hash', xhash)
xphone = input("[+] enter phone number : ")
cpass.set('cred', 'phone', xphone)
setup = open('config.data', 'w')
cpass.write(setup)
setup.close()
print("[+] setup complete !")

#python setup code source