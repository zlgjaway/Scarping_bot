import os
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from dotenv import load_dotenv
import datetime
import pandas as pd
load_dotenv()
API_key =os.getenv("api_key")

class EbayScraper(object):
    def __init__(self, API_key):
        self.api_key = API_key

    def extract_csv(self):
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title'])
        keywords = df['title'].tolist()  
        print(keywords)
        return  keywords

scraper = EbayScraper(API_key)
keywords = scraper.extract_csv()