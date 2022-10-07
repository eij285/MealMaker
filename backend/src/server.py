from flask import Flask, request
from json import dumps

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
    return None

if __name__ == "__main__":
    APP.run()
