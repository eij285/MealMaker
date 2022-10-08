from flask import Flask, request

from auth import auth_register

APP = Flask(__name__)

@APP.route('/auth/register', methods=['POST'])
def register():
    payload = request.get_json()
    username = payload['username']
    email = payload['email']
    password = payload['password']

    return auth_register(username, email, password)

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
    pass

@APP.route('/recipe/publish', methods=['PUT'])
def publish_recipe():
    pass

@APP.route('/recipe/unpublish', methods=['PUT'])
def unpublish_recipe():
    pass

@APP.route('/reset', methods=['DELETE'])
def reset():
    pass

if __name__ == "__main__":
    APP.run()
