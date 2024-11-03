import os
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()
API_key = os.getenv("api_key")

class EbayScraper(object):
    def __init__(self, API_key):
        self.api_key = API_key
        self.max_price = 500
        self.min_price = 10
        self.limit_rate = 1

    def extract_csv(self):
        # Read and filter data from CSV file
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title', 'price'])
        filtered_df = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords = filtered_df['title'].tolist()
        return keywords
    
    def request_item(self, keywords):
        call_rate = 0
        items_data = []  # Collect all extracted items here

        while call_rate < self.limit_rate: 
            try:
                api = finding(appid=self.api_key, config_file=None)
                
                # Iterate over keywords to query eBay API
                for keyword in keywords:
                    response = api.execute('findCompletedItems', {
                        'keywords': keyword,  
                        'sortOrder': 'EndTimeSoonest',    
                        'paginationInput': {
                            'entriesPerPage': 10,         
                            'pageNumber': 1
                        }
                    })
                    print(response)

                    # Extract item data
                    for item in response.reply.searchResult.item:
                        items_data.append({
                            "title": keyword,
                            "price": float(item.sellingStatus.currentPrice.value),
                            "currency": item.sellingStatus.currentPrice._currencyId,
                            "item_id": item.itemId,
                            "listing_url": item.viewItemURL
                        })
                call_rate += 1
                time.sleep(1)  # Pause to avoid hitting rate limits

            except ConnectionError as e:
                print(f"Error with eBay API request: {e.response.dict()}")
                break
        
        return items_data

    def save_to_csv(self, data):
        # Save data to CSV
        df = pd.DataFrame(data)
        df.to_csv('ebay_data.csv', index=False)
        print("Data saved to ebay_data.csv")
        print(df)

# Usage
scraper = EbayScraper(API_key)
keywords = scraper.extract_csv()  # Get all keywords from CSV
data = scraper.request_item(keywords)    # Pass all keywords to eBay API
scraper.save_to_csv(data)  # Save results to CSV