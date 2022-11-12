from tkinter import E
from config import DB_CONN_STRING
from backend_helper import verify_token
from datetime import datetime, timezone, timedelta

import psycopg2

def check_cart_active():
    pass

def activate_new_cart():
    pass

def purchase_minimal_costs():
    pass

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
                 'active' AND owner_id = $s;"
    cur.execute(sql_query, (u_id,))

    sql_result = cur.fetchall()
    if not sql_result:
        pass



    return {
        'status_code': 200,
        'body': {
            'cart_id': 12,
            'ingredients': [
                {
                    'item_id': 3,
                    'item_name': 'Apple Royal Gala',
                    'unit_type': 'pieces',
                    'unit_quantity': 1,
                    'item_quantity': 2,
                    'item_cost': 1.56
                },
                {
                    'item_id': 5,
                    'item_name': 'Woolworths Almonds Natural',
                    'unit_type': 'grams',
                    'unit_quantity': 450,
                    'item_quantity': 2,
                    'item_cost': 7.70
                }
            ]
        }
    }

def cart_remove_ingredient(ingredient_id, token):
    return {
        'status_code': 200,
        'body': {}
    }

def cart_add_by_id(ingr_id, token):
    return {
        'status_code': 200,
        'body': {
            'cart_id': 12,
            'item_id': 4,
            'item_name': 'D\'orsogna Middle Bacon Per Kg',
            'unit_type': 'kg',
            'unit_quantity': 1,
            'item_quantity': 2,
            'item_cost': 28.00
        }
    }

def cart_add_by_name(ing_name, ing_unit, ing_quantity, token):
    return {
        'status_code': 200,
        'body': {
            'cart_id': 12,
            'item_id': 4,
            'item_name': 'Woolworths Middle Bacon',
            'unit_type': 'grams',
            'unit_quantity': 250,
            'item_quantity': 3,
            'item_cost': 12.00
        }
    }

def cart_set_saved(token):
    return {
        'status_code': 200,
        'body': {}
    }

def cart_load_saved(cart_id, token):
    return {
        'status_code': 200,
        'body': {
            'cart_id': 3
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
    updated = datetime.now(tz=timezone.utc)

    return {
        'status_code': 200,
        'cart_id': 2,
        'owner_id': 4,
        'cart_status': 'saved',
        'last_updated': updated,
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