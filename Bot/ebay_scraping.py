from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import pandas as pd
import requests
import time

class EbayScraper:
    def __init__(self):
        load_dotenv()
        #self.min_price = 10
        #self.max_price = 200
        self.OAuth = os.getenv("OAuth")
        self.url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    def import_data(self):
        # Read and filter the data
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title', 'price'])
        #filtered_df = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords = df['title'].tolist()  # FIX: This was ['title'] before, which is just a string
        return keywords

    def scrape_Ebay(self, keywords):
        all_product_elements = []

        for keyword in keywords:
            headers = {
                "Authorization": f"Bearer {self.OAuth}",
                "Content-Type": "application/json"
            }
            params = {
                "q": keyword,
                "limit": "10"
            }
            response = requests.get(self.url, headers=headers, params=params)

            if response.status_code == 200:
                items = response.json()
                for item in items.get("itemSummaries", []):
                    try:
                        title = item['title']
                        price = float(item['price']['value'])
                        url = item.get('itemWebUrl', '')
                        print(f"{item['title']} - ${item['price']['value']}")
                        all_product_elements.append({
                            "title": title,
                            "price": price,
                            "url": url
                        })
                    except Exception as e:
                        print(f"Error parsing item: {e}")
            else:
                print("Error:", response.status_code, response.text)

        return all_product_elements

    def save_to_csv(self, extract_data):
        df = pd.DataFrame(extract_data)

        # Create blank rows for spacing
        spacing_rows = [{"title": "", "price": None, "url": ""}]
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
