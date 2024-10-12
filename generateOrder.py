import json
import os
from datetime import datetime
def load_menu():
    with open('menu.json', 'r') as f:
        return json.load(f)

def generate_order_json(order_items):
    menu = load_menu() 
    total_order = {
        "order_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "order_date": datetime.now().isoformat(),
        "items": [],
        "total_price": 0
    }
    
    for item in order_items:
        item_name = item["name"]
        item_size = item["size"]
        item_quantity = item["quantity"]
        
        # encontramos item en el menu
        for category in menu["menu"]["categories"]:
            for menu_item in category["items"]:
                if menu_item["name"].lower() == item_name.lower():
                    # se encontró el tiem, ahora matchearlo a su size
                    for size in menu_item["sizes"]:
                        if size["name"].lower() == item_size.lower():
                            price = size["price"]
                            break
                    else:
                        # si no existe el size, se pone el primero(esto si hay que mejorarlo, creo que primero creamos una funcion
                        # de current_pedido y otra ya de confirmacion de pedido)
                        price = menu_item["sizes"][0]["price"]
                        item_size = menu_item["sizes"][0]["name"]
                    
                    # calculo de total por item
                    item_total = price * item_quantity
                    
                    # añadir orden al json
                    total_order["items"].append({
                        "name": menu_item["name"],
                        "category": category["name"],
                        "size": item_size,
                        "quantity": item_quantity,
                        "price_per_item": price,
                        "item_total": item_total
                    })
                    
                    total_order["total_price"] += item_total
                    break  
            else:
                continue
            break
    
    # guardarlo en el directorio
    order_filename = f"order_{total_order['order_id']}.json"
    with open(order_filename, 'w') as f:
        json.dump(total_order, f, indent=2)
    
    return json.dumps(total_order, indent=2)