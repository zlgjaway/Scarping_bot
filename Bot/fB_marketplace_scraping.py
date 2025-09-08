import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
import pandas as pd
import time
import joblib
class FBMarketplaceScraper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("facebook_email")
        self.password = os.getenv("facebook_pass")
        self.city = "adelaide"
        #self.base_url = "https://www.facebook.com/marketplace/adelaide/video-games-consoles/?exact=false" #scrape video-games-consoles
        #self.base_url = "https://www.facebook.com/marketplace/category/electronics" #scrape electronics
        self.base_url = "https://www.facebook.com/marketplace/?ref=app_tab"

        self.days_listed = 7
        self.driver = webdriver.Chrome()
        self.multi_items_listing = [
        "games", "pack", "bundle", "items", "set", "collection", "lot", 
        "combo", "assorted", "variety", "multiple", "bulk", "series", 
        "edition", "mix", "group", "assortment"
        ]
        self.hprice = 100
        self.lprice = 10
        self.multi_item_description = "$"
        self.model = joblib.load("D:\WEB-Scraping Project\junk_filter_model.pkl") 


    def login(self):
        self.driver.get("https://www.facebook.com/login")
        self.driver.find_element(By.ID, "email").send_keys(self.email)
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        #self.driver.find_element(By.ID, "pass").submit()self.model
        input("Type 'ok' in the terminal and press Enter when you are ready to continue...")
        #time.sleep(5)  # Wait for login

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
        #self.driver.quit()
        #print(f"Soup:{soup}")
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
        #print(f"single_products:{single_products}")
        #print(f"multi_products:{multi_products}")
        return single_products, multi_products
    
    def is_valid_listing(self,title, description):
        text = f"{title} {description}"
        return self.model.predict([text])[0] == 1  # 0 = valid
        
    def process_single_list_data(self, single_products):
        extract_single_list_data = []
        for product in single_products:
            text = "\n".join(product.stripped_strings)
            url = product.get("href", "")
            lines = text.split("\n")
            title = lines[-2].split(",")[0] if len(lines) > 1 else ""
            location = lines[-1] if len(lines) > 1 else ""
            price_match = re.search(r"A\$[\d,.]+", text)
            price = float(price_match.group().replace("A$", "").replace(",", "")) if price_match else None
            if (float(price or 0) <= self.hprice): # MAYBE WRONG WITH THE WHEN TALKE IN TITLE NOT THE DATA
                extract_single_list_data.append({
                    "type" : "Single-item listing",
                    "title": title,
                    "price": price,
                    "location": location,
                    "url": re.sub(r"\?.*", "", url)
                })
        return extract_single_list_data
    
    def process_multi_list_data(self, multi_products):
        extract_multi_list_data = []
        seen_items = set()   # Track (title, price) pairs

        for product in multi_products:
            text = "\n".join(product.stripped_strings)
            product_url = re.sub(r"\?.*", "", product.get("href", ""))
            lines = text.split("\n")
            title = lines[-2].split(",")[0] if len(lines) > 1 else ""
            location = lines[-1] if len(lines) > 1 else ""
            price_match = re.search(r"A\$[\d,.]+", text)
            price = float(price_match.group().replace("A$", "").replace(",", "")) if price_match else None
           

            print(f"Navigating to: https://www.facebook.com{product_url}")
            url = f"https://www.facebook.com{product_url}"
            self.driver.get(url)
            time.sleep(5)

            try:
                self.driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="See more"]').click()
                time.sleep(5)
                print("See more clicked")
            except:
                print("No 'See more' button")
                pass

            multi_product_elements = self.driver.find_elements(By.XPATH, '//span[contains(@class, "x193iq5w xeuugli")]')
            #description = "\n".join([elem.text for elem in multi_product_elements]).lower()
            
            description_lines = []
            for elem in multi_product_elements:
                text = elem.text.lower()
                if 'location is approximate' in text: #problem withe over scrape
                    print("Reached static map, stopping.")
                    break
                description_lines.append(elem.text.lower())

            description = "\n".join(description_lines)

            # Flexible regex pattern for title + price lines
            pattern = re.compile(
                r"""^(?P<title>[^\d$]+?)          # Title: anything before numbers/$
                    \s*                           # Optional space
                    \$?(?P<price>\d+(?:\.\d{1,2})?) # Price: number, maybe with $
                    (?!\S)                         # No extra non-space characters after
                """, re.VERBOSE | re.IGNORECASE
            )
            valid_lines = [line for line in description.split("\n")
                       if pattern.match(line.strip())
                       and not any(w in line.lower() for w in ["sold", "firm", "hold", "pending"])]
            # Detect if it’s a multi-item listing
            if len(valid_lines) >= 3:
                for line in description.split("\n"):
                    line = line.strip()
                    #match = re.match(pattern, line)
                    match = pattern.match(line) #problem the item  in the list is not append just the title singletest is work 
                    #change 
                    if match:
                        #matches.append(match)
                        title_multi = match.group("title").strip()
                        price_multi = float(match.group("price"))
                        key = (title_multi.lower(), price_multi)
                        if key in seen_items:
                            continue  # Skip duplicates
                        seen_items.add(key)
                        if price_multi <= self.hprice and price_multi >= self.lprice and len(title_multi)>3 : #and self.is_valid_listing(title_multi, line): #work but over filter with list with short name 
                            extract_multi_list_data.append({
                                    "type" : "Multi-item listing",
                                    "title": title_multi, 
                                    "price": price_multi,
                                    "location": location,
                                    "url": product_url
                            })
            else:
                key = (title.lower(), price or 0)
                if key in seen_items:
                    continue  # Skip duplicates
                seen_items.add(key)
                if (float(price or 0) <= self.hprice): # MAYBE WRONG WITH THE WHEN TALKE IN TITLE NOT THE DATA
                    extract_multi_list_data.append({
                        "type" : "Single-item listing",
                        "title": title,
                        "price": price,
                        "location": location,
                        "url": product_url
                    })
                         

        self.driver.quit()
        return extract_multi_list_data

    def save_to_csv(self, data_1 , data_2 ): 
        df = pd.concat([pd.DataFrame(data_1), pd.DataFrame(data_2)], ignore_index=True)
        df.to_csv('facebook_marketplace_data.csv', index=False)
  


scraper = FBMarketplaceScraper()
scraper.login() 
single_products, multi_products = scraper.scrape_marketplace()
data_1 = scraper.process_single_list_data(single_products)
data_2 = scraper.process_multi_list_data(multi_products)
scraper.save_to_csv(data_1,data_2)

