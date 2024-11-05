from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

class EbayScrapper:
    def __init__(self):
        self.email = "long252005@gmail.com"
        self.password = "Rog#long252005"
        self.driver = webdriver.Firefox()

    def login(self):
        self.driver.get("https://signin.ebay.com.au/ws/eBayISAPI.dll?SignIn&sgfl=gh&ru=https%3A%2F%2Fwww.ebay.com.au%2F")
        self.driver.find_element(By.ID, "userid").send_keys(self.email)
        self.driver.find_element(By.ID, "")
