"""
import os
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
API_key =os.getenv("api_key")

class EbayScraper(object):
    def __init__(self, API_key):
        self.api_key = API_key
        self.max_price = 500
        self.min_price = 10
        self.limit_rate = 1

    def extract_csv(self):
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        keywords =  filtered_df['title'].tolist()
        return  keywords
    
    def request_item(self, keywords):
        call_rate = 0
        item_extract = []
        while call_rate <= self.limit_rate : 
            try:
                api  = finding(appid=self.api_key, config_file=None )
                for keyword in keywords:    
                    response = api.execute('findCompletedItems', {
                        'keywords': keyword,  
                        'sortOrder': 'EndTimeSoonest',    
                        'paginationInput': {
                        'entriesPerPage': 10,         
                        'pageNumber': 1
                        }
                    })
                    print (response)
            
                for item in response.reply.searchResult.item:
                    item_extract = item.currentPrice.value
                    return item_extract
            except ConnectionError as e:
                print(e.response.dict())
        call_rate +1
    def save_to_csv(self,data):
        df = pd.DataFrame(data)
        df.to_csv('ebay_data.csv', index=False)
        print(df)

scraper = EbayScraper(API_key)
keywords = scraper.extract_csv()  # Get all keywords
data = scraper.request_item(keywords)    # Pass all keywords at once
scraper.save_to_csv(data)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException

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
        
        #WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-submit button"))).click()
        #WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "userid")))

        #WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys(self.email)
        #self.driver.find_element(By.ID, "userid").send_keys(self.email)
        #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='userid']"))).send_keys(self.email)
        try:
    # Wait for the element to be clickable and attempt to interact
            #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "anchor-state")))
            self.driver.find_element(By.ID, "anchor-state")
            print("Element found")
            input("Please complete the reCAPTCHA and press Enter to continue...")
        except ElementNotInteractableException:
            print("Element is not interactable")
            self.driver.find_element(By.ID, "userid").send_keys(self.email)
            
        #self.driver.find_element(By.ID, "userid").send_keys(self.email)
        self.driver.find_element(By.ID, "signin-continue-btn").click()
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        self.driver.find_element(By.ID, "sgnBt").click()
        time.sleep(5)
#id="recaptcha-anchor-l

scrapper =  EbayScrapper()
scrapper.login()
#id="recaptcha-anchor-label">