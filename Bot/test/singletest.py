import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

# Change this to any multi-item listing URL
LISTING_URL = "https://www.facebook.com/marketplace/item/1896511417803617/"
email = os.getenv("facebook_email")
password = os.getenv("facebook_pass")
# Setup Chrome
driver = webdriver.Chrome()
driver.get("https://www.facebook.com/login")
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "pass").send_keys(password)
driver.find_element(By.ID, "pass").submit()
input("Type 'ok' in the terminal and press Enter when you are ready to continue...")
#time.sleep(5)  # Wait for login
driver.get(LISTING_URL)
time.sleep(5)

# Try to expand full description
try:
    see_more_btn = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="See more"]')
    see_more_btn.click()
    time.sleep(3)
    print("Clicked 'See more'")
except:
    print("No 'See more' button")

# Grab all description elements
desc_elems = driver.find_elements(By.XPATH, '//span[contains(@class, "x193iq5w xeuugli")]')

description_lines = []
for elem in desc_elems:
    #outer_html = elem.get_attribute("outerHTML")
    #outer_html = elem.get_attribute("outerHTML")
    text = elem.text.lower()
    if 'location is approximate' in text: #problem withe over scrape or could use if detected location is approximate to break
        print("Reached static map, stopping.")
        break
    description_lines.append(elem.text.lower())

full_description = "\n".join(description_lines)

driver.quit()

print("=== FULL DESCRIPTION ===")
print(full_description)
print("========================\n")

# Clean up and apply regex
pattern = re.compile(
    r"""^(?P<title>.+?)            # Title: anything up to price
        \s*[\$:]*\s*               # Optional $, :, whitespace
        (?P<price>\d+(?:\.\d{1,2})?) # Price
        (?!\S)                     # No extra characters
    """, re.VERBOSE | re.IGNORECASE
)

print("Detected items:")

for line in full_description.split("\n"):
    line = line.strip()
    if not line or any(w in line.lower() for w in ["sold", "firm", "hold", "pending"]):
        continue

    match = pattern.match(line)
    if match:
        title = match.group("title").strip()
        price = float(match.group("price"))
        print(f"✅ Title: {title}, Price: ${price}")
    else:
        print(f"❌ Skipped: {line}")
