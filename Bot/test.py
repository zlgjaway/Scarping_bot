import pandas as pd

class Compare_price():
    def __init__(self):
        self.fee = 15
        self.shipping = 15
    
    def import_data(self):
        # Load the CSV file with eBay data
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title', 'price'])
        # Convert the price column to float for numerical calculations
        df['price'] = df['price'].astype(float)
        # Extract the title and price as a list of tuples (title, price)
        keywords = df[['title', 'price']].values.tolist()
        return keywords

    def calculate_average_ebay_price(self, keywords):
        # Only process the first 10 items
        #items = [keyword[1] for keyword in keywords[:10]]  # Get prices for the first 10 items
        items = []
        items_list = []
        for keyword in keywords:
            if keyword :
                skip
            items.append(keyword[1])
            if len(items) == 10:
                print(items)
                average_price = sum(items) / len(items)  # Calculate average price
                items_list.append(average_price)
                items = []


   
""" 
    def caculate_margin(self,):
        Facebook_items = EbayScraper.import_data()
        print("hello")

    def import_ebay_data(self):
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title','price']) 
        filtered_df  = df[(df['price'] >= self.min_price) & (df['price'] <= self.max_price)]
        Ebay_items =  filtered_df['title'].tolist()
        print(Ebay_items)
        return  Ebay_items 
"""
Price = Compare_price()
Ebay_items = Price.import_data()
Price.calculate_average_ebay_price(Ebay_items)
#Price.caculate_averge_ebay_price(Ebay_items)
