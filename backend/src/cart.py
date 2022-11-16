from config import DB_CONN_STRING
from backend_helper import verify_token
from datetime import datetime, timezone, timedelta
from store import recipe_item_to_cart

import psycopg2
import uuid
import random
from pprint import pprint

def cart_add_all_ingredients(r_id, servings, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Check if cart is active
    sql_query = "SELECT cart_id FROM shopping_carts WHERE cart_status = \
                 'active' AND owner_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    # If not active, activate a new cart
    if not sql_result:
        sql_query = "INSERT INTO shopping_carts(owner_id) VALUES (%s) \
                     RETURNING cart_id;"
        cur.execute(sql_query, (str(u_id),))

        cart_id = cur.fetchone()[0]

    # Otherwise, set the cart_id from sql_query results
    else:
        cart_id, = sql_result[0]

    # Use recipe_id to get servings
    cur.execute("SELECT servings FROM recipes WHERE recipe_id = %s;", (r_id,))
    sql_result = cur.fetchall()

    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Invalid recipe_id'
        }
    else:
        r_servings, = sql_result[0]
    
    # Use recipe_id to get recipe ingredients
    sql_query = "SELECT ingredient_name, quantity, unit FROM \
                 recipe_ingredients WHERE recipe_id = %s;"
    cur.execute(sql_query, (str(r_id),))

    sql_result = cur.fetchall()

    cart_items = []

    # Add all cart items information to list
    for ingredient in sql_result:
        name, quantity, unit = ingredient
        cart_items += recipe_item_to_cart(name, quantity/r_servings * servings,
                                          unit)

    # Map each item to its count value and aggregate
    cart_items = [(x, cart_items.count(x)) for x in cart_items]
    cart_items = \
            [x for i, x in enumerate(cart_items) if x not in cart_items[i + 1:]]

    ingredients_body_content = []

    # For each cart item, insert into database and ingredients body
    for object in cart_items:
        item, quantity = object
        sql_query = "INSERT INTO cart_items(ingredient_name, \
                     ingredient_quantity, ingredient_cost, unit_type, \
                     item_quantity, cart_id) \
                     VALUES (%s, %s, %s, %s, %s, %s) RETURNING item_id;"

        cur.execute(sql_query, (item['item_name'], item['unit_quantity'], \
                    item['item_cost'], item['unit_type'], quantity, \
                    str(cart_id)))
        
        item_id = cur.fetchone()[0]

        ingredients_body_content.append({
            'item_id': item_id,
            'item_name': item['item_name'],
            'unit_type': item['unit_type'],
            'unit_quantity': item['unit_quantity'],
            'item_quantity': quantity,
            'item_cost': item['item_cost']
        })

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'cart_id': cart_id,
            'ingredients': ingredients_body_content
        }
    }

def cart_remove_ingredient(ing_id, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # TODO: Verify cart item is from user's cart

    # Drop ingredient
    cur.execute("DELETE FROM cart_items WHERE item_id = %s;", (str(ing_id),))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {}
    }

