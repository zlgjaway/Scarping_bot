import pandas as pd
#from ebay_scraping import EbayScraper
class Compare_price():
    def __init__(self):
        self.fee = 15
        self.shipping = 15
    
    def import_Ebay_data (self):
         #/home/zlgjaway/Documents/ScarpingBot_project/facebook_marketplace_data.csv
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title','price'])
        filtered_df  = df[(df['price'])]
        Ebay_items =  filtered_df['title'].tolist()
        print(Ebay_items)
        return  Ebay_items

    def caculate_averge_ebay_price(self,Ebay_items):
        for Ebay_item in Ebay_items:
            print(Ebay_item)
        
    
    
   
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
Ebay_items = Price.import_Ebay_data()
Price.caculate_averge_ebay_price(Ebay_items)