import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
import pandas as pd
import time

class FBMarketplaceScraper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("facebook_email")
        self.password = os.getenv("facebook_pass")
        self.city = "adelaide"
        self.base_url = "https://www.facebook.com/marketplace/category/video-games-consoles" #scrape video-games-consoles
        self.days_listed = 7
        self.driver = webdriver.Chrome()
        self.multi_items_listing = [
        "games", "pack", "bundle", "items", "set", "collection", "lot", 
        "combo", "assorted", "variety", "multiple", "bulk", "series", 
        "edition", "mix", "group", "assortment"
        ]
        self.multi_item_description = "$"


    def login(self):
        self.driver.get("https://www.facebook.com/login")
        self.driver.find_element(By.ID, "email").send_keys(self.email)
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        self.driver.find_element(By.ID, "pass").submit()
        time.sleep(5)  # Wait for login

    def scrape_marketplace(self):
        url = f"{self.base_url}"
        self.driver.get(url)
        time.sleep(5)

        all_html_content = []
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)  # Wait for new items to load

                all_product_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[role='link']")
                all_html_content.extend([elem.get_attribute('outerHTML') for elem in all_product_elements])
                # adding condition detect multi-item list 
                #try to sperate multi_item listing in differnt list
                #loop the list to extract data of the list 
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            print(f"There was an error: {e}")
        soup = BeautifulSoup(''.join(all_html_content), 'html.parser')
        self.driver.quit()

        single_products = []
        multi_products = []
        
        for product in soup.find_all("a"):
            description = product.text.lower()
            if self.city.lower() in description:
                if any(keyword in description for keyword in self.multi_items_listing):
                #if any(keyword in description for keyword in self.multi_items_listing):
                    multi_products.append(product)  # Multi-item listing
                else:
                    single_products.append(product)  # Single-item listing

        return single_products, multi_products
    def process_single_list_data(self, single_products):
        extract_single_list_data = []
        for product in single_products:
            text = "\n".join(product.stripped_strings)
            url = product.get("href", "")
            lines = text.split("\n")
            title = lines[-2].split(",")[0] if len(lines) > 1 else ""
            location = lines[-1] if len(lines) > 1 else ""
            price_match = re.search(r"\d[\d,.]*", text)
            price = float(price_match.group().replace(",", "")) if price_match else None

            extract_single_list_data.append({
                "title": title,
                "price": price,
                "location": location,
                "url": re.sub(r"\?.*", "", url)
            })
        return extract_single_list_data

    def process_multi_list_data(self,multi_products):
        all_html_multi_content = []
        extract_multi_list_data_1 = []
        for product in multi_products:
            url =  re.sub(r"\?.*", "", url)
            self.driver.get(f"https://www.facebook.com/{url}")
            multi_product_elements = self.driver.find_elements(By.XPATH, "//*[contains(@id, 'mount_0_0_')]/div/div[1]/div/div[3]//div[2]/div/div[2]")
            description = " ".join([elem.text for elem in multi_product_elements]).lower()
            if description.count(self.multi_item_description) >= 2:
                #if price in discrtion all_html_content
                all_html_multi_content.extend([elem.get_attribute('outerHTML') for elem in multi_product_elements])
                soup = BeautifulSoup(''.join(all_html_multi_content), 'html.parser')
                for product in soup:
                    text = "\n".join(product.stripped_strings)
                    url = product.get("href", "")
                    lines = text.split("\n")
                    title = lines[-2].split(",")[0] if len(lines) > 1 else ""
                    location = lines[-1] if len(lines) > 1 else ""
                    price_match = re.search(r"\d[\d,.]*", text)
                    price = float(price_match.group().replace(",", "")) if price_match else None

                    extract_multi_list_data_1.append({
                        "title": title,
                        "price": price,
                        "location": location,
                        "url": re.sub(r"\?.*", "", url)# only 1 url in 1 list
                    })
                    #if no price in discrtion append data
            else:
                text = "\n".join(product.stripped_strings)
                url = product.get("href", "")
                lines = text.split("\n")
                title = lines[-2].split(",")[0] if len(lines) > 1 else ""
                location = lines[-1] if len(lines) > 1 else ""
                price_match = re.search(r"\d[\d,.]*", text)
                price = float(price_match.group().replace(",", "")) if price_match else None

                extract_multi_list_data_1.append({
                    "title": title,
                    "price": price,
                    "location": location,
                    "url": re.sub(r"\?.*", "", url)
                })
        return extract_multi_list_data_1 
            

    def save_to_csv(self, data_1 , data_2 ):
        df = pd.concat([pd.DataFrame(data_1), pd.DataFrame(data_2)], ignore_index=True)
        df.to_csv('facebook_marketplace_data.csv', index=False)
        print(df)



scraper = FBMarketplaceScraper()
scraper.login()
single_products, multi_products = scraper.scrape_marketplace()
data_1 = scraper.process_single_list_data(single_products)
data_2 = scraper.process_multi_list_data(multi_products)
scraper.save_to_csv(data_1,data_2)
