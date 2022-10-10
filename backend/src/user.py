import psycopg2
# from error import InputError
import re

def user_units(token, unit):
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
    sql_update_query = """UPDATE users SET users.unit = %s, WHERE users.token = %s;"""
    input_data = (unit, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_efficiency(token, efficiency):
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
    if efficiency not in {"beginner", "intermediate", "expert"}:
        return {
            'status_code': 400,
            'error': 'Efficiency must be one of: ""beginner"", ""intermediate"", ""expert""'
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

def user_update_name(token, name):
    """Changes users name

    Args:
        token       (String): token of authenticated user
        name        (String): new name to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if len(name) < 1 or len(name) > 20:
        return {
            'status_code': 400,
            'error': 'Name must be between 1 and 20 characters inclusive'
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
    sql_update_query = """UPDATE users SET name = %s WHERE token = %s;"""
    input_data = (name, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_surname(token, surname):
    """Changes users surname

    Args:
        token       (String): token of authenticated user
        surname     (String): new surname to replace old

        
    Returns:
        Status 200
        Status 400
        Status 401

    """
    if len(surname) < 1 or len(surname) > 20:
        return {
            'status_code': 400,
            'error': 'Surname must be between 1 and 20 characters inclusive'
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
    sql_update_query = """UPDATE users SET surname = %s WHERE token = %s;"""
    input_data = (surname, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

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



def user_update_about_me(token, about_me):
    """Changes users about me

    Args:
        token       (String): token of authenticated user
        about_me    (String): new ebout me to replace old

        
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
    sql_update_query = """UPDATE users SET about_me = %s WHERE token = %s;"""
    input_data = (about_me, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

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
    if len(country) < 1 or len(country) > 20:
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
    if len(pronoun) < 1 or len(pronoun) > 20:
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

"""
def user_update_profile_picture(token):
    """
"""Changes users profile picture

    Args:

    Returns:

"""