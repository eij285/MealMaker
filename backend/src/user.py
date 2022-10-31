from this import d
import psycopg2
# from error import InputError
import re

from config import DB_CONN_STRING

def user_update(token, given_names, surname, display_name, email, about_me, country, visibility, pronoun, picture):
    """updates user details"""
    if email is None or display_name is None:
        return {
            'status_code': 400,
            'error': 'Display name or email fields cannot be empty'
        }
    output = {}
    output["status_code"] = 200
    output["given_names"] = user_update_name(token, given_names)
    output["last_name"] = user_update_surname(token, surname)
    output["display_name"] = user_update_display_name(token, display_name)
    output["email"] = user_update_email(token, email)
    output["about"] = user_update_about_me(token, about_me)
    output["country"] = user_update_country(token, country)
    output["visibility"] = user_update_visibility(token, visibility)
    output["pronoun"] = user_update_pronoun(token, pronoun)
    output["base64_image"] = user_update_profile_picture(token, picture)
    return output

def user_update_preferences(token, units, efficiency, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free):
    """updates user preferences"""
    output = {}
    output["status_code"] = 200
    output["units"] = user_update_units(token, units)
    output["efficiency"] = user_update_efficiency(token, efficiency)
    output["preferences"] = user_update_preferences_booleans(token, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free)
    return output

def user_info(token):
    """retrieves users information for his update page
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    cur.execute("SELECT pronoun, given_names, last_name, display_name, email, country, about, visibility, base64_image FROM users WHERE token = %s;", (token,))
    user = cur.fetchall()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
        'pronoun': user[0][0],
        'given_names': user[0][1],
        'last_name': user[0][2],
        'display_name': user[0][3],
        'email': user[0][4],
        'country': user[0][5],
        'about': user[0][6],
        'visibility': user[0][7],
        'base64_image': user[0][8]
    }

def user_preferences(token):
    """retrieves users preferences for his update page
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    cur.execute("SELECT units, efficiency, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free FROM users WHERE token = %s;", (token,))
    user = cur.fetchall()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
        'units': user[0][0],
        'efficiency': user[0][1],
        'breakfast': user[0][2],
        'lunch': user[0][3],
        'dinner': user[0][4],
        'snack': user[0][5],
        'vegetarian': user[0][6],
        'vegan': user[0][7],
        'kosher': user[0][8],
        'halal': user[0][9],
        'dairy_free': user[0][10],
        'gluten_free': user[0][11],
        'nut_free': user[0][12],
        'egg_free': user[0][13],
        'shellfish_free': user[0][14],
        'soy_free': user[0][15]
    }

def user_update_preferences_booleans(token, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free):
    """Updates all the booleans of the user preferences page
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET 
                          breakfast = %s,
                          lunch = %s,
                          dinner = %s,
                          snack = %s,
                          vegetarian = %s,
                          vegan = %s,
                          kosher = %s,
                          halal = %s,
                          dairy_free = %s,
                          gluten_free = %s,
                          nut_free = %s,
                          egg_free = %s,
                          shellfish_free = %s,
                          soy_free = %s
                          WHERE token = %s;"""
    input_data = (breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_units(token, unit):
    """Changes users prefered form of measurement

    Checks a registered users prefered form of measurement (metric or imperial). User can then
    Toggle the measurement method into the one that is the opposite of what was already selected
    The default measurement would be metric.

    Args:
        token       (String): token of authenticated user
        unit        (String): new measurement unit to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if unit not in {"Imperial", "Metric"}:
        return {
            'status_code': 400,
            'error': 'Measurement must be one of: ""Imperial"", ""Metric""'
        }
        #raise InputError("Measurement must be one of: ""Imperial"", ""Metric""")
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET units = %s WHERE token = %s;"""
    input_data = (unit, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_efficiency(token, efficiency):
    """Changes users cooking speed

    Checks a registered users cooking speed. User can then
    change their cooking speed so that recipe display suggested time will be adjusted
    default would be beginner but can choose to change to intermediate or expert

    Args:
        token       (String): token of authenticated user
        efficiency  (String): new efficiency to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if efficiency not in {"Beginner", "Intermediate", "Expert"}:
        return {
            'status_code': 400,
            'error': 'Efficiency must be one of: ""Beginner"", ""Intermediate"", ""Expert""'
        }
        #raise InputError("Efficiency must be one of: ""beginner"", ""intermediate"", ""expert""")
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET efficiency = %s WHERE token = %s;"""
    input_data = (efficiency, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_name(token, given_names):
    """Changes users name

    Args:
        token       (String): token of authenticated user
        name        (String): new name to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if given_names is not None:
        if len(given_names) > 20:
            return {
                'status_code': 400,
                'error': 'given_names must be shorter than 20 characters inclusive'
            }
        # raise InputError("Name must be between 1 and 20 characters inclusive")
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET given_names = %s WHERE token = %s;"""
    input_data = (given_names, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_surname(token, last_name):
    """Changes users surname

    Args:
        token       (String): token of authenticated user
        surname     (String): new surname to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if last_name is not None:
        if len(last_name) > 20:
            return {
                'status_code': 400,
                'error': 'last_name must be shorter than 20 characters inclusive'
            }
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET last_name = %s WHERE token = %s;"""
    input_data = (last_name, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }
def user_update_display_name(token, display_name):
    """Changes users display name

    Args:
        token        (String): token of authenticated user
        display_name (String): new display name to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if len(display_name) < 1 or len(display_name) > 30:
        return {
            'status_code': 400,
            'error': 'Display name must be between 1 and 30 characters inclusive'
        }
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET display_name = %s WHERE token = %s;"""
    input_data = (display_name, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_email(token, email):
    """Changes users email

    Args:
        token       (String): token of authenticated user
        email       (String): new email to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Check that the email is not already registered in database
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    if cur.fetchall():
        cur.execute("SELECT email FROM users WHERE token = %s;", (token,))
        current_email = cur.fetchall()
        for emails in current_email:
            if email != emails[0]:
                return {
                    'status_code': 400,
                    'error': 'Email has already been registered'
                }

    # TODO: Check that email is valid
    email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(email_regex, email):
        return {
            'status_code': 400,
            'error': 'Email is in invalid format'
        }
    sql_update_query = """UPDATE users SET email = %s WHERE token = %s;"""
    input_data = (email, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }
