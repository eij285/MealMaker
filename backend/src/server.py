from crypt import methods
from flask import Flask, request
from flask_cors import CORS
from json import dumps
import psycopg2

from auth import auth_register, auth_login, auth_logout, \
                 auth_logout_everywhere, auth_update_pw, auth_reset_link, \
                 auth_reset_pw
from backend_helper import database_reset, files_reset
from user import user_preferences, user_update, user_info, user_update_preferences
from recipe import create_recipe, edit_recipe, publish_recipe
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
    return dumps(user_update(token, name, surname, display_name, email, about_me, country, visibility, pronoun))

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

@APP.route('/recipe/create', methods=['POST'])
def create_recipe():
    data = request.get_json()
    # Verify token
    token = data['token']
    #if not verify_token(token):
    #    return dumps({'status_code': 401, 'error': None})
    
    name = data['name']
    description = data['description']
    method = data['method']
    portion_size = data['portion_size']
    token = data['token']
    return dumps(create_recipe(name, description, method, portion_size, token))
        
'''
@APP.route('/recipe/edit', methods=['PUT'])
def edit_recipe():
    data = request.get_json()
    # Verify token
    token = data['token']
    if not verify_token(token):
        return dumps({'status_code': 401, 'error': None})
    
    name = data['name']
    description = data['description']
    methods = data['method']
    portion_size = data['portion_size']
    recipe_id = data['recipe_id']

    return dumps(edit_recipe(name, description, methods, portion_size, recipe_id))
'''

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
