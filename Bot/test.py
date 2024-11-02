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
    
    def check_api_usage(self):
        try:
            api = finding(appid=self.api_key, config_file=None)
            response = api.execute('GetApiUsage', {})
            api_calls_remaining = response.reply.ApiUsage.Remaining
            api_calls_made = response.reply.ApiUsage.Made
            print(f"API Calls Made: {api_calls_made}, API Calls Remaining: {api_calls_remaining}")
        except ConnectionError as e:
            print(f"Error checking API usage: {e.response.dict()}")
        
    def request_item(self):
        self.check_api_usage()

scraper = EbayScraper(API_key)
scraper.request_item()    # Pass all keywords at once