def user_update_about_me(token, about_me):
    """Changes users about me

    Args:
        token       (String): token of authenticated user
        about_me    (String): new about to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET about = %s WHERE token = %s;"""
    input_data = (about_me, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }
def user_update_country(token, country):
    """Changes users country

    Args:
        token       (String): token of authenticated user
        country     (String): new country to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if country is not None:
        if len(country) < 0 or len(country) > 20:
            return {
                'status_code': 400,
                'error': 'Country must be shorter than 20 characters inclusive'
            }
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET country = %s WHERE token = %s;"""
    input_data = (country, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }
def user_update_visibility(token, visibility):
    """Changes users visibilty

    Args:
        token       (String): token of authenticated user
        visibility  (String): new visibility to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if visibility not in {"private", "public"}:
        return {
            'status_code': 400,
            'error': 'Visibility must be one of: ""private"", ""public""'
        }
        # raise InputError("Visibility must be one of: ""private"", ""public""")
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET visibility = %s WHERE token = %s;"""
    input_data = (visibility, token)
    cur.execute(sql_update_query, input_data)
    if visibility is "private":
        sql_search_query = """SELECT recipe_id from Recipes r join users u on r.owner_id = u.id WHERE recipe_status = %s AND u.token = %s;"""
        input_data = ("published", token)
        cur.execute(sql_search_query, input_data)
        public_recipes = cur.fetchall()
        # changes all public recipes to drafts
        for recipe in public_recipes:
            sql_update_query = """UPDATE recipes SET recipe_status = %s WHERE recipe_id = %s;"""
            input_data = ("draft", recipe[0])
            cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_pronoun(token, pronoun):
    """Changes users pronoun

    Args:
        token       (String): token of authenticated user
        pronoun     (String): new pronoun to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if pronoun is not None:
        if len(pronoun) < 0 or len(pronoun) > 20:
            return {
                'status_code': 400,
                'error': 'Pronoun must be between 1 and 20 characters inclusive'
            }
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET pronoun = %s WHERE token = %s;"""
    input_data = (pronoun, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_update_profile_picture(token, picture):
    """
    Changes users profile picture

    Args:

    Returns:

    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    sql_update_query = """UPDATE users SET base64_image = %s WHERE token = %s;"""
    input_data = (picture, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
    }

def user_subscribe(token, subscribe_to):
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        sql_search_query = """SELECT visibility FROM users WHERE id = %s"""
        cur.execute(sql_search_query, (subscribe_to,))
        visibility, = cur.fetchone()
        if visibility is "private":
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'Cannot subscribe to a private user'
            }
        sql_search_query = """
            SELECT id FROM users WHERE token IS NOT NULL AND token = %s
            """
        cur.execute(sql_search_query, (str(token),))
        follower_result = cur.fetchone()
        if follower_result is None:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'Subscription requires login'
            }
        u_id, = follower_result
        sql_search_query = """
            SELECT COUNT(*) FROM subscriptions s
            WHERE following_id = %s AND follower_id = %s 
            """
        cur.execute(sql_search_query, (subscribe_to, u_id))
        subscribed, = cur.fetchone()
        if subscribed > 0:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'already subscribed'
            }
        sql_insert_query = """
            INSERT INTO subscriptions (following_id, follower_id)
            VALUES (%s, %s)
            """
        input_data = (subscribe_to, u_id)
        cur.execute(sql_insert_query, input_data)
        conn.commit()
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 500,
            'error': 'Problem subscribing to user'
        }
    return {
        'status_code': 200
    }

