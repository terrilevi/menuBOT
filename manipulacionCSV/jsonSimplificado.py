import csv
import json
import re

def fl_oz_to_ml(fl_oz):
    return round(fl_oz * 29.5735, 2)

def transform_menu_data(input_file, output_json):
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        menu_data = {"menu": {"categories": []}}
        categories = {}

        for row in reader:
            category_name = row['Category']
            if category_name not in categories:
                categories[category_name] = {"name": category_name, "items": []}

            item_name = re.sub(r'\((Small|Medium|Large|Child)\)', '', row['Item']).strip()
            item = next((i for i in categories[category_name]["items"] if i["name"] == item_name), None)
            
            if not item:
                item = {
                    "id": f"{category_name[:2].upper()}{len(categories[category_name]['items']):03d}",
                    "name": item_name,
                    "sizes": []
                }
                categories[category_name]["items"].append(item)

            serving_size = row['Serving Size']
            if 'fl oz' in serving_size:
                value = float(serving_size.split()[0])
                serving_size_value = fl_oz_to_ml(value)
                serving_size_unit = "ml"
            else:
                value_match = re.search(r'(\d+(\.\d+)?)', serving_size)
                serving_size_value = float(value_match.group(1)) if value_match else 0
                serving_size_unit = "g"

            size_match = re.search(r'\((Small|Medium|Large|Child)\)', row['Item'])
            size_name = size_match.group(1) if size_match else "Regular"

            item["sizes"].append({
                "name": size_name,
                "price": float(row['Price']),
                "servingSize": {
                    "value": serving_size_value,
                    "unit": serving_size_unit
                }
            })

        menu_data["menu"]["categories"] = list(categories.values())

    with open(output_json, 'w') as file:
        json.dump(menu_data, file, indent=2)

    print(f"Transformation complete. Output file: {output_json}")

# Usage
input_file = 'menu.csv'
output_json = 'simplified_menu.json'
transform_menu_data(input_file, output_json)