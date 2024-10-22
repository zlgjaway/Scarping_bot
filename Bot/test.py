from bs4 import BeautifulSoup
import requests
 
url = "https://www.scrapethissite.com/pages/forms/"
page_source = requests.get(url)
# Fetch the page source


# Parse it using BeautifulSoup
soup = BeautifulSoup(page_source.text, 'html.parser')
print(soup.prettify())