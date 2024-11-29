import pandas as pd

class ComparePrice:
    def __init__(self):
        self.ebay_fee = 0.15
        self.paypal_fee = 0.029
        self.shipping = 15
        self.percentage = 100

    def import_ebay_data(self):
        df = pd.read_csv('ebay_data.csv', sep=',', usecols=['title', 'price'])
        df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to float, handling errors
        Ebay_items = df[df['title'].notna() & df['price'].notna()].values.tolist()
        return Ebay_items

    def import_FB_data(self):
        df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title', 'price'])
        df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to float
        FB_items = df[df['title'].notna() & df['price'].notna()].values.tolist()
        return FB_items

    def calculate_average_ebay_price(self, ebay_items):
        average_prices = []
        current_prices = []

        for item in ebay_items:
            current_prices.append(item[1])
            if len(current_prices) == 10:
                average_prices.append(sum(current_prices) / 10)
                current_prices = []

        # Handle remaining items if not a multiple of 10
        if current_prices:
            average_prices.append(sum(current_prices) / len(current_prices))

        return average_prices

    def calculate_cost(self, fb_items):
        fb_items_cost_list = []
        for fb_item in fb_items:
            total_fees = fb_item[1] * self.ebay_fee + fb_item[1] * self.paypal_fee + self.shipping
            cost = fb_item[1] + total_fees
            fb_items_cost_list.append(cost)
        return fb_items_cost_list

    def calculate_margin(self, fb_items_cost_list, ebay_avg_prices, fb_items):
        item_margin_list = []
        for i, fb_item_cost in enumerate(fb_items_cost_list):
            # Use the corresponding average price from eBay
            ebay_price = ebay_avg_prices[i] if i < len(ebay_avg_prices) else 0
            if ebay_price > 0:
                profit = ebay_price - fb_item_cost
                margin = (profit / fb_items[i][1]) * self.percentage
                item_margin_list.append(margin)
        return item_margin_list

# Initialize and run
price_compare = ComparePrice()
ebay_items = price_compare.import_ebay_data()
fb_items = price_compare.import_FB_data()

average_ebay_prices = price_compare.calculate_average_ebay_price(ebay_items)
fb_item_costs = price_compare.calculate_cost(fb_items)
profit_margins = price_compare.calculate_margin(fb_item_costs, average_ebay_prices, fb_items)

# Output profit margins
print("Profit Margins:", profit_margins)


