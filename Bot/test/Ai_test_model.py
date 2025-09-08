import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import time

class EbayScraper: #not percios to keyworld 
    def __init__(self):
        load_dotenv()
        #self.min_price = 10
        #self.max_price = 200
        self.App_ID = os.getenv("App_ID")
        self.OAuth = os.getenv("OAuth")
        self.url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self.API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-V3.1"
        self.headers = {"Authorization": "Bearer YOUR_HF_API_TOKEN"}

    def import_data(self):
        # Read and filter the data
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title', 'price'])
        #filtered_df = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords = df['title'].tolist()  # FIX: This was ['title'] before, which is just a string
        return keywords
    
        
    # use ai to filter ebay api data
    def query_model(self,prompt):
        payload = {"inputs": prompt}
        response = requests.post(self.API_URL, json=payload, headers=self.headers)
        return response.json()

    # Example usage
    prompt = "Extract brand, model, condition, and category: 'Nintendo 64 console + 2 controllers, used'"
    result = query_model(prompt)
    print(result)


    def get_sold_count(self, keyword): # api lock
        url = "https://svcs.ebay.com/services/search/FindingService/v1"
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "findCompletedItems",
            "X-EBAY-SOA-SECURITY-APPNAME": self.App_ID,  # Still required
            "X-EBAY-SOA-REQUEST-DATA-FORMAT": "JSON",
            "Authorization": f"Bearer {self.OAuth}"
        }
        params = {
            "keywords": keyword,
            "GLOBAL-ID": "EBAY-AU",
            "itemFilter(0).name": "SoldItemsOnly",
            "itemFilter(0).value": "true",
            "paginationInput.entriesPerPage": "100"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                sold_count = int(
                    data["findCompletedItemsResponse"][0]
                    ["paginationOutput"][0]
                    ["totalEntries"][0]
                )
                return sold_count
            except Exception as e:
                print(f"Error parsing sold count for '{keyword}': {e}")
                return 0
        else:
            print(f"Error in Finding API for '{keyword}':", response.status_code, response.text)
            return 0
        
    def scrape_Ebay(self, keywords):
        all_product_elements = []

        for keyword in keywords:
            headers = {
                "Authorization": f"Bearer {self.OAuth}",
                "Content-Type": "application/json",
                "X-EBAY-C-MARKETPLACE-ID": "EBAY_AU"
            }
            params = {
                "q": keyword,
                "limit": "10",
                "filter": "conditionIds:{3000|2500},itemLocationCountry:AU"
            }
            response = requests.get(self.url, headers=headers, params=params)

            if response.status_code == 200:
                items = response.json()
                active_count = items.get("total", 0)   # total active listings

                count = 0
                total_price = 0
                for item in items.get("itemSummaries", []):
                    try:
                        price = float(item['price']['value'])
                        print(f"{item['title']} - ${price}")
                        total_price += price
                        count += 1
                    except Exception as e:
                        print(f"Error parsing item for '{keyword}': {e}")

                average_price = total_price / count if count > 0 else None

                # --- Call Finding API for sold count ---
                sold_count = self.get_sold_count(keyword)
                time.sleep(2)

                # --- STR ---
                STR = (sold_count / active_count * 100) if active_count else 0

                all_product_elements.append({
                    "keyword": keyword,
                    "average_price": average_price,
                    "active_count": active_count,
                    "sold_count": sold_count,
                    "STR": STR #Sell-Through Rate
                })
            else:
                print(f"Error with keyword '{keyword}':", response.status_code, response.text)

        return all_product_elements

    def save_to_csv(self, extract_data):
        df = pd.DataFrame(extract_data)

        # Create blank rows for spacing
        spacing_rows = [{"keyword": "", "average_price": None, "active_count": "", "sold_count": "","STR": ""}]
        spaced_data = []

        for i in range(0, len(df), 10):
            spaced_data.extend(df.iloc[i:i+10].to_dict('records'))
            spaced_data.extend(spacing_rows)

        spaced_df = pd.DataFrame(spaced_data)
        spaced_df.to_csv('ebay_data.csv', index=False)
        print("Data saved to ebay_data.csv")

# Main run
scraper = EbayScraper()
keywords = scraper.import_data()
products = scraper.scrape_Ebay(keywords)
scraper.save_to_csv(products)