def user_unsubscribe(token, unsubscribe_to):
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        sql_search_query = """
            SELECT id FROM users WHERE token IS NOT NULL AND token = %s
            """
        cur.execute(sql_search_query, (str(token),))
        follower_result = cur.fetchone()
        if follower_result is None:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'Unsubscription requires login'
            }
        u_id, = follower_result
        sql_search_query = """
            SELECT COUNT(*) FROM subscriptions s
            WHERE following_id = %s AND follower_id = %s 
            """
        cur.execute(sql_search_query, (unsubscribe_to, u_id))
        subscribed, = cur.fetchone()
        if subscribed == 0:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'not currently subscribed to user'
            }
        sql_delete_query = """
            DELETE FROM subscriptions
            WHERE following_id = %s and follower_id = %s
            """
        input_data = (unsubscribe_to, u_id)
        cur.execute(sql_delete_query, input_data)
        conn.commit()
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 500,
            'error': 'Problem unsubscribing from user'
        }
    return {
        'status_code': 200
    }

def user_get_subs(token, query, error_msg, dict_key):
    """
    Get followers or following list, depending on query. Query must select three
    columns (id, display_name, base64_image) from users table.

    Args:
        token       (String): token of authenticated user
        query       (String): select query to execute

    Returns:
        subs        (list): list of following or followers (id, name, image)

    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        # subscriptions is a graph of outbound links (following) and inbound
        # links (following), thus use same logic for both
        cur.execute(query, (str(token),))
        subs_array = []
        subs = cur.fetchall()
        for id, display_name, base64_image in subs:
            subs_array.append({
                'id': id,
                'display_name': display_name,
                'base64_image': base64_image
            })
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': error_msg
        }
    return {
        'status_code': 200,
        dict_key: subs_array
    }

def user_get_followers(token):
    query = """
        SELECT u.id, u.display_name, u.base64_image FROM users u
        INNER JOIN subscriptions s ON (u.id = s.follower_id)
        INNER JOIN users v ON (s.following_id = v.id)
        WHERE v.token IS NOT NULL AND v.token = %s
        """
    error_msg = 'Unable to get followers list (subscribers)'
    dict_key = 'followers'
    return user_get_subs(token, query, error_msg, dict_key)

def user_get_following(token):
    query = """
        SELECT u.id, u.display_name, u.base64_image FROM users u
        INNER JOIN subscriptions s ON (u.id = s.following_id)
        INNER JOIN users v ON (s.follower_id = v.id)
        WHERE v.token IS NOT NULL AND v.token = %s
        """
    error_msg = 'Unable to get following list (subscriptions)'
    dict_key = 'followings'
    return user_get_subs(token, query, error_msg, dict_key)

def user_get_profile(token, id):
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        sql_search_query = """SELECT visibility FROM users WHERE id = %s"""
        cur.execute(sql_search_query, (id,))
        status, = cur.fetchone()
        if status is "private":
            sql_search_query = """
                SELECT display_name, base64_image FROM users WHERE id = %s
                """
            cur.execute(sql_search_query, (id,))
            user_details = cur.fetchone()
            cur.close()
            conn.close()
            return {
                'status_code': 200,
                'display_name': user_details[0],
                'base64_image': user_details[1],
                'id': id
            }
        sql_data_query = """
            SELECT pronoun, given_names, last_name, display_name, email,
            country, about, visibility, base64_image FROM users
            WHERE id = %s
            """
        cur.execute(sql_data_query, (id,))
        user = cur.fetchone()
        if token:
            sql_subs_query = """
                SELECT COUNT(s.*) FROM subscriptions s
                INNER JOIN users u ON (s.follower_id = u.id)
                INNER JOIN users v ON (s.following_id = v.id)
                WHERE u.token IS NOT NULL AND u.token = %s
                AND v.id = %s
                """
            cur.execute(sql_subs_query, (token, id))
            subscribed, = cur.fetchone()
            is_subscribed = True if subscribed > 0 else False
        else:
            is_subscribed = False

        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'pronoun': user[0],
            'given_names': user[1],
            'last_name': user[2],
            'display_name': user[3],
            'email': user[4],
            'country': user[5],
            'about': user[6],
            'visibility': user[7],
            'base64_image': user[8],
            'id': id,
            'is_subscribed': is_subscribed
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 500,
            'error': 'Problem retrieving user profile'
        }
