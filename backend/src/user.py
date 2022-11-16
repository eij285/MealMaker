from this import d
import psycopg2
# from error import InputError
import re

from config import DB_CONN_STRING

def user_update(token, given_names, surname, display_name, email, about_me, country, visibility, pronoun, picture):
    """Updates user details

    Args:
        token               (String): token of authenticated user
        given_name          (String)
        surname             (String)
        dsiplay_name        (String)
        email               (String)
        about_me            (String)
        country             (String)
        visibility          (String)
        pronoun             (String)
        picture             (String)
        
    Returns:
        Status 200 - successful change of user details
        Status 400 - empty fields
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
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
    """Updates user preferences

    Args:
        token               (String): token of authenticated user
        units               (String)
        efficiency          (String)
        breakfast           (Boolean)
        lunch               (Boolean)
        dinner              (Boolean)
        snack               (Boolean)
        vegetarian          (Boolean)
        vegan               (Boolean)
        kosher              (Boolean)
        halal               (Boolean)
        dairy_free          (Boolean)
        gluten_free         (Boolean)
        nut_free            (Boolean)
        egg_free            (Boolean)
        shellfish_free      (Boolean)
        soy_free            (Boolean)

    Returns:
        Status 200 - successful change of user perferences
        Status 400 - empty fields or invalid fields
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    output = {}
    output["status_code"] = 200
    output["units"] = user_update_units(token, units)
    output["efficiency"] = user_update_efficiency(token, efficiency)
    output["preferences"] = user_update_preferences_booleans(token, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free)
    return output

def user_info(token):
    """retrieves users information for his update page
    Args:
        token               (String): token of authenticated user        
    Returns:
        Status 200 - body containing dictionary with fields
            given_name          (String)
            surname             (String)
            dsiplay_name        (String)
            email               (String)
            about_me            (String)
            country             (String)
            visibility          (String)
            pronoun             (String)
            picture             (String)
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
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
    Args:
        token               (String): token of authenticated user

    Returns:
        Status 200 - body containing dictionary with fields
            units               (String)
            efficiency          (String)
            breakfast           (Boolean)
            lunch               (Boolean)
            dinner              (Boolean)
            snack               (Boolean)
            vegetarian          (Boolean)
            vegan               (Boolean)
            kosher              (Boolean)
            halal               (Boolean)
            dairy_free          (Boolean)
            gluten_free         (Boolean)
            nut_free            (Boolean)
            egg_free            (Boolean)
            shellfish_free      (Boolean)
            soy_free            (Boolean)
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
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
    """Helper function that updates all the booleans of the user preferences page

    Args:
        token               (String): token of authenticated user
        breakfast           (Boolean)
        lunch               (Boolean)
        dinner              (Boolean)
        snack               (Boolean)
        vegetarian          (Boolean)
        vegan               (Boolean)
        kosher              (Boolean)
        halal               (Boolean)
        dairy_free          (Boolean)
        gluten_free         (Boolean)
        nut_free            (Boolean)
        egg_free            (Boolean)
        shellfish_free      (Boolean)
        soy_free            (Boolean)

    Returns:
        Status 200 - successful change of user perferences
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
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
    if visibility == "private":
        sql_search_query = """
            SELECT recipe_id FROM recipes r JOIN users u ON (r.owner_id = u.id)
            WHERE recipe_status = %s AND u.token = %s;
            """
        input_data = ("published", token)
        cur.execute(sql_search_query, input_data)
        public_recipes = cur.fetchall()
        # changes all public recipes to drafts
        #print(public_recipes)
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
        token       (String): token of authenticated user
        picture     (String): new picture url to replace old

        
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
    """subscribe to a user (token must be valid)
    
    Args:
        token             (String): token of authenticated user
        unsubscribe_to    (Integer): id of user u are subscribing to
        
    Returns:
        Status 200 - user subscribed to successfully
        Status 400 - already subscribed
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
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
    """unsubscribe to a user (token must be valid)
    
    Args:
        token             (String): token of authenticated user
        unsubscribe_to    (Integer): id of user u are subscribing to
        
    Returns:
        Status 200 - user unsubscribed to successfully
        Status 400 - not already subscribed
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
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

def user_get_subs(user_id, query, error_msg, dict_key):
    """
    Get followers or following list, depending on query. Query must select three
    columns (id, display_name, base64_image) from users table.

    Args:
        user_id     (Integer): user id of user requesting data for
        query       (String): select query to execute
        error_msg   (String): error message to show if there's an error
        dict_key    (String): dictionary key to use for 

    Returns:
        subs        (list): list of following or followers (id, name, image)
    """
    if not re.match(r'^[0-9]+$', str(user_id)):
        return {
            'status_code': 404,
            'error': 'User with given id does not exist'
        }
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        # subscriptions is a graph of outbound links (following) and inbound
        # links (following), thus use same logic for both
        cur.execute(query, (str(user_id),))
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

