#1. Analyze Descriptions for Multi-item Listings
"""
import re

def parse_description(description):
    items = []
    # Regular expression to extract item and price
    pattern = r"([\w\s]+):?\s*\$([\d.]+)"
    matches = re.findall(pattern, description)
    for match in matches:
        item_name = match[0].strip()
        item_price = float(match[1])
        items.append({"name": item_name, "price": item_price})
    return items

# Example description
description = 
Game 1: $10
Game 2 - $15
Controller - $20


parsed_items = parse_description(description)
print(parsed_items)
# Output: [{'name': 'Game 1', 'price': 10.0}, {'name': 'Game 2', 'price': 15.0}, {'name': 'Controller', 'price': 20.0}]
"""