def cart_add_by_id(ing_id, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid
    
    # Get ingredient from recipe
    sql_query = "SELECT ingredient_name, quantity, unit FROM \
                 recipe_ingredients WHERE ingredient_id = %s;"
    cur.execute(sql_query, (str(ing_id),))

    sql_result = cur.fetchall()

    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Invalid recipe_ingredient_id'
        }

    name, quantity, unit = sql_result[0]

    # Check if cart is active
    sql_query = "SELECT cart_id FROM shopping_carts WHERE cart_status = \
                 'active' AND owner_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    # If not active, activate a new cart
    if not sql_result:
        sql_query = "INSERT INTO shopping_carts(owner_id) VALUES (%s) \
                     RETURNING cart_id;"
        cur.execute(sql_query, (str(u_id),))

        cart_id = cur.fetchone()[0]

    # Otherwise, set the cart_id from sql_query results
    else:
        cart_id, = sql_result[0]

    # Insert into cart items
    cart_items = recipe_item_to_cart(name, quantity, unit)

    # Map each item to its count value and aggregate
    cart_items = [(x, cart_items.count(x)) for x in cart_items]
    cart_items = list(set(cart_items))

    ingredients_body_content = []

    for object in cart_items:
        item, quantity = object

        sql_query = "INSERT INTO cart_items(ingredient_name, \
                     ingredient_quantity, ingredient_cost, unit_type, cart_id) \
                     VALUES (%s, %s, %s, %s, %s) RETURNING item_id;"
        cur.execute(sql_query, (item['item_name'], item['unit_quantity'], \
                    item['item_cost'], item['unit_type'], cart_id))
        
        item_id = cur.fetchone()[0]

        ingredients_body_content.append({
            'item_id': item_id,
            'item_name': item['item_name'],
            'unit_type': item['unit_type'],
            'unit_quantity': item['unit_quantity'],
            'item_quantity': quantity,
            'item_cost': item['item_cost']
        })

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'cart_id': 12,
            'ingredients': ingredients_body_content
        }
    }

def cart_add_by_name(ing_name, ing_unit, ing_quantity, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Check if cart is active
    sql_query = "SELECT cart_id FROM shopping_carts WHERE cart_status = \
                 'active' AND owner_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    # If not active, activate a new cart
    if not sql_result:
        sql_query = "INSERT INTO shopping_carts(owner_id) VALUES (%s) \
                     RETURNING cart_id;"
        cur.execute(sql_query, (str(u_id),))

        cart_id = cur.fetchone()[0]

    # Otherwise, set the cart_id from sql_query results
    else:
        cart_id, = sql_result[0]

    # Insert into cart items
    cart_items = recipe_item_to_cart(ing_name, ing_quantity, ing_unit)

    # Map each item to its count value and aggregate
    cart_items = [(x, cart_items.count(x)) for x in cart_items]
    cart_items = list(set(cart_items))

    ingredients_body_content = []

    for object in cart_items:
        item, quantity = object

        sql_query = "INSERT INTO cart_items(ingredient_name, \
                     ingredient_quantity, ingredient_cost, unit_type, cart_id) \
                     VALUES (%s, %s, %s, %s, %s) RETURNING item_id;"
        cur.execute(sql_query, (item['item_name'], item['unit_quantity'], \
                    item['item_cost'], item['unit_type'], cart_id))
        
        item_id = cur.fetchone()[0]

        ingredients_body_content.append({
            'item_id': item_id,
            'item_name': item['item_name'],
            'unit_type': item['unit_type'],
            'unit_quantity': item['unit_quantity'],
            'item_quantity': quantity,
            'item_cost': item['item_cost']
        })

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'cart_id': 12,
            'ingredients': ingredients_body_content
        }
    }

def cart_set_saved(token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Check if cart is active
    sql_query = "SELECT cart_id FROM shopping_carts WHERE cart_status = \
                 'active' AND owner_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    if not sql_result:
        return {
            'status_code': 200,
            'error': 'No currently active cart'
        }

    else:
        cart_id, = sql_result[0]

    # Set cart to saved
    sql_query = "UPDATE shopping_carts SET cart_status = 'saved' WHERE cart_id = %s"
    cur.execute(sql_query, (str(cart_id),))

    # Create new active cart
    sql_query = "INSERT INTO shopping_carts(owner_id) VALUES (%s) RETURNING \
                 cart_id;"
    cur.execute(sql_query, (str(u_id),))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {}
    }

def cart_load_saved(cart_id, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Check if cart is valid
    sql_query = "SELECT cart_status FROM shopping_carts WHERE cart_id = %s;"
    cur.execute(sql_query, (str(cart_id),))

    sql_result = cur.fetchall()

    # Cart id does not exist
    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Invalid cart id: cart does not exist'
        }
    else:
        cart_status, = sql_result[0]

    # Cart id is already active
    if cart_status == 'active':
        return {
            'status_code': 400,
            'error': 'Invalid cart id: cart is already active'
        }

    # Drop current cart
    cur.execute("DELETE FROM shopping_carts WHERE cart_status = 'active'")

    # Load saved cart
    sql_query = "UPDATE shopping_carts SET cart_status = 'active' WHERE \
                 cart_id = %s;"
    cur.execute(sql_query, (str(cart_id),))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'cart_id': cart_id
        }
    }