def user_get_followers(user_id):
    query = """
        SELECT u.id, u.display_name, u.base64_image FROM users u
        INNER JOIN subscriptions s ON (u.id = s.follower_id)
        INNER JOIN users v ON (s.following_id = v.id)
        WHERE v.id = %s AND v.visibility = 'public'
        """
    error_msg = 'Unable to get followers list (subscribers)'
    dict_key = 'followers'
    followers_list = user_get_subs(user_id, query, error_msg, dict_key)

    if 'error' in followers_list:
        return followers_list
    # determine if reason user has no followers is because they are private
    if not followers_list[dict_key]:
        try:
            conn = psycopg2.connect(DB_CONN_STRING)
            cur = conn.cursor()
            visibility_query = """
                SELECT visibility FROM users
                WHERE id = %s
                """
            cur.execute(visibility_query, (user_id,))
            followers_list['visibility'] = cur.fetchone()[0]
            cur.close()
            conn.close()
        except:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': error_msg
            }
    else:
        followers_list['visibility'] = 'public'
    return followers_list

def user_get_following(user_id):
    query = """
        SELECT u.id, u.display_name, u.base64_image FROM users u
        INNER JOIN subscriptions s ON (u.id = s.following_id)
        WHERE s.follower_id = %s
        """
    error_msg = 'Unable to get following list (subscriptions)'
    dict_key = 'followings'
    return user_get_subs(user_id, query, error_msg, dict_key)

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
            subs_query = """
                SELECT COUNT(s.*) FROM subscriptions s
                INNER JOIN users u ON (s.follower_id = u.id)
                INNER JOIN users v ON (s.following_id = v.id)
                WHERE u.token IS NOT NULL AND u.token = %s
                AND v.id = %s
                """
            cur.execute(subs_query, (token, id))
            subscribed, = cur.fetchone()
            is_subscribed = True if subscribed > 0 else False
            efficiency_query = """
                SELECT efficiency FROM users
                WHERE token IS NOT NULL AND token = %s
                """
            cur.execute(efficiency_query, (token,))
            visitor_efficiency, = cur.fetchone()
        else:
            is_subscribed = False
            visitor_efficiency = 'Intermediate'

        followers_query = """
            SELECT COUNT(*) FROM subscriptions WHERE following_id = %s
            """
        cur.execute(followers_query, (id,))
        num_followers, = cur.fetchone()

        followings_query = """
            SELECT COUNT(*) FROM subscriptions WHERE follower_id = %s
            """
        cur.execute(followings_query, (id,))
        num_followings, = cur.fetchone()

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
            'is_subscribed': is_subscribed,
            'visitor_efficiency': visitor_efficiency,
            'num_followers': num_followers,
            'num_followings': num_followings,
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 500,
            'error': 'Problem retrieving user profile'
        }

