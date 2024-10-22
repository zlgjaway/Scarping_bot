import pandas as pd
from Scraping import soup, items

# Assuming you have a list of product data
products = []

# Add items to your list
for item in items:
    title = item.find('span', class_='something-title-class').text
    price = item.find('span', class_='something-price-class').text
    products.append({'Title': title, 'Price': price})

# Convert the list to a DataFrame and save it as a CSV file
df = pd.DataFrame(products)
df.to_csv('facebook_marketplace_data.csv', index=False)
