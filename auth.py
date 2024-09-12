import configparser
import asyncio
import socks
import random
from telethon import TelegramClient
from telethon.tl.functions.account import GetAuthorizationsRequest

# Lecture des configurations API et du téléphone
cpass = configparser.RawConfigParser()
cpass.read('config.data')

api_id = cpass['cred']['id']
api_hash = cpass['cred']['hash']
phone = cpass['cred']['phone']

# Lecture des proxies depuis le fichier de configuration
proxy_config = configparser.ConfigParser()
proxy_config.read('proxies.ini')
proxy_sections = proxy_config.sections()
selected_proxy = random.choice(proxy_sections)

proxy = (
    socks.SOCKS5, 
    proxy_config[selected_proxy]['host'], 
    int(proxy_config[selected_proxy]['port']),
    True,  
    proxy_config[selected_proxy].get('username'), 
    proxy_config[selected_proxy].get('password')
)

async def auth():
    client = TelegramClient(
        session=phone,
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy
    )
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input('[+] Enter the code sent from Telegram: ')
        await client.sign_in(phone, code)
    
    sessions = await client(GetAuthorizationsRequest())
    print(sessions)

if __name__ == '__main__':
    asyncio.run(auth())


''' code bien fait 
proxy = (socks.SOCKS5, proxy_ip, int(proxy_port), True, proxy_login, proxy_password)

async def auth():
    client = TelegramClient(
        session=phone,
        api_id=api_id,
        api_hash=api_hash,
        proxy=proxy
    )
    await client.connect()
    sessions = await client(GetAuthorizationsRequest())
    print(sessions)


if __name__ == '__main__':
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auth())
'''