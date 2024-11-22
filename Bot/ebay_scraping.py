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
class EbayScraper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("ebay_email")
        self.password = os.getenv("ebay_pass")
        self.driver = webdriver.Chrome()
        self.min_price = 10
        self.max_price = 200
    
    def login(self):
        self.driver.get("https://signin.ebay.com.au/ws/eBayISAPI.dll?SignIn&sgfl=gh&ru=https%3A%2F%2Fwww.ebay.com.au%2F")
        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='userid']")))
        except Exception as e:
            print(f"There are an error: {e}")
        self.driver.find_element(By.ID, "userid").send_keys(self.email)
        #signin-continue-btn
        self.driver.find_element(By.ID, "signin-continue-btn").submit()
        #time.sleep(5)
        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='pass']")))
        except Exception as e:
            print(f"There are an error: {e}")
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        #sgnBt
        self.driver.find_element(By.ID, "sgnBt").submit()
        time.sleep(5)
    def import_data (self):
         #/home/zlgjaway/Documents/ScarpingBot_project/facebook_marketplace_data.csv
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords =  filtered_df['title'].tolist()
        print(keywords)
        return  keywords 
    
    def scrape_Ebay(self, keywords):
        all_product_elements = []
        Button_click = 0
        for keyword in keywords:
            # Find and clear the search input field, then enter the keyword
            search_input = self.driver.find_element(By.ID, "gh-ac")
            search_input.clear()
            search_input.send_keys(keyword)

            # Click the search button id="gh-btn"
            self.driver.find_element(By.ID, "gh-btn").click()
            time.sleep(5)  # Wait for results to load

            # Scroll to filter option and click on it
            if Button_click < 1:
                element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@name='LH_Sold']//a[contains(@href, 'LH_Sold=1')]"))#check if element exists but you only need to click once 
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element) # scroll to view element
                element.click()
                Button_click = Button_click +1
                time.sleep(5)  # Wait for page to refresh after filtering

            #// xpath = *[@id="item473776eb82"] ; css selector =#item3bbd688738 //*[@id="item3bbd688738"]
            items = self.driver.find_elements(By.CSS_SELECTOR, "li.s-item")
            
            # Extract and store the outerHTML of each item
            for item in  items[2:12]:  # Get outerHTML of up to 10 items
                all_product_elements.append(item.get_attribute('outerHTML'))
        # Use BeautifulSoup on the joined HTML content 
        soup = BeautifulSoup(''.join(all_product_elements), 'html.parser')
        self.driver.quit()

        products = [product for product in soup.find_all('li', class_='s-item')]
        
        return products
    
    def process_data(self, products):
        extract_data = []
        for product in products:
            # Extract text
            text = "\n".join(product.stripped_strings)
            # Extract URL
            link_tag = product.find('a', href=True)
            url = link_tag['href'] if link_tag else ''
            # Extract title
            title_tag = product.find('span', {'role': 'heading'})
            title = title_tag.text.strip() if title_tag else 'N/A'
            # Extract price
            price_match = re.search(r"\$\d[\d,.]*", text)
            price = float(price_match.group().replace("$", "").replace(",", "")) if price_match else None

            # Append extracted data
            extract_data.append({
                "title": title,
                "price": price,
                "url": url,
            })
        return extract_data
    
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
scraper.login()
keywords = scraper.import_data()
products = scraper.scrape_Ebay(keywords)
extract_data = scraper.process_data(products)
scraper.save_to_csv(extract_data)

