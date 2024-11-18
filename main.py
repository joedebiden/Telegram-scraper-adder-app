from telebox.managers.telegram_account_manager import TelegramAccountManager
from telebox.features.scraper import Scraper
from telebox.features.adder import Adder





if __name__ == "__main__":
    account_manager = TelegramAccountManager(session_name="my_session", proxy={"host": "proxy_host", "port": 1234})
    account_manager.connect_account()

    scraper = Scraper(account_manager)
    members = scraper.scrape_members("target_group")

    adder = Adder(account_manager)
    adder.add_members("destination_group", members)

    account_manager.disconnect_account()
