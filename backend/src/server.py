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
                 user_get_followers, user_get_following, user_get_profile, \
                 get_users
from recipe import recipe_create, recipe_publish, recipe_edit, recipe_update, \
                   recipe_clone, recipe_delete, recipes_fetch_own, \
                   recipes_user_published, recipe_details, recipe_like, \
                   recipe_related
from review import reviews_all_for_recipe, review_create, review_delete, \
                   review_reply, review_reply_delete, review_vote
from feed import feed_fetch_discover, feed_fetch_subscription, \
                 feed_fetch_trending
from search import search
from message import message_send, message_edit, message_delete, message_react
from message_room import *
from recipe_book import cookbook_create, cookbook_delete, cookbook_edit, \
                        cookbook_fetch_own, cookbook_update, cookbook_view, \
                        cookbooks_user_published, cookbook_subscribe, \
                        cookbook_unsubscribe, cookbook_add_recipe, \
                        cookbook_remove_recipe, cookbook_all_recipes, \
                        cookbook_publish
from notifications import notifications_fetch_all

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

@APP.route('/user/get/users', methods=['POST'])
def users_get():    
    return dumps(get_users())

@APP.route('/recipe/create', methods=['POST'])
def create_recipe():
    data = request.get_json()
    token = data['token']
    name = data['name']
    description = data['description']
    servings = data['servings']
    recipe_status = data['recipe_status']
    return dumps(recipe_create(name, description, servings, recipe_status, token))

@APP.route('/recipe/publish', methods=['PUT'])
def publish_recipe():
    data = request.get_json()
    token = data['token']    
    recipe_id = data['recipe_id']
    return dumps(recipe_publish(recipe_id, 'published', token))

@APP.route('/recipe/unpublish', methods=['PUT'])
def unpublish_recipe():
    data = request.get_json()
    token = data['token']    
    recipe_id = data['recipe_id']
    return dumps(recipe_publish(recipe_id, 'draft', token))

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

@APP.route('/cookbook/create', methods=['POST'])
def create_cookbook():
    data = request.get_json()
    token = data['token']
    name = data['name']
    description = data['description']
    status = data['status']

    return dumps(cookbook_create(name, status, description, token))

@APP.route('/cookbook/edit', methods=['POST'])
def edit_cookbook():
    data = request.get_json()
    token = data['token']
    cookbook_id = data['cookbook_id']
    return dumps(cookbook_edit(cookbook_id, token))

@APP.route('/cookbook/all-recipes', methods=['POST'])
def all_recipes_for_cookbook():
    data = request.get_json()
    token = data['token']
    cookbook_id = data['cookbook_id']
    return dumps(cookbook_all_recipes(cookbook_id, token))

@APP.route('/cookbook/update', methods=['POST'])
def update_cookbook():
    data = request.get_json()
    token = data['token']
    return dumps(cookbook_update(data, token))

@APP.route('/cookbook/delete', methods=['POST'])
def delete_cookbook():
    data = request.get_json()
    token = data['token']
    cookbook_id = data['cookbook_id']
    return dumps(cookbook_delete(cookbook_id, token))

@APP.route('/cookbook/fetch-own', methods=['POST'])
def fetch_own_cookbooks():
    data = request.get_json()
    token = data['token']
    return dumps(cookbook_fetch_own(token))

@APP.route('/cookbooks/user/published', methods=['GET'])
def published_user_cookbooks():
    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
    else:
        user_id = -1
    return dumps(cookbooks_user_published(user_id))

@APP.route('/cookbook/view', methods=['GET', 'POST'])
def details_for_cookbook():
    if request.method == 'POST':
        data = request.get_json()
        token = data['token']
        cookbook_id = data['cookbook_id']
    else:
        if 'cookbook_id' in request.args:
            cookbook_id = request.args.get('cookbook_id')
        else:
            cookbook_id = None
        token = None
    return dumps(cookbook_view(cookbook_id, token))

