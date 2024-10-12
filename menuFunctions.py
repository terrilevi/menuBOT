import json
import logging

logging.basicConfig(level=logging.INFO)

def load_menu():
    with open('menu.json', 'r') as f:
        return json.load(f)

def get_summarized_menu():
    logging.info("get_summarized_menu function called")
    menu = load_menu()
    summarized_menu = {"categories": []}
    for category in menu["menu"]["categories"]:
        summarized_category = {
            "name": category["name"],
            "items": []
        }
        for item in category["items"]:
            summarized_item = {
                "name": item["name"],
                "sizes": [{"name": size["name"], "price": size["price"]} for size in item["sizes"]]
            }
            summarized_category["items"].append(summarized_item)
        summarized_menu["categories"].append(summarized_category)
    return json.dumps(summarized_menu, indent=2)

"""
# this one i have no idea how it was made, but it works as robust as it should be



    {
        "name": "get_items_by_categories",
        "description": "Get items with their prices within specific categories. The function can handle variations or translations of category names.",
        "parameters": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of category names or keywords. Can include variations or translations."
                }
            },
            "required": ["categories"]
        }
    },


import unidecode
def normalize_text(text):
    return unidecode.unidecode(text.lower())
def get_items_by_categories(categories):
    logging.info("get_items_by_categories function called")
    menu = load_menu()
    items_by_category = {}

    # Normalize the category names in the menu
    normalized_menu_categories = {normalize_text(category["name"]): category for category in menu["menu"]["categories"]}

    # Combine all user input categories into a single string and normalize it
    normalized_user_input = normalize_text(" ".join(categories))

    for menu_category_name, category_data in normalized_menu_categories.items():
        # Check if any part of the normalized menu category name is in the normalized user input
        if any(part in normalized_user_input for part in menu_category_name.split()):
            original_category_name = category_data["name"]
            items_by_category[original_category_name] = []

            for item in category_data["items"]:
                item_info = {"name": item["name"]}
                if len(item["sizes"]) == 1 and item["sizes"][0]["name"] == "Regular":
                    item_info["price"] = item["sizes"][0]["price"]
                else:
                    item_info["sizes"] = [
                        {"size": size["name"], "price": size["price"]}
                        for size in item["sizes"]
                    ]
                items_by_category[original_category_name].append(item_info)

    return json.dumps(items_by_category, indent=2)
"""

def get_items_by_categories(categories):
    menu = load_menu()
    items_by_category = {}

    for category in menu["menu"]["categories"]:
        if category["name"] in categories:
            items_by_category[category["name"]] = []
            for item in category["items"]:
                item_info = {"name": item["name"]}
                if len(item["sizes"]) == 1 and item["sizes"][0]["name"] == "Regular":
                    item_info["price"] = item["sizes"][0]["price"]
                else:
                    item_info["sizes"] = [
                        {"size": size["name"], "price": size["price"]}
                        for size in item["sizes"]
                    ]
                items_by_category[category["name"]].append(item_info)

    return json.dumps(items_by_category, indent=2)


def get_menu_categories():
    logging.info("get_menu_categories function called")
    menu = load_menu()
    categories = [category["name"] for category in menu["menu"]["categories"]]
    return json.dumps(categories, indent=2)



def get_item_details(item_name):
    logging.info("get_item_details function called")
    menu = load_menu()
    for category in menu["menu"]["categories"]:
        for item in category["items"]:
            if item["name"].lower() == item_name.lower():
                return json.dumps(item, indent=2)
    return json.dumps({"error": "Item not found"}, indent=2)



def get_all_products_with_prices():
    logging.info("get_all_products_with_prices function called")
    menu = load_menu()
    all_products = []

    for category in menu["menu"]["categories"]:
        for item in category["items"]:
            product_info = {
                "name": item["name"],
                "category": category["name"],
                "prices": []
            }
            
            for size in item["sizes"]:
                price_info = {
                    "price": size["price"]
                }
                if size["name"] != "Regular" or len(item["sizes"]) > 1:
                    price_info["size"] = size["name"]
                product_info["prices"].append(price_info)
            
            all_products.append(product_info)

    return json.dumps(all_products, indent=2)