def cart_save_payment_method(name, number, exp_date, cvv, token):
    return {
        'status_code': 200,
        'body': {
            'method_id': 2
        }
    }

def cart_update_payment_method(name, number, exp_date, cvv, token):
    return {
        'status_code': 200,
        'body': {
            'method_id': 2
        }
    }

def cart_get_payment_method(method_id, token):
    return {
        'status_code': 200,
        'body': {
            'card_name': 'Person A',
            'card_number': 4023546912302424,
            'card_cvv': 412,
            'card_exp_date': '12/30'
        }
    }

def cart_list_payment_methods(token):
    return {
        'status_code': 200,
        'body': [
            {
                'method_id': 2,
                'card_name': 'Person A',
                'card_number': 4023546912302424,
                'card_cvv': 412,
                'card_exp_date': '12/30'
            },
            {
                'method_id': 3,
                'card_name': 'Person A\'s Business Card',
                'card_number': 4098877212341234,
                'card_cvv': 412,
                'card_exp_date': '12/25'
            }
        ]
    }

def cart_display_details(cart_id, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Check that the cart belongs to the user
    sql_query = "SELECT * FROM shopping_carts WHERE cart_id = %s \
                 AND owner_id = %s;"
    cur.execute(sql_query, (str(cart_id), str(u_id)))

    sql_result = cur.fetchall()

    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Cart id does not belong to requested user'
        }

    cart_id_db, owner_id, cart_status, last_updated = sql_result[0]

    # Get all cart items
    cur.execute("SELECT * FROM cart_items WHERE cart_id = %s;", (str(cart_id),))
    sql_result = cur.fetchall()

    # Loop through all items in result
    items_body_content = []
    for item in sql_result:
        item_id, item_name, ing_quantity, item_cost, unit_type, \
                item_quantity, _ = item
        
        items_body_content.append({
            'item_id': item_id,
            'item_name': item_name,
            'unit_type': unit_type,
            'unit_quantity': ing_quantity,
            'item_quantity': item_quantity,
            'item_cost': item_cost
        })

    return {
        'status_code': 200,
        'cart_id': cart_id_db,
        'owner_id': owner_id,
        'cart_status': cart_status,
        'last_updated': last_updated,
        'items': items_body_content,
    }

