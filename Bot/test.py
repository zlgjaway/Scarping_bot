import os
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
API_key =os.getenv("api_key")

class EbayScraper(object):
    def __init__(self, API_key):
        self.api_key = API_key
        self.max_price = 500
        self.min_price = 10
        self.limit_rate = 1

    def extract_csv(self):
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords =  filtered_df['title'].tolist()
        return  keywords
    
    def request_item(self, keywords):
        call_rate = 0
        item_extract = []
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
            
                for item in response.reply.searchResult.item:
                    item_extract = item.currentPrice.value
                    return item_extract
            except ConnectionError as e:
                print(e.response.dict())
        call_rate +1
    def save_to_csv(self,data):
        df = pd.DataFrame(data)
        df.to_csv('ebay_data.csv', index=False)
        print(df)

scraper = EbayScraper(API_key)
keywords = scraper.extract_csv()  # Get all keywords
data = scraper.request_item(keywords)    # Pass all keywords at once
scraper.save_to_csv(data)

