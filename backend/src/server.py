from flask import Flask, request
from flask_cors import CORS
from config import SQL_SCHEMA, SQL_DATA
from json import dumps

from auth import auth_register, auth_login, auth_logout, \
                 auth_logout_everywhere, auth_update_pw, auth_reset_link, \
                 auth_reset_pw
from backend_helper import database_reset, database_populate
from user import user_preferences, user_update, user_info, \
                 user_update_preferences, user_subscribe, user_unsubscribe, \
                 user_get_followers, user_get_following, user_get_profile
from recipe import recipe_create, recipe_edit, recipe_update, recipe_clone, \
                   recipe_delete, recipes_fetch_own, recipes_user_published, \
                   recipe_details, recipe_like, \
                   recipe_related
from review import reviews_all_for_recipe, review_create, review_delete, \
                   review_reply, review_reply_delete, review_vote
from feed import feed_fetch_discover, feed_fetch_subscription, \
                 feed_fetch_trending
from search import search
from cart import cart_add_all_ingredients, cart_remove_ingredient, \
                 cart_add_by_id, cart_add_by_name, cart_set_saved, \
                 cart_load_saved, cart_save_payment_method, \
                 cart_update_payment_method, cart_get_payment_method, \
                 cart_list_payment_methods, cart_display_details, \
                 cart_display_all_details, cart_make_order, \
                 cart_fetch_past_orders_all, cart_fetch_past_order_details

APP = Flask(__name__)
CORS(APP)

@APP.route('/')
def index():
    return "COMP3900 Meal Maker by Code Chefs. This route doesn't return data."

@APP.route('/auth/register', methods=['POST'])
def register():
    payload = request.get_json()
    display_name = payload['display-name']
    email = payload['email']
    password = payload['password']

    return dumps(auth_register(display_name, email, password))

