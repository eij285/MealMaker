from crypt import methods
from flask import Flask, request
from flask_cors import CORS
from json import dumps
import psycopg2

from auth import auth_register, auth_login, auth_logout, \
                 auth_logout_everywhere, auth_update_pw, auth_reset_link, \
                 auth_reset_pw
from backend_helper import database_reset, files_reset
from user import user_preferences, user_update, user_info, user_update_preferences, user_subscribe, user_unsubscribe, user_get_followers, user_get_following, user_get_profile
from recipe import recipe_create, recipe_edit, recipe_update, recipe_clone, \
                   recipe_delete, recipes_fetch_own, recipe_details, recipe_like
from review import reviews_all_for_recipe, review_create, review_delete, \
                   review_reply, review_reply_delete
from backend_helper import database_reset

APP = Flask(__name__)
CORS(APP)

@APP.route('/', methods=['GET'])
def index():
    conn = psycopg2.connect("dbname=meal-maker-db")
    cur = conn.cursor()
    print(conn)

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
    # Verify token
    token = payload['token']
    #if not verify_token(token):
    #    return dumps({'status_code': 401, 'error': None})
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
    # Verify token
    token = payload['token']
    #if not verify_token(token):
    #    return dumps({'status_code': 401, 'error': None})
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
    # Verify token
    token = payload['token']
    #if not verify_token(token):
    #    return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_info(token))

@APP.route('/user/preferences', methods=['POST'])
def get_user_preferences():
    payload = request.get_json()
    # Verify token
    token = payload['token']
    #if not verify_token(token):
    #   return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_preferences(token))

@APP.route('/user/subscribe', methods=['PUT'])
def subscribe():
    payload = request.get_json()
    # Verify token
    token = payload['token']
    subscribe_to = payload['id']
    #if not verify_token(token):
    #   return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_subscribe(token, subscribe_to))

@APP.route('/user/unsubscribe', methods=['DELETE'])
def unsubscribe():
    payload = request.get_json()
    # Verify token
    token = payload['token']
    unsubscribe_to = payload['id']
    #if not verify_token(token):
    #   return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_unsubscribe(token, unsubscribe_to))

@APP.route('/user/get/subscribers', methods=['POST'])
def get_subscribers():
    payload = request.get_json()
    # Verify token
    token = payload['token']
    #if not verify_token(token):
    #   return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_get_followers(token))

@APP.route('/user/get/subscriptions', methods=['POST'])
def get_subscriptions():
    payload = request.get_json()
    # Verify token
    token = payload['token']
    #if not verify_token(token):
    #   return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_get_following(token))

@APP.route('/user/get/profile', methods=['POST'])
def get_profile():
    payload = request.get_json()
    # Verify token
    id = payload['id']
    #if not verify_token(token):
    #   return dumps({'status_code': 401, 'error': None})
    
    return dumps(user_get_profile(id))

@APP.route('/recipe/create', methods=['POST'])
def create_recipe():
    data = request.get_json()
    # Verify token
    token = data['token']
    #if not verify_token(token):
    #    return dumps({'status_code': 401, 'error': None})
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
    return recipe_like(recipe_id, token)

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
    return review_create(recipe_id, rating, comment, token)

"""
@APP.route('/review/delete', methods=['POST'])
def create_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    return review_delete(review_id, token)
"""

@APP.route('/review/reply', methods=['POST'])
def reply_to_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    reply = data['reply']
    return review_reply(review_id, reply, token)

@APP.route('/review/reply/delete', methods=['POST'])
def delete_reply_to_review():
    data = request.get_json()
    token = data['token']
    review_id = data['review_id']
    return review_reply_delete(review_id, token)


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

@APP.route('/reset', methods=['DELETE', 'GET'])
def reset():
    status = database_reset()
    if status:
        files_reset()
    return {}

if __name__ == "__main__":
    APP.run(debug=True)
