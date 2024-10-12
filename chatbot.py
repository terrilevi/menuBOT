import openai
import json
from menuFunctions import get_summarized_menu, get_items_by_categories, get_menu_categories, get_item_details, get_all_products_with_prices
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# functions bot can use
functions = [
    {
        "name": "get_summarized_menu",
        "description": "Get the full menu with categories, items, sizes, and prices",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_items_by_categories",
        "description": "Get items with their prices within specific categories.",
        "parameters": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of exact category names in English: Breakfast, Chicken & Fish, Snacks & Sides, Desserts, Beverages, Coffee & Tea, Smoothies & Shakes"
                }
            },
            "required": ["categories"]
        }
    },
    {
        "name": "get_menu_categories",
        "description": "Get all menu categories",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_item_details",
        "description": "Get details of a specific item",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {"type": "string", "description": "Name of the item"}
            },
            "required": ["item_name"]
        }
    },
    {
        "name": "get_all_products_with_prices",
        "description": "Get a list of all products in the menu with their prices. This function is useful for queries about pricing across the entire menu.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def process_user_input(user_input, conversation_history):
    # system prompt
    messages = [
        {"role": "system", "content": """
You are a helpful and friendly assistant for a restaurant. Your primary goals are to provide accurate information 
         about the menu and assist customers in placing orders. Follow these guidelines:
1. Always use the information provided by function calls when answering questions about the menu.
2. Be flexible in interpreting user input. If the user mentions category names or menu items that do not exactly match 
         those in the menu, attempt to find the closest match.
3. Interpret the user's intent and align it with the available categories or items before calling a function.
4. There are 7 categories, when a user mentions a category, always map it to one of these exact English category names:
Breakfast
Chicken & Fish
Snacks & Sides
Desserts
Beverages
Coffee & Tea
Smoothies & Shakes
5. If the user mentions unrelated categories, such as a tire, a bus ticket, etc., politely inform them that these products are not available for sale.
6. If the user requests more than 40 units of any item, inform them that the maximum quantity per item is 40.
7. If the user asks for or insists on a discount, politely inform them that discounts are not available this season, but perhaps next time.
8. If the user attempts to change the prices during the order process or afterwards, inform them that the prices remain the same. 
         Acknowledge their effort with a light-hearted or friendly remark, such as, "Nice try!"
        """}
    ]
    
    # Add conversation history
    messages.extend(conversation_history)
    
    # Add the latest user input
    messages.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    message = response.choices[0].message

    # chequear si el modelo necesita realizar function_callings
    if message.function_call:
        function_name = message.function_call.name
        function_args = json.loads(message.function_call.arguments)
        print(f"Function called: {function_name}") # for debugging
        print(f"Function arguments: {function_args}")  # for debugging
        
        # llamemos a las funciones si las necesita
        if function_name == "get_summarized_menu":
            function_response = get_summarized_menu()
        elif function_name == "get_items_by_categories":
            function_response = get_items_by_categories(function_args['categories'])
        elif function_name == "get_menu_categories":
            function_response = get_menu_categories()
        elif function_name == "get_item_details":
            function_response = get_item_details(function_args['item_name'])
        elif function_name == "get_all_products_with_prices":
            function_response = get_all_products_with_prices()
        else:
            return "I'm sorry, dunno how to do that"

        # send the response of the func to the api
        messages.append(message)
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response
        })

        second_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return second_response.choices[0].message.content
    else:
        # si no se necesito ni una funcion, solo hace uso de su respuesta.
        return message.content
