from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

LOCATORS = {
    "kwBox": "#KeywordOrPhrase",
    "lnBox": "#FinalistLastName",
    "cat":"#Category",
    "country":"#FairCountry",
    "state":"#FairState",
    "submit":"body > div > form > div > div:nth-child(15) > div > input"
}

class Scraper:
    def __init__(self, filename:str):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-cloud-import')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-client-side-phishing-detection')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--guest')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko)'
            'Chrome/142.0.0.0 Safari/537.36'
        )
        # chrome_options.add_argument("--headless=new")
        chrome_options.page_load_strategy = 'eager'
        service = ChromeService()
        self.driver = webdriver.Chrome(options=chrome_options, service=service)

        self.wdwait = WebDriverWait(self.driver,10)

        with open(filename, "r") as f:
            self.urls = f.read().splitlines()
        
    
    def run(self):
        for url in self.urls:
            
            self.scrape(url)

   

    def scrape(self, url):
        kwBox, lnBox, cat, country, state, submit = None, None, None, None, None, None
        try:
            self.driver.get(url)
            kwBox = self.wdwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOCATORS["kwBox"])))
            lnBox = self.wdwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOCATORS["lnBox"])))
            cat = self.wdwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOCATORS["cat"])))
            country = self.wdwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOCATORS["country"])))
            state = self.wdwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOCATORS["state"])))
            submit = self.wdwait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOCATORS["submit"])))
        except TimeoutException:
            print(f"Timeout while loading {url}")
            return
        
        
        kwBox.send_keys(" ")
        lnBox.send_keys(" ")
        Select(cat).select_by_index(0)
        Select(country).select_by_index(0)
        Select(state).select_by_index(0)
        sleep(2)
        try:
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(submit)).click()
            self.wdwait.until(EC.url_changes(url))
        except TimeoutException:
            print(f"Timeout while loading {url}")
            return
        print(f"Successfully loaded {url}")

        


    
