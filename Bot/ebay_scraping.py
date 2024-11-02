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
        self.max_price = 500
        self.min_price = 10
        self.limit_rate = 5000

    def extract_csv(self):
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords =  filtered_df['title'].tolist()
        return  keywords
    
    def request_item(self, keywords):
        call_rate = 0
        while call_rate <= self.limit_rate : 
            try:
                api  = finding(appid=self.api_key, config_file=None )
                for keyword in keywords:    
                    response = api.execute('findCompletedItems', {
                        'keywords': keyword,  
                        'sortOrder': 'EndTimeSoonest',    
                        'paginationInput': {
                        'entriesPerPage': 10,         
                        'pageNumber': 1
                        }
                    })
                    print (response)
                call_rate = call_rate +1
                for item in response.reply.searchResult.item:
                    print(f"Price: {item.currentPrice.value}")
            except ConnectionError as e:
                print(e.response.dict())

scraper = EbayScraper(API_key)
keywords = scraper.extract_csv()  # Get all keywords
scraper.request_item(keywords)    # Pass all keywords at once

