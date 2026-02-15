import requests
import csv
import os
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, filename:str):
        with open(filename, "r") as f:
            self.urls = f.read().splitlines()
        
    
    def run(self):
        for url in self.urls:
            self.scrape(url)

    def scrape(self, url:str):
        
        session = requests.Session()

        response = session.get(url)
        
        if response.status_code == 200:
            
            print(f"Successfully scraped {url}")
        else:
            print(f"Failed to scrape {url} with status code {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']


        data = {
            'KeywordOrPhrase': '',
            'FinalistLastName': '',
            'Category': 'Any Category',
            'FairCountry': 'Any Country',
            'FairState': 'Any State',
            'SelectedIsefYears': '0',
            'IsGetAllAbstracts': 'True',
            '__RequestVerificationToken': token,
        }

        response = session.post('https://abstracts.societyforscience.org/', data=data)
        if response.status_code == 200:
            print(f"Successfully posted to {url}")
        else:
            print(f"Failed to post to {url} with status code {response.status_code}") 
            return

        soup = BeautifulSoup(response.content, 'html.parser')   
        print(f"Successfully parsed HTML from {url}")
        data = []
        for row in soup.find_all('tr'):
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if cols: data.append(cols)
        print(f"Successfully extracted data from {url}")
        # Save to CSV
        os.makedirs('current', exist_ok=True)
        with open('current/dataset.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Year', 'Finalist Name(s)', 'Project Title', 'Category', 'Fair Country', 'Fair State', 'Fair Province', "Awards Won"])
            writer.writerows(data)
        print(f"Successfully saved data to current/dataset.csv from {url}")