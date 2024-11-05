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

class EbayScrapper:
    def __init__(self):
        self.email = "long252005@gmail.com"
        self.password = "Rog#252005"
        self.driver =  webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://signin.ebay.com.au/ws/eBayISAPI.dll?SignIn&sgfl=gh&ru=https%3A%2F%2Fwww.ebay.com.au%2F")
        #bot detection
        #if self.driver.find_element(By.XPATH, "//label[@for='userid']"):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='userid']"))).send_keys("question_boi")      
        WebDriverWait(self.driver, 5).until((By.ID, "userid").send_keys(self.email))
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        time.sleep(5)
#id="recaptcha-anchor-label">

scrapper =  EbayScrapper()
scrapper.login()