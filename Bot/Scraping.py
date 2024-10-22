from bs4 import BeautifulSoup
from Login import driver

# Fetch the page source
page_source = driver.page_source

# Parse it using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

print(soup.prettify())
items = soup.find_all('div', class_='something-item-class')  # Update with actual class name

for item in items:
    title = item.find('span', class_='something-title-class').text  # Adjust this for the correct tag
    print(title)