from crypt import methods
from flask import Flask, request
from json import dumps
import psycopg2

from auth import auth_register
from helpers import database_reset, files_reset

APP = Flask(__name__)

@APP.route('/', methods=['GET'])
def index():
    conn = psycopg2.connect("dbname=codechefs-db")
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
    login = payload['email']
    password = payload['password']

    # return auth_login(email, password)
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

@APP.route('/reset', methods=['DELETE', 'GET'])
def reset():
    status = database_reset()
    if status:
        files_reset()
    return {}

if __name__ == "__main__":
    APP.run(debug=True)