@APP.route('/auth/login', methods=['POST'])
def login():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    return dumps(auth_login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def logout():
    payload = request.get_json()
    token = payload['token']

    return dumps(auth_logout(token))

@APP.route('/auth/logout-everywhere', methods=['POST'])
def logout_everywhere():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    return dumps(auth_logout_everywhere(email, password))

@APP.route('/auth/update-password', methods=['PUT'])
def update_password():
    payload = request.get_json()
    token = payload['token']
    password = payload['password']
    
    return dumps(auth_update_pw(token, password))

@APP.route('/auth/reset-link', methods=['PUT'])
def reset_link():
    payload = request.get_json()
    email = payload['email']
    base_url = "http://localhost:3000/password-reset?"

    return dumps(auth_reset_link(email, base_url))

@APP.route('/auth/reset-password', methods=['PUT'])
def reset_password():
    payload = request.get_json()
    email = payload['email']
    code = payload['code']
    password = payload['password']

    return dumps(auth_reset_pw(email, code, password))

@APP.route('/user/update', methods=['PUT'])
def update_user_details():
    payload = request.get_json()
    token = payload['token']
    display_name = payload['display-name']
    name = payload['given-names']
    surname = payload['last-name']
    email = payload['email']
    about_me = payload['about']
    country = payload['country']
    visibility = payload['visibility']
    pronoun = payload['pronoun']
    picture = payload['base64-image']
    return dumps(user_update(token, name, surname, display_name, email, about_me, country, visibility, pronoun, picture))

@APP.route('/user/preferences/update', methods=['PUT'])
def update_user_preferences():
    payload = request.get_json()
    token = payload['token']
    units = payload['units']
    efficiency = payload['efficiency']
    breakfast = payload['breakfast']
    lunch = payload['lunch']
    dinner = payload['dinner']
    snack = payload['snack']
    vegetarian = payload['vegetarian']
    vegan = payload['vegan']
    kosher = payload['kosher']
    halal = payload['halal']
    dairy_free = payload['dairy_free']
    gluten_free = payload['gluten_free']
    nut_free = payload['nut_free']
    egg_free = payload['egg_free']
    shellfish_free = payload['shellfish_free']
    soy_free = payload['soy_free']
    return dumps(user_update_preferences(token, units, efficiency, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free))

@APP.route('/user/info', methods=['POST'])
def get_user_details():
    payload = request.get_json()
    token = payload['token']
    
    return dumps(user_info(token))

@APP.route('/user/preferences', methods=['POST'])
def get_user_preferences():
    payload = request.get_json()
    token = payload['token']
    
    return dumps(user_preferences(token))

@APP.route('/user/subscribe', methods=['PUT'])
def subscribe():
    payload = request.get_json()
    token = payload['token']
    subscribe_to = payload['id']
    
    return dumps(user_subscribe(token, subscribe_to))

@APP.route('/user/unsubscribe', methods=['POST'])
def unsubscribe():
    payload = request.get_json()
    token = payload['token']
    unsubscribe_to = payload['id']
    
    return dumps(user_unsubscribe(token, unsubscribe_to))

@APP.route('/user/get/subscribers', methods=['POST'])
def get_subscribers():
    payload = request.get_json()
    token = payload['token']
    
    return dumps(user_get_followers(token))

@APP.route('/user/get/subscriptions', methods=['POST'])
def get_subscriptions():
    payload = request.get_json()
    token = payload['token']
    
    return dumps(user_get_following(token))

@APP.route('/user/get/profile', methods=['POST'])
def get_profile():
    payload = request.get_json()
    token = payload['token']
    id = payload['id']
    
    return dumps(user_get_profile(token, id))

@APP.route('/recipe/create', methods=['POST'])
def create_recipe():
    data = request.get_json()
    token = data['token']
    name = data['name']
    description = data['description']
    servings = data['servings']
    recipe_status = data['recipe_status']

    return dumps(recipe_create(name, description, servings, recipe_status, token))

@APP.route('/recipe/edit', methods=['POST'])
def edit_recipe():
    data = request.get_json()
    token = data['token']
    recipe_id = data['recipe_id']
    return dumps(recipe_edit(recipe_id, token))

@APP.route('/recipe/update', methods=['POST'])
def update_recipe():
    data = request.get_json()
    token = data['token']
    return dumps(recipe_update(data, token))

@APP.route('/recipe/clone', methods=['POST'])
def copy_recipe():
    data = request.get_json()
    token = data['token']
    recipe_id = data['recipe_id']
    return dumps(recipe_clone(recipe_id, token))

@APP.route('/recipe/delete', methods=['POST'])
def delete_recipe():
    data = request.get_json()
    token = data['token']
    recipe_id = data['recipe_id']
    return dumps(recipe_delete(recipe_id, token))

@APP.route('/recipes/fetch-own', methods=['POST'])
def fetch_own_recipes():
    data = request.get_json()
    token = data['token']
    return dumps(recipes_fetch_own(token))

@APP.route('/recipes/user/published', methods=['GET'])
def published_user_recipes():
    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
    else:
        user_id = -1
    return dumps(recipes_user_published(user_id))

@APP.route('/recipe/details', methods=['GET', 'POST'])
def details_for_recipe():
    if request.method == 'POST':
        data = request.get_json()
        token = data['token']
        recipe_id = data['recipe_id']
    else:
        if 'recipe_id' in request.args:
            recipe_id = request.args.get('recipe_id')
        else:
            recipe_id = None
        token = None
    return dumps(recipe_details(recipe_id, token))

@APP.route('/recipe/like', methods=['POST'])
def like_recipe():
    data = request.get_json()
    token = data['token']
    recipe_id = data['recipe_id']
    return dumps(recipe_like(recipe_id, token))

@APP.route('/recipe/related', methods=['GET'])
def related_recipes():
    recipe_id = request.args.get('recipe_id')
    return dumps(recipe_related(recipe_id))

@APP.route('/reviews/all-for-recipe', methods=['GET', 'POST'])
def all_reviews_for_recipe():
    if request.method == 'POST':
        data = request.get_json()
        token = data['token']
        recipe_id = data['recipe_id']
    else:
        if 'recipe_id' in request.args:
            recipe_id = request.args.get('recipe_id')
        else:
            recipe_id = None
        token = None
    return dumps(reviews_all_for_recipe(recipe_id, token))

@APP.route('/review/create', methods=['POST'])
def create_review():
    data = request.get_json()
    token = data['token']
    recipe_id = data['recipe_id']
    rating = data['rating']
    comment = data['comment']
    return dumps(review_create(recipe_id, rating, comment, token))

@APP.route('/review/delete', methods=['POST'])
def delete_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    return dumps(review_delete(review_id, token))

@APP.route('/review/reply', methods=['POST'])
def reply_to_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    reply = data['reply']
    return dumps(review_reply(review_id, reply, token))

@APP.route('/review/reply/delete', methods=['POST'])
def delete_reply_to_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    return dumps(review_reply_delete(review_id, token))

@APP.route('/review/vote', methods=['POST'])
def vote_for_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    is_upvote = data['is_upvote']
    return dumps(review_vote(review_id, is_upvote, token))

@APP.route('/search', methods=['GET'])
def search_recipe():
    if 'search_term' in request.args:
        search_term = request.args.get('search_term')
    else:
        search_term = ""
    return dumps(search(search_term))

@APP.route('/feed/discover', methods=['POST'])
def feed_discover():
    data = request.get_json()
    token = data['token']
    return dumps(feed_fetch_discover(token))

@APP.route('/feed/subscription', methods=['POST'])
def feed_subscription():
    data = request.get_json()
    token = data['token']
    return dumps(feed_fetch_subscription(token))

@APP.route('/feed/trending', methods=['GET'])
def feed_trending():
    return dumps(feed_fetch_trending())

@APP.route('/cart/add-all', methods=['POST'])
def cart_add_all():
    # Starts a cart using current recipe
    # 
    # Don't forget conversions
    data = request.get_json()
    r_id = data['recipe_id']
    servings = data['servings']
    token = data['token']

    return dumps(cart_add_all_ingredients(r_id, servings, token))

    # return {
    #   'body': {
    #       'cart_id': 2
    #       'ingredients: [
    #           {
    #               'item_id': 3
    #               'item_name':
    #               'item_quantity':
    #               'item_cost':
    #           },
    #           {
    #               'item_id': 2
    #               'item_name':
    #               'item_quantity':
    #               'item_cost':
    #           },
    #       ]
    #   }
    # }

@APP.route('/cart/rmv-ingredient', methods=['POST'])
def cart_rmv_ingredient():
    # Removes ingredient from active cart
    data = request.get_json()
    ing_id = data['cart_ingredient_id']
    token = data['token']

    return dumps(cart_remove_ingredient(ing_id, token))

    # return {
    #   'body': {}
    # }

@APP.route('/cart/add-ingredient/id', methods=['POST'])
def cart_add_ingredient_id():
    # Adds ingredient from a recipe's ingredients (individual)
    data = request.get_json()
    ing_id = data['recipe_ingredient_id']
    token = data['token']

    return dumps(cart_add_by_id(ing_id, token))

    # return {
    #   'body': {
    #       'cart_id': id of new cart (if previously inactive)
    #       'item_id': 3
    #       'item_name':
    #       'item_quantity':
    #       'item_cost':
    #   }
    # }

@APP.route('/cart/add-ingredient/name', methods=['POST'])
def cart_add_ingredient_name():
    # Adds ingredient by search term
    data = request.get_json()
    ing_name = data['ingredient_name']
    ing_unit = data['ingredient_unit']
    ing_quantity = data['ingredient_quantity']
    token = data['token']

    return dumps(cart_add_by_name(ing_name, ing_unit, ing_quantity, token))

    # return {
    #   'body': {
    #       'cart_id': id of new cart (if previously inactive)
    #       'item_id': 3
    #       'item_name':
    #       'item_quantity':
    #       'item_cost':
    #   }
    # }


@APP.route('/cart/save', methods=['POST'])
def cart_save():
# Saves cart so an order can be made in the future
    data = request.get_json()
    token = data['token']
    return dumps(cart_set_saved(token))

@APP.route('/cart/load', methods=['POST'])
def cart_load():
# Loads a saved cart so the order can be made
    data = request.get_json()
    cart_id = data['cart_id']
    token = data['token']
    return dumps(cart_load_saved(cart_id, token))

@APP.route('/cart/payment-method/save', methods=['POST'])
def cart_payment_method_save():
    data = request.get_json()
    name = data['card_name']
    number = data['card_number']
    exp_date = data['card_exp_date']
    cvv = data['card_cvv']
    token = data['token']

    return dumps(cart_save_payment_method(name, number, exp_date, cvv, token))

    # return {
    #   'body': {
    #       'method_id': 2
    #   }
    # }

@APP.route('/cart/payment-method/update', methods=['POST'])
def cart_payment_method_update():
    # Returns details of specific updated payment method (individual)
    data = request.get_json()
    name = data['card_name']
    number = data['card_number']
    exp_date = data['card_exp_date']
    cvv = data['card_cvv']
    token = data['token']

    return dumps(cart_update_payment_method(name, number, exp_date, cvv, token))

    # return {
    #   'body': {
    #       'method_id': 2
    #   }
    # }

@APP.route('/cart/payment-method/get', methods=['POST'])
def cart_payment_method_get():
    # Returns details of specific payment method (individual)
    data = request.get_json()
    method_id = data['method_id']
    token = data['token']

    return dumps(cart_get_payment_method(method_id, token))

    # return {
    #   'body': {
    #       'card_name': 
    #       'card_number': 
    #       'card_cvv':
    #       'card_exp_date':
    #   }
    # }

@APP.route('/cart/payment-method/list', methods=['POST'])
def cart_payment_method_list():
# Returns list of payment methods
    data = request.get_json()
    token = data['token']

    return dumps(cart_list_payment_methods(token))
    # return {
    #   'body': [
    #       {
    #           'method_id': 2
    #           'card_name': 
    #           'card_number': 
    #           'card_cvv':
    #           'card_exp_date':
    #       },
    #       {
    #           'method_id': 3
    #           'card_name': 
    #           'card_number': 
    #           'card_cvv':
    #           'card_exp_date':
    #       },
    #   ]
    # }

@APP.route('/cart/display', methods=['POST'])
def cart_display():
    data = request.get_json()
    cart_id = data['cart_id']
    token = data['token']
    return dumps(cart_display_details(cart_id, token))
# Displays cart given id

# @APP.route('/cart/display/active', methods=['POST'])
# def cart_display():
#     data = request.get_json()
#     token = data['token']
#     return dumps(cart_display_details(token))
# # Displays currently active cart

@APP.route('/cart/display/all')
def cart_display_all():
    data = request.get_json()
    token = data['token']
# Gets list of all carts given user id
    return dumps(cart_display_all_details(token))

@APP.route('/cart/order', methods=['POST'])
def cart_order():
    # Places order using stored data in db
    # Post request so we have the option to send token for emails?
    # Get request will also need email supplied
    data = request.get_json()
    method_id = data['method_id']
    deliver_by = data['deliver_by']
    deliver_loc = data['delivery_address']
    token = data['token']

    return dumps(cart_make_order(method_id, deliver_by, deliver_loc, token))

@APP.route('/cart/past-orders', methods=['POST'])
def cart_past_orders():
    data = request.get_json()
    token = data['token']

    return dumps(cart_fetch_past_orders_all(token))

    # return {
    #   'body': [
    #       {
    #           'order_id': ,
    #           'order_number': ,
    #           'payment_amount': ,
    #           'order_status': ,
    #       },
    #       {
    #           'order_id': ,
    #           'order_number': ,
    #           'payment_amount': ,
    #           'order_status': ,
    #       },
    #   ]
    # }

@APP.route('/cart/past-orders/get', methods=['POST'])
def cart_past_orders_get():
    data = request.get_json()
    order_id = data['order_id']
    token = data['token']

    return dumps(cart_fetch_past_order_details(order_id, token))

    # return {
    #   'body': {
    #       order_id        SERIAL,
    #       order_number    CHAR(10) NOT NULL UNIQUE,
    #       cart_id         INTEGER NOT NULL,
    #       placed_on       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #       completed_on    TIMESTAMP,
    #       order_status    VARCHAR(10) NOT NULL DEFAULT ('pending'),
    #       payment_method_id INTEGER NOT NULL,
    #       delivery_time   TIMESTAMP NOT NULL,
    #       delivery_address TEXT NOT NULL,
    #       payment_amount  MONEY NOT NULL,
    #       'items': [
    #           {
    #               'item_id': 3
    #               'item_name':
    #               'item_quantity':
    #               'item_cost':
    #           },
    #           {
    #               'item_id': 2
    #               'item_name':
    #               'item_quantity':
    #               'item_cost':
    #           },
    #       ],
    #       'card_name': 
    #       'card_number': 
    #       'card_cvv':
    #       'card_exp_date':
    #   },
    # }

# 

# TODO:
# Update user stories to allow only authenticated
# 
# JSON File containing ingredients (substitute for grocery store integration or
#   web scraping)
# 

# @APP.route('/recipe/publish', methods=['PUT'])
# def publish_recipe():
#     data = request.get_json()
#     # Verify token
#     token = data['token']
#     if not verify_token(token):
#         return dumps({'status_code': 401, 'error': None})

    
#     recipe_id = data['recipe_id']
#     return dumps(publish_recipe(recipe_id, "t"))

# @APP.route('/recipe/unpublish', methods=['PUT'])
# def unpublish_recipe():
#     data = request.get_json()
#     # Verify token
#     token = data['token']
#     if not verify_token(token):
#         return dumps({'status_code': 401, 'error': None})
    
#     recipe_id = data['recipe_id']
#     return dumps(publish_recipe(recipe_id, "f"))


@APP.route('/reset', methods=['GET'])
def reset():
    if database_reset():
        message = f'Database {SQL_SCHEMA} successfully reset'
    else:
        message = f'Database {SQL_SCHEMA} failed to reset'
        
    return {
        'message': message
    }

@APP.route('/populatedb', methods=['GET'])
def populatedb():
    if database_populate():
        message = f'Database {SQL_SCHEMA} successfully populated with {SQL_DATA}'
    else:
        message = f'Database {SQL_SCHEMA} failed to populate with {SQL_DATA}'
        
    return {
        'message': message
    }

if __name__ == "__main__":
    APP.run(debug=True)
