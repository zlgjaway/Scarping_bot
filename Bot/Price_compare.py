import pandas as pd
import math

class Compare_price():
    def __init__(self):
        self.ebay_fee = 0.15
        self.paypal_fee = 0.029
        self.shipping = 9.70
        self.percentage = 100
        self.blacklist   = []
        
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
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title','price','url']) 
        df = df[~df['title'].str.lower().str.contains('|'.join(self.blacklist))] #self.blacklist
        """
        # Ensure title is a string and lowercase it
        df['title'] = df['title'].astype(str).str.lower()

        # Apply filters
        mask = ~df['title'].str.contains('|'.join(self.blacklist), na=False) #self.blacklist
        mask &= df['price'].notna()
        
        # Get final list
        FB_items = df[mask].values.tolist()
        """
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
                Total_Fees =  FB_item[1] * self.ebay_fee + FB_item[1] * self.paypal_fee + self.shipping
                cost = FB_item[1] + Total_Fees
                FB_items_cost_list.append(cost)
            return FB_items_cost_list
    
    def calculate_margin(self, FB_items_cost_list, Ebay_average_prices_list,FB_items):
        item_margin_list = []
        for Total_cost, Ebay_price,FB_item in zip(FB_items_cost_list, Ebay_average_prices_list,FB_items):
            FB_cost = FB_item[1]
            if Total_cost > 0 and not math.isnan(FB_cost):
                profit = Ebay_price - Total_cost
                margin = round((profit / FB_cost) * self.percentage,0)
                if 20 < margin < 500:
                    item_margin_list.append({
                            "title": FB_item[0],
                            "price": FB_item[1],
                            "url"  : FB_item[2],
                            "Profit Margins": margin
                        })#margin
                    print(f"Profit Margins:, {margin}%") 

                
        return item_margin_list
    
    def save_to_csv(self, item_margin_list): 
        df = pd.concat([pd.DataFrame(item_margin_list)], ignore_index=True)
        df.to_csv('Calculate_margin.csv', index=False)
    
    
Price = Compare_price()
Ebay_items = Price.import_ebay_data()
average_ebay_price = Price.calculate_average_ebay_price(Ebay_items)
fb_items = Price.import_FB_data()
cost = Price.caculate_cost(fb_items)
margin = Price.calculate_margin(cost,average_ebay_price,fb_items)
Price.save_to_csv(margin)

#Price.caculate_averge_ebay_price(Ebay_items)
