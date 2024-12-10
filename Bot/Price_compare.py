import pandas as pd
import math

class Compare_price():
    def __init__(self):
        self.ebay_fee = 0.15
        self.paypal_fee = 0.029
        self.shipping = 15
        self.percentage = 100
        
    def import_ebay_data(self):
        # Load the CSV file with eBay data
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title', 'price'])
        # Convert the price column to float for numerical calculations
        df['price'] = df['price'].astype(float)
        # Extract the title and price as a list of tuples (title, price)
        #keywords = df[df['title', 'price'] != 'NaN'].values.tolist()
        Ebay_items = df[df['title'].notna() & df['price'].notna()].values.tolist()
        return Ebay_items
    
    def import_FB_data(self):
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title','price']) 
        FB_items = df[df['title'].notna() & df['price'].notna()].values.tolist()
        return  FB_items 
          
    def calculate_average_ebay_price(self, keywords):
        # Only process the first 10 items
        #items = [keyword[1] for keyword in keywords[:10]]  # Get prices for the first 10 items
        items = []
        Ebay_average_prices_list = []
        for Ebay_item in keywords:
            items.append(Ebay_item[1])
            if len(items) == 10:
                average_price = sum(items) / len(items)  # Calculate average price
                Ebay_average_prices_list.append(average_price)
                items = []
        return Ebay_average_prices_list
        
        
    def caculate_cost(self,FB_items):
            FB_items_cost_list = []
            for FB_item in FB_items:
                Total_Fees =  FB_item[1] * self.ebay_fee + FB_item[1] * self.paypal_fee
                cost = FB_item[1] + Total_Fees
                FB_items_cost_list.append(cost)
            return FB_items_cost_list
    
    def calculate_margin(self, FB_items_cost_list, Ebay_average_prices_list,FB_items):
        item_margin_list = []
        for Total_cost, Ebay_price,FB_item in zip(FB_items_cost_list, Ebay_average_prices_list,FB_items):
            FB_cost = FB_item[1]
            if Total_cost > 0 and not math.isnan(FB_cost):
                profit = Ebay_price - Total_cost
                margin = (profit / FB_cost) * self.percentage 
                item_margin_list.append(margin)
                print(f"Profit Margins:, {margin}%")  
            else:
                item_margin_list.append(0)
        
        return item_margin_list
    
Price = Compare_price()
Ebay_items = Price.import_ebay_data()
average_ebay_price = Price.calculate_average_ebay_price(Ebay_items)
fb_items = Price.import_FB_data()
cost = Price.caculate_cost(fb_items)
margin = Price.calculate_margin(cost,average_ebay_price,fb_items)


#Price.caculate_averge_ebay_price(Ebay_items)