def cart_display_all_details(token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Find all cart ids belonging to user
    sql_query = "SELECT cart_id, cart_status FROM shopping_carts WHERE \
                 owner_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    carts_body_content = []

    # Append all to body content of json
    for result in sql_result:
        cart_id, cart_status = result

        carts_body_content.append({
            'cart_id': cart_id,
            'cart_status': cart_status
        })

    return {
        'status_code': 200,
        'carts': carts_body_content
    }

def cart_make_order(m_id, deliver_by, deliver_loc, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Generate order number
    cur.execute("SELECT MAX(order_id) FROM orders;")
    sql_result = cur.fetchone()[0]

    # Using order_id for seed
    if not sql_result:
        seed = 1
    else:
        seed, = sql_result[0]
        seed = int(seed)

    # Generate order number
    rd = random.Random()
    rd.seed(seed)
    num = uuid.UUID(int=rd.getrandbits(128)).hex[:8].upper()

    order_no = 'MM' + num

    # Create new order
    sql_query = "INSERT INTO orders(order_number, payment_method_id, \
                 delivery_time, delivery_address, payment_amount, owner_id) \
                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING order_id;"
    cur.execute(sql_query, (order_no, m_id, deliver_by, deliver_loc, '0', \
                str(u_id)))
    
    order_id, = cur.fetchone()[0]

    # Get active cart and its ingredients
    sql_query = "SELECT i.ingredient_name, i.ingredient_quantity, \
                 i.ingredient_cost, i.unit_type, i.item_quantity \
                 FROM shopping_cart c LEFT JOIN cart_items i \
                 ON s.cart_id = i.cart_id \
                 WHERE s.owner_id = %s AND s.cart_status = 'active';"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()
    total_cost = 0

    # Insert all results into order_items and add cost to order
    for result in sql_result:
        ing_name, ing_quantity, ing_cost, unit_type, item_quantity = result
        total_cost += float(ing_cost) * int(item_quantity)

        # Add items to order_items
        sql_query = "INSERT INTO order_items(ingredient_name, \
                     ingredient_quantity, ingredient_cost, unit_type, \
                     item_quantity, order_id) \
                     VALUES (%s, %s, %s, %s, %s, %s);"
        cur.execute(sql_query, (ing_name, ing_quantity, ing_cost, unit_type, \
                    item_quantity, order_id))
        
    sql_query = "UPDATE orders SET payment_amount = %s WHERE order_id = %s;"
    cur.execute(sql_query, (str(total_cost), str(u_id)))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {}
    }

def cart_fetch_past_orders_all(token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Get all orders
    sql_query = "SELECT order_id, order_number, placed_on, payment_amount, \
                 order_status FROM orders WHERE owner_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    body_content = []
    for result in sql_result:
        order_id, order_number, placed_on, payment_amount, order_status = result

        body_content.append({
            'order_id': order_id,
            'order_number': order_number,
            'placed_on': placed_on,
            'payment_amount': payment_amount,
            'order_status': order_status
        })

    return {
        'status_code': 200,
        'body': body_content
    }

def cart_fetch_past_order_details(order_id, token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Verify token
    token_valid = verify_token(token)
    if not token_valid:
        return {
            'status_code': 401,
            'error': 'Invalid token'
        }
    else:
        u_id = token_valid

    # Get order details
    sql_query = "SELECT * FROM orders WHERE order_id = %s AND owner_id = %s;"
    cur.execute(sql_query, (str(order_id), str(u_id)))
    
    sql_result = cur.fetchall()

    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Order does not belong to user'
        }

    _, order_number, placed_on, completed_on, order_status, payment_method_id, \
            delivery_time, delivery_address, payment_amount = sql_result[0]
    
    # Get order item details
    sql_query = "SELECT * FROM order_items WHERE order_id = %s;"
    cur.execute(sql_query, (str(order_id),))

    sql_result = cur.fetchall()

    items_body_content = []

    for result in sql_result:
        item_id, ingredient_name, ingredient_quantity, ingredient_cost, \
                unit_type, item_quantity, _ = result

        items_body_content.append({
            'item_id': item_id,
            'item_name': ingredient_name,
            'unit_type': unit_type,
            'unit_quantity': ingredient_quantity,
            'item_quantity': item_quantity,
            'item_cost': ingredient_cost
        })

    # Get payment details
    sql_query = "SELECT cardholder_name, card_number, expiration_date, cvv \
                 FROM payment_methods WHERE method_id = %s;"
    cur.execute(sql_query, (str(payment_method_id),))

    card_name, card_number, card_cvv, card_exp_date = cur.fetchone()[0]


    return {
        'order_id': order_id,
        'order_number': order_number,
        'placed_on': placed_on,
        'completed_on': completed_on,
        'order_status': order_status,
        'payment_method_id': payment_method_id,
        'delivery_time': delivery_time,
        'delivery_address': delivery_address,
        'payment_amount': payment_amount,
        'items': items_body_content,
        'card_name': card_name,
        'card_number': card_number,
        'card_cvv': card_cvv,
        'card_exp_date': card_exp_date
    }

if __name__ == "__main__":
    pprint(cart_make_order(3, datetime.now(), datetime.now(), "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoxLCJleHAiOjE2NjkxOTA3NzJ9.rhh0O0fVKrKOY0DiQplEaBDg6_xknlWhO8XC9qB-txE"))