from config import DB_CONN_STRING
from backend_helper import verify_token
from datetime import datetime, timezone, timedelta
from store import recipe_item_to_cart

import psycopg2

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

    ingredients_body_content = []

    # For each cart item, insert into database and ingredients body
    for item in cart_items:
        sql_query = "INSERT INTO cart_items (ingredient_name, \
                     ingredient_quantity, ingredient_cost, unit_type, cart_id) \
                     VALUES (%s, %s, %s, %s, %s) RETURNING item_id;"

        cur.execute(sql_query, (item['item_name'], item['unit_quantity'], \
                    item['item_cost'], item['unit_type'], str(cart_id)))
        
        item_id = cur.fetchone()[0]

        # TODO: Add handling to check for quantities
        ingredients_body_content.append({
            'item_id': item_id,
            'item_name': item['item_name'],
            'unit_type': item['unit_type'],
            'unit_quantity': item['unit_quantity'],
            'item_quantity': 1,
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
    ingredients_body_content = []

    for item in cart_items:
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
            'item_quantity': 1,
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
    ingredients_body_content = []

    for item in cart_items:
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
            'item_quantity': 1,
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
    

    return {
        'status_code': 200,
        'cart_id': cart_id_db,
        'owner_id': owner_id,
        'cart_status': cart_status,
        'last_updated': last_updated,
        'items': [
            {
                'item_id': 3,
                'item_name': 'Apple Royal Gala',
                'unit_type': 'pieces',
                'unit_quantity': 1,
                'item_quantity': 2,
                'item_cost': 1.56
            },
            {
                'item_id': 4,
                'item_name': 'D\'orsogna Middle Bacon Per Kg',
                'unit_type': 'kg',
                'unit_quantity': 1,
                'item_quantity': 2,
                'item_cost': 28.00
            }
        ],
        'owner_name': 'Person C'
    }

def cart_display_all_details(token):

    return {
        'status_code': 200,
        'cart_id': 2
    }

def cart_make_order(m_id, deliver_by, deliver_loc, token):
    return {
        'status_code': 200,
        'body': {}
    }

def cart_fetch_past_orders_all(token):
    return {
        'status_code': 200,
        'body': [
            {
                'order_id': 1,
                'order_number': 'CDE_CFSsomeRandOmStr1ng',
                'payment_amount': 120.50,
                'order_status': 'completed'
            },
            {
                'order_id': 2,
                'order_number': 'CDE_CFSsomeRand0mStr2ng',
                'payment_amount': 88.45,
                'order_status': 'pending'
            }
        ]
    }

def cart_fetch_past_order_details(order_id, token):
    placed = datetime.now(tz=timezone.utc)
    completed = datetime.now(tz=timezone.utc) + timedelta(days=3)
    delivery = datetime.now(tz=timezone.utc) + timedelta(days=14)

    return {
        'order_id': 3,
        'order_number': 'CDE_CFSsomeRand0mStr3ng',
        # 'cart_id': 5,
        'placed_on': placed,
        'completed_on': completed,
        'order_status': 'pending',
        'payment_method_id': 3,
        'delivery_time': delivery,
        'payment_amount': 123.50,
        'items': [
            {
                'item_id': 3,
                'item_name': 'Apple Royal Gala',
                'unit_type': 'pieces',
                'unit_quantity': 1,
                'item_quantity': 2,
                'item_cost': 1.56
            },
            {
                'item_id': 4,
                'item_name': 'D\'orsogna Middle Bacon Per Kg',
                'unit_type': 'kg',
                'unit_quantity': 1,
                'item_quantity': 2,
                'item_cost': 28.00
            }
        ],
        'card_name': 'Person A',
        'card_number': 4023546912302424,
        'card_cvv': 412,
        'card_exp_date': '12/30'
    }

if __name__ == "__main__":
    print(cart_display_details(1, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoxLCJleHAiOjE2NjkwNzE3NDh9.ElABkTG2hFL-Nvu0Q1WMdTcuoDeLLpvrA5Ejr-d1gaw"))