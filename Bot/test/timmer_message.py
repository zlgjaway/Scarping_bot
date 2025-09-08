import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
import time
import joblib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import datetime
import pytz  # pip install pytz


class FBMarketplaceScraper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("facebook_email_2")
        self.password = os.getenv("facebook_pass_2")
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

    def message(self):
        adelaide_tz  = pytz.timezone("Australia/Adelaide")
        today_adelaide = datetime.datetime.now(adelaide_tz).date()

        target_time = adelaide_tz.localize(datetime.datetime(today_adelaide.year, today_adelaide.month, today_adelaide.day, 9, 40))
        #target_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
        self.driver.get("https://www.facebook.com/messages/t/752144137725139")
        input("Type 'ok' in the terminal and press Enter when you are ready to continue...")
        while datetime.datetime.now(adelaide_tz) < target_time:
            time.sleep(30)  # check every 30 seconds
        wait = WebDriverWait(self.driver, 15)
        message_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="textbox"][contenteditable="true"]'))
        )
        message_box.send_keys("Hey, I haven’t heard back from you — are you still interested?")
        message_box.send_keys(Keys.ENTER)

        #message_box.send_keys(Keys.ENTER)
        #input("Type 'ok' in the terminal and press Enter when you are ready to continue...")
        self.driver.quit()
scraper = FBMarketplaceScraper()
scraper.login() 
scraper.message()