def get_users():
    """
    Get list of all users

    Args: None

    Returns:
        Status 200 - body containing a dictionary of dictionary each containing fields:
            id              (Integer)
            display_name    (String)
        Status 500 - server error (failure to connect to database)
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
    sql_search_query = """select id, display_name from users;"""
    cur.execute(sql_search_query)
    users = cur.fetchall()
    user_list = []
    for u in users:
        dict = {
            "id": u[0],
            "display_name": u[1]
        }
        user_list.append(dict)
    conn.commit()
    cur.close()
    conn.close()
    return {
        'status_code': 200,
        'body': user_list
    }

def user_stats(user_id, token):
    """
    Get user stats

    Args:
        user_id    (Integer): id of user to get stats for

    Returns:
        Status 200 - dictionary of user stats
        Status 400 - failed to fetch user info
        Status 404 - invalid user id or user doesn't exist
        Status 500 - server error (failure to connect to database)
    """
    if not re.match(r'^[0-9]+$', str(user_id)):
        return {
            'status_code': 404,
            'error': 'User with given id does not exist'
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

    try:
        query = "SELECT COUNT(*) FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        if cur.fetchone()[0] == 0:
            raise Exception
    except:
        return {
            'status_code': 404,
            'error': 'User with given id does not exist'
        }

    try:
        # public user info
        query = "SELECT display_name, base64_image FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        display_name, user_image = cur.fetchone()

        query = "SELECT COUNT(*) FROM subscriptions WHERE following_id = %s"
        cur.execute(query, (user_id,))
        num_followers, = cur.fetchone()

        query = "SELECT COUNT(*) FROM subscriptions WHERE follower_id = %s"
        cur.execute(query, (user_id,))
        num_followings, = cur.fetchone()

        query = """
            SELECT COUNT(*) FROM recipes WHERE recipe_status = 'published'
            AND owner_id = %s
            """
        cur.execute(query, (user_id,))
        num_published_recipes, = cur.fetchone()

        query = "SELECT COUNT(*) FROM recipes WHERE owner_id = %s"
        cur.execute(query, (user_id,))
        num_recipes, = cur.fetchone()

        query = """
            SELECT COUNT(*) FROM cookbooks WHERE cookbook_status = 'published'
            AND owner_id = %s
            """
        cur.execute(query, (user_id,))
        num_published_cookbooks, = cur.fetchone()

        query = "SELECT COUNT(*) FROM cookbooks WHERE owner_id = %s"
        cur.execute(query, (user_id,))
        num_cookbooks, = cur.fetchone()

        query = """
            SELECT COUNT(*) FROM cookbooks WHERE cookbook_status = 'published'
            AND owner_id = %s
            """
        cur.execute(query, (user_id,))
        num_published_cookbooks, = cur.fetchone()

        query = """
            SELECT COUNT(DISTINCT c.cookbook_id) FROM cookbooks c
            JOIN cookbook_followers f
            ON (f.cookbook_id = c.cookbook_id)
            WHERE c.owner_id = %s
            """
        cur.execute(query, (user_id,))
        num_cookbooks_followed, = cur.fetchone()

        query = "SELECT COUNT(*) FROM cookbook_followers WHERE follower_id = %s"
        cur.execute(query, (user_id,))
        num_cookbooks_following, = cur.fetchone()

        query = """
            SELECT COUNT(v.*), AVG(v.rating) FROM recipe_reviews v 
            JOIN recipes r ON (r.recipe_id = v.recipe_id)
            WHERE r.owner_id = %s"""
        cur.execute(query, (user_id,))
        reviews_received_result = cur.fetchone()
        reviews_received_count = reviews_received_result[0]
        reviews_received_average = \
            '0.0' if reviews_received_result[1] is None else str(reviews_received_result[1])

        query = "SELECT COUNT(*), AVG(rating) FROM recipe_reviews WHERE user_id = %s"
        cur.execute(query, (user_id,))
        reviews_made_result = cur.fetchone()
        reviews_made_count = reviews_made_result[0]
        reviews_made_average = \
            '0.0' if reviews_made_result[1] is None else str(reviews_made_result[1])

        query = """
            SELECT COUNT(DISTINCT recipe_id) FROM recipe_user_likes
            WHERE user_id = %s
            """
        cur.execute(query, (user_id,))
        reciped_liked_by_user, = cur.fetchone()

        query = """
            SELECT COUNT(DISTINCT l.user_id) FROM recipe_user_likes l
            JOIN recipes r ON (r.recipe_id = l.recipe_id)
            WHERE r.owner_id = %s
            """
        cur.execute(query, (user_id,))
        reciped_liked_by_others, = cur.fetchone()
        
        # check if current user is anonymous or another user requesting private
        # user information
        if token:
            query = "SELECT id FROM users WHERE token = %s"
            cur.execute(query, (str(token),))
            cur_user_id, = cur.fetchone()
        else:
            # not authenticated, assume user_id = -1
            cur_user_id = -1

        stats_data = {
            'status_code': 200,
            'body': {
                'display_name': display_name,
                'user_image': user_image,
                'num_followers': num_followers,
                'num_followings': num_followings,
                'num_published_recipes': num_published_recipes,
                'num_recipes': num_recipes,
                'num_published_cookbooks': num_published_cookbooks,
                'num_cookbooks': num_cookbooks,
                'num_cookbooks_followed': num_cookbooks_followed,
                'num_cookbooks_following': num_cookbooks_following,
                'reviews_received_count': reviews_received_count,
                'reviews_received_average': reviews_received_average,
                'reviews_made_count': reviews_made_count,
                'reviews_made_average': reviews_made_average,
                'reciped_liked_by_user': reciped_liked_by_user,
                'reciped_liked_by_others': reciped_liked_by_others
            }
        }
        if not token or cur_user_id != int(user_id):
            cur.close()
            conn.close()
            return stats_data
            
        # private info only from this point forward
        query = "SELECT COUNT(*) FROM message_room_owners WHERE owner_id = %s"
        cur.execute(query, (user_id,))
        num_message_rooms_owner, = cur.fetchone()

        query = """
            SELECT COUNT(*) FROM message_room_members
            WHERE member_id NOT IN (
                SELECT owner_id FROM message_room_owners WHERE owner_id = %s
            ) AND member_id = %s
            """
        cur.execute(query, (user_id, user_id))
        num_message_rooms_member, = cur.fetchone()


        stats_data['body']['num_message_rooms_owner'] = num_message_rooms_owner
        stats_data['body']['num_message_rooms_member'] = num_message_rooms_member

        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 404,
            'error': 'could not fetch user stats'
        }

    return stats_data
