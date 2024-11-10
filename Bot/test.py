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
        #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='userid']"))).send_keys("")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='userid']")))
        #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "userid")))
        self.driver.find_element(By.ID, "userid").send_keys(self.email)
        #self.driver.find_element(By.ID, "signin-continue-btn").click()
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        self.driver.find_element(By.ID, "sgnBt").click()
        time.sleep(5)
#id="recaptcha-anchor-l

scrapper =  EbayScrapper()
scrapper.login()
#id="recaptcha-anchor-label">
"""
//*[@id="signin-form"]/div/div[1]/div/div[1]/div/div[1]
"""