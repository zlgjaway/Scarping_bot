from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



import time
email = "long252005@gmail.com"
password = "Rog#252005"
driver = webdriver.Chrome()
#driver = uc.Chrome()
df_title = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title'])


driver.get("https://www.ebay.com.au/")
driver.find_element(By.ID, "gh-ac").send_keys(df_title)
time.sleep(5)

