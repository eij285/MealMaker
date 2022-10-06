from flask import Flask, request
from json import dumps

APP = Flask(__name__)

@APP.route('/auth/register')
def register():
    payload = request.get_json()
    # According to acceptance criteria for MM3900-10, should be able to use
    # email so might have to rename this to something suitable
    payload = request.get_json()
    

@APP.route('/auth/login')
def login():
    payload = request.get_json()
    # According to acceptance criteria for MM3900-10, should be able to use
    # email so might have to rename this to something suitable
    username = payload['username']
    password = payload['password']
    return dumps()

if __name__ == "__main__":
    APP.run()