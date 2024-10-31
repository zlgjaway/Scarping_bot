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
        self.df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title'])
        print(self.df)

    def request_item(self):
        try:
            api  = finding(appid=self.api_key, config_file=None )
            response = api.execute('findItemsAdvanced', {'keywords': self.df})
            for item in response.reply.searchResult.item:
                print("Price: {item.sellingStatus}")
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

scraper =  EbayScraper(API_key)
scraper.request_item()
