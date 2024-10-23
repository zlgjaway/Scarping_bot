from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

# Set up your driver (this example uses Chrome)
driver = webdriver.Firefox()
#""D:\WEB-Scraping Project\chromedriver-win64\chromedriver.exe""

# Open Facebook login page
driver.get("https://www.facebook.com/login")

# Enter your credentials (consider using environment variables or a config file to store these)
email = "nevav55008@ibtrades.com"
password = "Rog#252005"

email_input = driver.find_element(By.ID ,"email")

password_input = driver.find_element(By.ID ,"pass")


email_input.send_keys(email)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

time.sleep(5)  # Wait for the page to load

# After logging in, go to the Facebook Marketplace

driver.get("https://www.facebook.com/marketplace/")
time.sleep(5)  # Wait for the page to load



items = driver.find_elements(By.XPATH, "//a[@role='link' and contains(@href, '/marketplace/item')]")

for item in items:
    try:

        # Scrape the item name
        name = item.find_element(By.XPATH, ".//span[contains(@style, '-webkit-line-clamp')]").text
        # Scrape the price
        price = item.find_element(By.XPATH, ".//span[contains(text(), 'AU$')]").text
        # Scrape location (optional)
        location = item.find_element(By.XPATH, ".//span[contains(text(), 'Adelaide')]").text
        #break for 5 seconds
        driver.implicitly_wait(5)
        
    except exception as e :
        print("there an error ocurre")
        

# Close the WebDriver
driver.quit()