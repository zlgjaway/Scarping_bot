from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re
import pandas as pd
import time

# Set up your driver (this example uses Chrome)
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)
#""D:\WEB-Scraping Project\chromedriver-win64\chromedriver.exe""



# Open Facebook login page
driver.get("https://www.facebook.com/login")

# Enter your credentials (consider using environment variables or a config file to store these)
email = "nevav55008@ibtrades.com"
password = "Rog#252005"
city = "adelaide"

email_input = driver.find_element(By.ID ,"email")

password_input = driver.find_element(By.ID ,"pass")


email_input.send_keys(email)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

time.sleep(5)  # Wait for the page to load

# After logging in, go to the Facebook Marketplace

driver.get("https://www.facebook.com/marketplace/?ref=app_tab")

time.sleep(5)  # Wait for the page to load
max_retries = 5
attempt = 0
wait = WebDriverWait(driver, 10)
try:
# Scroll to load more items
    last_height = driver.execute_script("return document.body.scrollHeight")
    while attempt < max_retries:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


            time.sleep(5)  # Wait for new items to load

            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')

            #scrap_products =  driver.find_elements(By.CSS_SELECTOR, "a[role='link']")
            scrap_products = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_fy"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[3]/div/div[1]/div/div/div/span/div/div/div/div[2]/div[1]/div/div/span/div/div/div/div/a')))

            # scrap_products = soup.find_all("a")

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # Break the loop if no new content is loaded
                break
            last_height = new_height
        except (WebDriverException, NoSuchElementException) as e:
            if driver:
                driver.quit()  # Quit the driver if it was initialized
            print(f"\nScrapper stopped due to: {e}, launching again in 4 seconds...")
            time.sleep(4)
            attempt += 1
except Exception as e:
    print(f"There was an error: {e}")


#page_source = driver.page_source

#soup = BeautifulSoup(page_source, 'html.parser')

products = [scrap_product for scrap_product in scrap_products if city.lower() in scrap_product.text.lower()]

# Assuming you have a list of product data
products_data = []

# Add items to your list
for product in products:
    url = product.get('href')
    text = "\n".join(product.stripped_strings)
    products_data.append({"text": text, "url": url})

print(soup.prettify())

# Convert the list to a DataFrame and save it as a CSV file

extract_data = []

for item in products_data:
    lines = item["text"].split("\n")
    numeric_pattern = re.compile(r"\d[\d,.]*")
    price = None 
    title = ""
    location = ""

    for line in lines:
        match = numeric_pattern.search(line)

        if match:
            price_str = match.group()
            price = float(price_str.replace(",",""))
            break
    if price is not None:
        print(f"Price extracted: {price}")
    else:
        print("Price not found")
    
    if len(lines) > 1:
        title = lines[-2]
        location = lines[-1]

    extract_data.append({
        "title" : title,
        "price" : price,
        "location": location,
        "url": re.sub(r"\?.*", "", item["url"]) if item["url"] else ""

    })
print(extract_data)
df = pd.DataFrame(extract_data)
df.to_csv('facebook_marketplace_data.csv', index=False)

df_1 = pd.DataFrame(products_data)
df_1.to_csv('facebook_marketplace_data_2.csv', index=False)