@APP.route('/cookbook/subscribe', methods=['PUT'])
def subscribe_cookbook():
    payload = request.get_json()
    token = payload['token']
    subscribe_to = payload['cookbook_id']
    
    return dumps(cookbook_subscribe(token, subscribe_to))

@APP.route('/cookbook/unsubscribe', methods=['POST'])
def unsubscribe_cookbook():
    payload = request.get_json()
    token = payload['token']
    unsubscribe_to = payload['cookbook_id']
    return dumps(cookbook_unsubscribe(token, unsubscribe_to))

@APP.route('/cookbook/add/recipe', methods=['PUT'])
def recipe_add_cookbook():
    payload = request.get_json()
    token = payload['token']
    cookbook_id = payload['cookbook_id']
    recipe_id = payload['recipe_id']
    return dumps(cookbook_add_recipe(token, cookbook_id, recipe_id))

@APP.route('/cookbook/remove/recipe', methods=['POST'])
def recipe_remove_cookbook():
    payload = request.get_json()
    token = payload['token']
    cookbook_id = payload['cookbook_id']
    recipe_id = payload['recipe_id']
    return dumps(cookbook_remove_recipe(token, cookbook_id, recipe_id))

@APP.route('/cookbook/publish', methods=['PUT'])
def publish_cookbook():
    data = request.get_json()
    token = data['token']
    cookbook_id = data['cookbook_id']
    return dumps(cookbook_publish(cookbook_id, 'published', token))

@APP.route('/cookbook/unpublish', methods=['PUT'])
def unpublish_cookbook():
    data = request.get_json()
    token = data['token']
    cookbook_id = data['cookbook_id']
    return dumps(cookbook_publish(cookbook_id, 'draft', token))

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


@APP.route('/message/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data['message']
    target_id = data['room_id']
    token = data['token']
    return dumps(message_send(target_id, message, token))

@APP.route('/message/edit', methods=['POST'])
def edit_message():
    data = request.get_json()
    message_id = data['message_id']
    message_content = data['message']
    token = data['token']
    return dumps(message_edit(message_id, message_content, token))

@APP.route('/message/delete', methods=['POST'])
def delete_message():
    data = request.get_json()
    message_id = data['message_id']
    token = data['token']
    return dumps(message_delete(message_id, token))

@APP.route('/message/react', methods=['POST'])
def react_message():
    data = request.get_json()
    message_id = data['message_id']
    react_char = data['react_char']
    token = data['token']
    return dumps(message_react(message_id, react_char, token))

@APP.route('/message-rooms/create', methods=['POST'])
def create_message_room():
    data = request.get_json()
    token = data['token']
    member_id_list = data['member_id_list']
    return dumps(create_room(member_id_list, token))

@APP.route('/message-rooms/delete', methods=['POST'])
def delete_message_room():
    data = request.get_json()
    token = data['token']
    room_id = data['room_id']
    return dumps(delete_room(token, room_id))

@APP.route('/message-rooms', methods=['POST'])
def message_rooms():
    data = request.get_json()
    token = data['token']
    return fetch_user_rooms(token)

@APP.route('/message-rooms/add-member', methods=['POST'])
def message_rooms_add_member():
    data = request.get_json()
    token = data['token']
    room_id = data['room_id']
    member_id_list = data['member_id_list']
    return add_member_to_room(room_id, member_id_list, token)

@APP.route('/message-rooms/set-owner', methods=['POST'])
def message_rooms_set_owner():
    data = request.get_json()
    token = data['token']
    room_id = data['room_id']
    owner_id_list = data['owner_id_list']
    return add_owner_to_room(room_id, owner_id_list, token)

@APP.route('/message-rooms/fetch-details', methods=['POST'])
def message_rooms_fetch_details():
    data = request.get_json()
    token = data['token']
    room_id = data['room_id']
    return fetch_room_details(room_id, token)

@APP.route('/notifications/fetch-all', methods=['POST'])
def fetch_all_notifications():
    data = request.get_json()
    token = data['token']
    return notifications_fetch_all(token)
    

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
