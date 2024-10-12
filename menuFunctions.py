import json
import logging
logging.basicConfig(level=logging.INFO)
def load_menu():
    with open('menu.json', 'r') as f:
        return json.load(f)




#####FORMATEOS#####

def format_categories(categories):
    formatted = "Estas son nuestras categorías del menú:\n\n"
    for category in categories:
        formatted += f"- {category}\n\n"
    return formatted + "¿Te gustaría conocer los productos dentro de alguna de estas categorías?"

def format_summarized_menu(menu_json):
    menu = json.loads(menu_json)
    formatted = "Este es nuestro menú completo:\n\n"
    for category in menu['categories']:
        formatted += f"**{category['name']}**\n"
        for item in category['items']:
            formatted += f"- {item['name']}: "
            if len(item['sizes']) == 1:
                formatted += f"${item['sizes'][0]['price']:.2f}\n"
            else:
                sizes = ", ".join([f"{size['name']} ${size['price']:.2f}" for size in item['sizes']])
                formatted += f"{sizes}\n"
        formatted += "\n"
    return formatted + "¿Qué te gustaría ordenar o sobre qué quieres saber más?"



####FUNCIONES#####

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
    return format_summarized_menu(json.dumps(summarized_menu))

def get_menu_categories():
    logging.info("get_menu_categories function called")
    menu = load_menu()
    categories = [category["name"] for category in menu["menu"]["categories"]]
    return format_categories(categories)


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



def get_item_details(item_name):
    logging.info("get_item_details function called")
    menu = load_menu()
    for category in menu["menu"]["categories"]:
        for item in category["items"]:
            if item["name"].lower() == item_name.lower():
                return json.dumps(item, indent=2)
    return json.dumps({"error": "Item not found"}, indent=2)



    return json.dumps(all_products, indent=2)

