from features.scraper import Scraper

if __name__ == "__main__":
    
    # to fetch on account.data
    api_id = 123456
    api_hash = "your_api_hash"
    phone = "+1234567890"
    session_name = "my_session"

    scraper = Scraper(session_name, api_id, api_hash, phone)
    scraper.perform_task()
