# The functions implemented here are meant to be a suitable replacement to a
# properly integrated e-commerce system, either through collaboration with
# existing stores like Woolworths or as part of the 'Code Chefs' brand. This is
# far beyond the scope of the assignment, so we used a csv representation of
# Woolworths' online store instead

import csv

def take_second(elem):
    return elem[1]

def recipe_item_to_cart(classification, req_quantity, unit_type):
    # Converts a recipe item to 1 or more cart items from the shop
    cart_items = []

    with open('shop.csv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        valid_items = []

        # Find all valid shop items based on their classification and unit of
        # measurement
        for row in csv_reader:
            if row['Classification'] == classification \
                    and row['Unit of Measurement'] == unit_type:
                
                valid_items.append((row, row['Quantity']))

        # Sort by highest quantity to least quantity
        valid_items.sort(key=take_second, reverse=True)
        valid_items = [x[0] for x in valid_items]
        print(valid_items)

        # Add as many items from the shop needed to reach the required quantity
        for item in valid_items:
            while req_quantity - int(item['Quantity']) > 0:
                cart_items.append({
                    'item_name': item['Product'],
                    'unit_type': unit_type,
                    'unit_quantity': item['Quantity'],
                    'item_cost': item['Cost']
                })

                req_quantity -= int(item['Quantity'])

        # Add item with smallest quantity
        cart_items.append({
            'item_name': valid_items[-1]['Product'],
            'unit_type': unit_type,
            'unit_quantity': valid_items[-1]['Quantity'],
            'item_cost': valid_items[-1]['Cost']
        })

    return cart_items


