from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
import os
import re
import pandas as pd
import time
import requests

class EbayScraper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("ebay_email")
        self.password = os.getenv("ebay_pass")
        self.driver = webdriver.Chrome()
        self.min_price = 10
        self.max_price = 200
        self.url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self.OAuth = os.getenv("OAuth")
   
    def import_data (self):
         #/home/zlgjaway/Documents/ScarpingBot_project/facebook_marketplace_data.csv
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords =  ['title'].tolist()
        print(keywords)
        return  keywords 
    
    def scrape_Ebay(self, keywords):
        all_product_elements = []
        for keyword in keywords:
            # Find and clear the search input field, then enter the keyword
            search_input = self.driver.find_element(By.ID, "gh-ac")
            search_input.clear()
            search_input.send_keys(keyword)

            headers = {
                "Authorization": f"Bearer {self.OAuth}",
                "Content-Type": "application/json",
            }
            params = {
                "q": keyword,
                "limit": "10"
            }
            response = requests.get(self.url, headers=headers, params=params)
            if response.status_code == 200:
                items = response.json()
                for item in items.get("itemSummaries", []):
                    print(f"{item['title']} - ${item['price']['value']}")
                    all_product_elements.append[item]
            else:
                print("Error:", response.text)

    
        
        return all_product_elements
    

    def save_to_csv(self,extract_data):
        df = pd.DataFrame(extract_data)
        
        # Create blank rows for spacing
        spacing_rows = [{"title": "", "price": None, "url": ""}]  # Adjust keys to match column names
        spaced_data = []

        # Insert a blank row after every 10 products
        for i in range(0, len(df), 10):
            spaced_data.extend(df.iloc[i:i+10].to_dict('records'))  # Add 10 products
            spaced_data.extend(spacing_rows)  # Add a blank row

        # Convert spaced data back to DataFrame
        spaced_df = pd.DataFrame(spaced_data)

        # Save to CSV
        spaced_df.to_csv('ebay_data.csv', index=False)

          
scraper = EbayScraper()
keywords = scraper.import_data()
products = scraper.scrape_Ebay(keywords)
scraper.save_to_csv(products)

