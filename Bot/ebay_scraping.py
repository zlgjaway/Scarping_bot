from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

class EbayScrapper:
    def __init__(self):
        self.email = "long252005@gmail.com"
        self.password = "Rog#252005"
        self.driver =  webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://signin.ebay.com.au/ws/eBayISAPI.dll?SignIn&sgfl=gh&ru=https%3A%2F%2Fwww.ebay.com.au%2F")
        #bot detection
        #if self.driver.find_element(By.XPATH, "//label[@for='userid']"):
        
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-submit button"))).click()
        WebDriverWait(self.driver,5).until(EC.find_element((By.ID,"userid"))).send_keys(self.email)
        WebDriverWait(self.driver,5).until(EC.find_element((By.ID,"pass"))).send_keys(self.password)
        time.sleep(5)
#id="recaptcha-anchor-label">

    def extract_data(self):
        #/home/zlgjaway/Documents/ScarpingBot_project/facebook_marketplace_data.csv
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords =  filtered_df['title'].tolist()
        return  keywords 

    def scrape_ebay(self,keywords):
        for item in keywords:
            self.driver.find_element(By.ID,"gh-ac").send_key(item)
            self.driver.find_element(By.ID,"gh-btn").click()
            self.driver.find_element(By.ID,"icon-checkbox-unchecked-18").click()
            items = []
            #loop 10 prices tage for 1 item
            try:
                if  items <=  10:
                    all_product_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[role='link']")
                    items.extend([elem.get_attribute('outerHTML') for elem in all_product_elements])

            except Exception as e:
                print(f"there are an error: {e}")
            soup = BeautifulSoup(''.join(items), 'html.parser')
            potential_items = soup
            self.driver.quit()



scrapper =  EbayScrapper()
scrapper.login()