import json
import os
from datetime import datetime
def load_menu():
    with open('menu.json', 'r') as f:
        return json.load(f)


def update_current_order(order_items):
    menu = load_menu()
    current_order = {
        "items": [],
        "total_price": 0
    }
    
    for item in order_items:
        item_name = item["name"]
        item_size = item["size"]
        item_quantity = item["quantity"]
        
        # Find item in the menu
        for category in menu["menu"]["categories"]:
            for menu_item in category["items"]:
                if menu_item["name"].lower() == item_name.lower():
                    # Match the size
                    for size in menu_item["sizes"]:
                        if size["name"].lower() == item_size.lower():
                            price = size["price"]
                            break
                    else:
                        # If size doesn't exist, use the first one
                        price = menu_item["sizes"][0]["price"]
                        item_size = menu_item["sizes"][0]["name"]
                    
                    # Calculate total for this item
                    item_total = price * item_quantity
                    
                    # Add to current order
                    current_order["items"].append({
                        "name": menu_item["name"],
                        "category": category["name"],
                        "size": item_size,
                        "quantity": item_quantity,
                        "price_per_item": price,
                        "item_total": item_total
                    })
                    
                    current_order["total_price"] += item_total
                    break
            else:
                continue
            break
    
    return json.dumps(current_order, indent=2)