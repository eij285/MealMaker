from flask import Flask, request
from json import dumps
from auth import auth_register
from recipe import create_recipe, edit_recipe, publish_recipe
from backend_helper import *

APP = Flask(__name__)
###

@APP.route('/auth/register', methods=['POST'])
def register():
    payload = request.get_json()
    username = payload['username']
    email = payload['email']
    password = payload['password']

    return auth_register(username, email, password)

###
@APP.route('/auth/login', methods=['POST'])
def login():
    payload = request.get_json()
    login = payload['login']
    password = payload['password']

    # return auth_login(login, password)
    pass

@APP.route('/auth/update-password', methods=['PUT'])
def update_password():
    pass

@APP.route('/auth/reset-link', methods=['PUT'])
def reset_link():
    payload = request.get_json()
    email = payload['email']

    # return auth_reset_link(email)
    pass

@APP.route('/auth/reset-password', methods=['PUT'])
def reset_password():
    payload = request.get_json()
    password = payload['password']

    # return auth_reset_pw(password)
    pass

@APP.route('/user/update', methods=['PUT'])
def update_user_details():
    pass

@APP.route('/recipe/create', methods=['POST'])
def create_recipe():
    data = request.get_json()
    # Verify token
    token = data['token']
    if not verify_token(token):
        return dumps({'status_code': 401, 'error': None})
    
    name = data['name']
    description = data['description']
    method = data['method']
    portion_size = data['portion_size']
    token = data['token']
    return dumps(create_recipe(name, description, method, portion_size, token))
        

@APP.route('/recipe/edit', methods=['PUT'])
def publish_recipe():
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

@APP.route('/recipe/publish', methods=['PUT'])
def publish_recipe():
    data = request.get_json()
    # Verify token
    token = data['token']
    if not verify_token(token):
        return dumps({'status_code': 401, 'error': None})
    
    recipe_id = data['recipe_id']
    publish = data['publish']
    return dumps(publish_recipe(recipe_id, publish))

@APP.route('/recipe/unpublish', methods=['PUT'])
def unpublish_recipe():
    data = request.get_json()
    # Verify token
    token = data['token']
    if not verify_token(token):
        return dumps({'status_code': 401, 'error': None})
    
    recipe_id = data['recipe_id']
    publish = data['publish']
    return dumps(publish_recipe(recipe_id, publish))

@APP.route('/reset', methods=['DELETE'])
def reset():
    pass

if __name__ == "__main__":
    APP.run()
