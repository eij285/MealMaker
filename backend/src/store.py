# The functions implemented here are meant to be a suitable replacement to a
# properly integrated e-commerce system, either through collaboration with
# existing stores like Woolworths or as part of the 'Code Chefs' brand. This is
# far beyond the scope of the assignment, so we used a csv representation of
# Woolworths' online store instead

import csv

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
                
                valid_items.append(row)

        # Add as many items from the shop needed to reach the required quantity
        # whilst minimising the cost
        # TODO
        for item in valid_items:
            cart_items.append({
                'item_name': item['Product'],
                'unit_type': unit_type,
                'unit_quantity': item['Quantity'],
                'item_cost': item['Cost']
            })

    return cart_items


