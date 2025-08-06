import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

class scrape_for_5070ti:
    def __init__(self):
       self.url = "https://www.pccasegear.com/products/68122/gigabyte-geforce-rtx-5070-ti-windforce-oc-gddr7-16gb"  # asus prime 5070ti
       #self.url = "https://www.pccasegear.com/products/65470/asus-geforce-rtx-4070-super-dual-evo-oc-12gb"
       self.email = "tanhatlong252005@gmail.com"
       self.password = "Rog#long252005"
       self.driver = webdriver.Chrome()
       self.name = "Long Ta"
       #self.address = "Unit 2/60 Chief St" 
       self.card_number = "5163 6100 8883 2454"
       self.vaid = "09 / 28"
       self.cvv = "433"
    
    def login(self):
        self.driver.get("https://www.pccasegear.com/login")
        self.driver.find_element(By.ID, "login-email-address").send_keys(self.email)
        self.driver.find_element(By.ID, "login-password").send_keys(self.password)
        input("Type 'ok' in the terminal and press Enter when you are ready to continue...")
        self.driver.find_element(By.ID, "loginBtn").submit()


    def wait_for_product_to_be_available(self):
        while True:
            # Check if the button is disabled or "Sold Out"
            try:
                self.driver.find_element(By.XPATH, "//button[@class='add-to-cart pointer sold-out-btn-bg' and @disabled]")
                
                # If the button is found and disabled, refresh the page
                print("Product is sold out. Refreshing the page...")
                self.driver.refresh()  # Refresh the page to check availability again
                
                # Wait for a few seconds before checking again
                time.sleep(2)  # Adjust the sleep time as needed
                
            except Exception as e:
                # If the button is not found (not sold out), break out of the loop
                print("Product is available, proceeding with checkout.")
                break
    
    def get_order(self):
        self.driver.get(self.url)
        self.wait_for_product_to_be_available()
        self.driver.find_element(By.XPATH, "//*[@id='main']/div[2]/div[2]/div[7]/form/div[1]/div[2]/button").click()
        time.sleep(1)
        #self.driver.find_element(By.CLASS_NAME, "btn checkout-btn-bg").click()
        #btn blue_btn
    def make_payment(self):
        self.driver.get("https://www.pccasegear.com/secure_checkout")
        
        self.driver.find_element(By.ID, "i-agree").click()
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the field to be visible before sending keys
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "zzzxy-name"))).send_keys(self.name)

        card_iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@name, 'braintree-hosted-field-number')]"))
        )
        self.driver.switch_to.frame(card_iframe)  

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "input"))
        ).send_keys(self.card_number)
        self.driver.switch_to.default_content()  # Exit the iframe



        expiry_iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='braintree-hosted-field-expirationDate']"))
        )
        self.driver.switch_to.frame(expiry_iframe) 

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "input"))
        ).send_keys(self.vaid)
        self.driver.switch_to.default_content()  # Exit the iframe


        cvv_iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='braintree-hosted-field-cvv']"))
        )
        self.driver.switch_to.frame(cvv_iframe) 

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "input"))
        ).send_keys(self.cvv)
        self.driver.switch_to.default_content()

        input("Type 'ok' in the terminal and press Enter when you are ready to continue...")


scrape = scrape_for_5070ti()
scrape.login()

# Set the target time for the card release (adjust the date and time as needed)
release_time = datetime(2025, 2, 21, 0, 30, 0)  # February 21st, 2025, 12:30 AM ACDT (Adelaide)


# Get the current time
current_time = datetime.now()

# Calculate the time difference
time_diff = release_time - current_time

# If the target time is in the future, wait until it's time
if time_diff.total_seconds() > 0:
    print(f"Waiting until {release_time} to make the order...")
    time.sleep(time_diff.total_seconds())  # Wait for the time difference

# After the wait, proceed with the payment code

        

scrape.get_order()
scrape.make_payment()