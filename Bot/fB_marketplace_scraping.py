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

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            print(f"There was an error: {e}")

        soup = BeautifulSoup(''.join(all_html_content), 'html.parser')
        self.driver.quit()

        products = [product for product in soup.find_all("a") if self.city.lower() in product.text.lower()]
        return products

    def process_data(self, products):
        extract_data = []
        for product in products:
            text = "\n".join(product.stripped_strings)
            url = product.get("href", "")
            lines = text.split("\n")
            title = lines[-2].split(",")[0] if len(lines) > 1 else ""
            location = lines[-1] if len(lines) > 1 else ""
            price_match = re.search(r"\d[\d,.]*", text)
            price = float(price_match.group().replace(",", "")) if price_match else None

            extract_data.append({
                "title": title,
                "price": price,
                "location": location,
                "url": re.sub(r"\?.*", "", url)
            })

        return extract_data

    def save_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv('facebook_marketplace_data.csv', index=False)
        print(df)



scraper = FBMarketplaceScraper()
scraper.login()
products = scraper.scrape_marketplace()
data = scraper.process_data(products)
scraper.save_to_csv(data)
