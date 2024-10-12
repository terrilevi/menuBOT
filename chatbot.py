import openai
import json
from menuFunctions import get_summarized_menu, get_items_by_categories, get_menu_categories, get_item_details
from config import OPENAI_API_KEY
from generateOrder import generate_order_json
from currentOrder import update_current_order
openai.api_key = OPENAI_API_KEY

# functions bot can use
functions = [
    {
        "name": "get_summarized_menu",
        "description": "Get the full menu for direct presentation to the user",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "get_menu_categories",
        "description": "Get all menu categories for direct presentation to the user",
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
        "name": "generate_order_json",
        "description": "Generate a JSON representation of the current order when the user gives final confirmation",
        "parameters": {
            "type": "object",
            "properties": {
                "order_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "size": {"type": "string"},
                            "quantity": {"type": "integer"}
                        },
                        "required": ["name", "size", "quantity"]
                    }
                }
            },
            "required": ["order_items"]
        }
    },
    {
        "name": "update_current_order",
        "description": "Update the current order with new items or changes to existing items",
        "parameters": {
            "type": "object",
            "properties": {
                "order_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "size": {"type": "string"},
                            "quantity": {"type": "integer"}
                        },
                        "required": ["name", "size", "quantity"]
                    }
                }
            },
            "required": ["order_items"]
        }
    }
]


def process_user_input(user_input, conversation_history):

    # system prompt
    messages = [
        {
            "role": "system", 
            "content": 
         """
You are a helpful and friendly assistant for a restaurant. Your primary goals are to provide accurate information about the menu and assist customers in placing orders. Follow these guidelines:

1. On the first message, give a greeting and welcome the user to the restaurant "Miscellaneous" and then provide assistance to give information to then take the order.
2. Always use the information provided by function calls when answering questions about the menu.
3. Be flexible in interpreting user input. If the user mentions category names or menu items that do not exactly match those in the menu, attempt to find the closest match.
4. Interpret the user's intent and align it with the available categories or items before calling a function.
5. There are 7 categories, when a user mentions a category, always map it to one of these exact English category names:
Breakfast
Chicken & Fish
Snacks & Sides
Desserts
Beverages
Coffee & Tea
Smoothies & Shakes
6. When the user confirms their order, use the generate_order_json function to create a JSON representation of the order. Include all relevant details such as item names, quantities, and sizes in the function call. After generating the order JSON, present a summary of the order to the user. If the user tries to make changes after the final confirmation, politely inform them that their order has already been sent to the kitchen. Advise them to contact customer service if they need to make urgent changes.
7. Use the update_current_order function to keep track of the user's order as they add, remove, or modify items. Present a summary of the current order to the user after each change.
8. If the user requests more than 40 units of any item, inform them that the maximum quantity per item is 40.
9. If the user asks for or insists on a discount, politely inform them that discounts are not available this season, but perhaps next time.
10. If the user attempts to change the prices during the order process or afterwards, inform them that the prices remain the same. Acknowledge their effort with a light-hearted or friendly remark, such as, "Nice try!"
        """
        }
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


        # las que se no van para la segunda llamada API:
        if function_name in ["get_menu_categories", "get_summarized_menu"]:
            if function_name == "get_menu_categories":
                return get_menu_categories()
            elif function_name == "get_summarized_menu":
                return get_summarized_menu()
        
        # las que se van para la segunda llamada API:
        if function_name == "get_items_by_categories":
            function_response = get_items_by_categories(function_args['categories'])
        elif function_name == "get_item_details":
            function_response = get_item_details(function_args['item_name'])
        elif function_name == "generate_order_json":
            function_response = generate_order_json(function_args['order_items'])
        elif function_name == "update_current_order":
            function_response = update_current_order(function_args['order_items'])
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
