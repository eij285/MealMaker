import psycopg2
# from error import InputError
import re

def user_update(token, given_names, surname, display_name, email, about_me, country, visibility, pronoun):
    """updates user details"""
    if email is None or display_name is None:
        return {
            'status_code': 400,
            'error': 'Display name or email fields cannot be empty'
        }
    output = {}
    output["given_names"] = user_update_name(token, given_names)
    output["last_name"] = user_update_surname(token, surname)
    output["display_name"] = user_update_display_name(token, display_name)
    output["email"] = user_update_email(token, email)
    output["about"] = user_update_about_me(token, about_me)
    output["country"] = user_update_country(token, country)
    output["visibility"] = user_update_visibility(token, visibility)
    output["pronoun"] = user_update_pronoun(token, pronoun)
    return output

def user_update_preferences(token, units, efficiency, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free):
    """updates user preferences"""
    output = {}
    output["units"] = user_update_units(token, units)
    output["efficiency"] = user_update_efficiency(token, efficiency)
    output["preferences"] = user_update_preferences_booleans(token, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free, soy_free)
    return output

def user_info(token):
    """retrieves users information for his update page
    """
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    cur.execute("SELECT pronoun, given_names, last_name, display_name, email, country, about, visibility FROM users WHERE token = %s;", (token,))
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
        'visibility': user[0][7]
    }

def user_preferences(token):
    """retrieves users preferences for his update page
    """
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET 
                          breakfast = %d,
                          lunch = %d,
                          dinner = %d,
                          snack = %d,
                          vegetarian = %d,
                          vegan = %d,
                          kosher = %d,
                          halal = %d,
                          dairy_free = %d,
                          gluten_free = %d,
                          nut_free = %d,
                          egg_free = %d,
                          shellfish_free = %d,
                          soy_free = %d
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET unit = %s WHERE token = %s;"""
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
        if len(given_names) < 1 or len(given_names) > 20:
            return {
                'status_code': 400,
                'error': 'given_names must be between 1 and 20 characters inclusive'
            }
        # raise InputError("Name must be between 1 and 20 characters inclusive")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
        if len(last_name) < 1 or len(last_name) > 20:
            return {
                'status_code': 400,
                'error': 'last_name must be between 1 and 20 characters inclusive'
            }
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }

    # Check that the email is not already registered in database
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    if cur.fetchall():
        return {
            'status_code': 400,
            'errors': ['Email has already been registered']
        }
    
    # TODO: Check that email is valid
    email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(email_regex, email):
        return {
            'status_code': 400,
            'errors': ['Email is in invalid format']
        }
    sql_update_query = """UPDATE users SET email = %s, WHERE token = %s;"""
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
                'error': 'Country must be between 1 and 20 characters inclusive'
            }
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET visibility = %s WHERE token = %s;"""
    input_data = (visibility, token)
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
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
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
"""
def user_update_profile_picture(token):
    """
"""Changes users profile picture

    Args:

    Returns:

"""