if __name__ == "__main__":

    from src.Scraper import Scraper
    scraper = Scraper("config/url.txt")
    scraper.run()