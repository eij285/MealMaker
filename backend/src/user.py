import psycopg2
from error import InputError
import re

def check_valid_email(email_str):
    '''
    Check for if the email is valid and conforms to the restrictions
    that define an email address
    '''

    valid = 0
    # pylint: disable=anomalous-backslash-in-string
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # rough explanation, may be useful if changes must be made to tests:
    # starts with at least one "word" character, with optional symbols in the middle/end
    # then an @, again at least one "word" followed by optional symbols
    # then any amount of words separated with "\",".","-"
    # must end with at least one .___ where the word following
    # the dot is 2 or 3 characters in length

    if re.search(regex, email_str):
        valid = 1

    return valid


def user_units(token, unit):
    """Changes users prefered form of measurement

    Checks a registered users prefered form of measurement (metric or imperial). User can then
    Toggle the measurement method into the one that is the opposite of what was already selected
    The default measurement would be metric.

    Args:

    Returns:

    """
    if unit not in {"Imperial", "Metric"}:
        raise InputError("Measurement must be one of: ""Imperial"", ""Metric""")
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

    Returns:

    """
    if efficiency not in {"beginner", "intermediate", "expert"}:
        raise InputError("Efficiency must be one of: ""beginner"", ""intermediate"", ""expert""")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET users.efficiency = %s, WHERE users.token = %s;"""
    input_data = (efficiency, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_name(token, name):
    """Changes users name

    Args:

    Returns:

    """
    if len(name) < 1 or len(name) > 20:
        raise InputError("Name must be between 1 and 20 characters inclusive")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET users.name = %s, WHERE users.token = %s;"""
    input_data = (name, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_surname(token, surname):
    """Changes users surname

    Args:

    Returns:

    """
    if len(surname) < 1 or len(surname) > 20:
        raise InputError("Surname must be between 1 and 20 characters inclusive")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET users.surname = %s, WHERE users.token = %s;"""
    input_data = (surname, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_display_name(token, display_name):
    """Changes users display name

    Args:

    Returns:

    """
    if len(display_name) < 1 or len(display_name) > 30:
        raise InputError("Dsplay name must be between 1 and 20 characters inclusive")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET users.display_name = %s, WHERE users.token = %s;"""
    input_data = (display_name, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_email(token, email):
    """Changes users email

    Args:

    Returns:

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
    sql_update_query = """UPDATE users SET users.email = %s, WHERE users.token = %s;"""
    input_data = (email, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()



def user_update_about_me(token, about_me):
    """Changes users about me

    Args:

    Returns:

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
    sql_update_query = """UPDATE users SET users.about_me = %s, WHERE users.token = %s;"""
    input_data = (about_me, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_country(token, country):
    """Changes users country

    Args:

    Returns:

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
    sql_update_query = """UPDATE users SET users.country = %s, WHERE users.token = %s;"""
    input_data = (country, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_visibility(token, visibility):
    """Changes users visibilty

    Args:

    Returns:

    """
    if visibility not in {"private", "public"}:
        raise InputError("Visibility must be one of: ""private"", ""public""")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET users.visibility = %s, WHERE users.token = %s;"""
    input_data = (visibility, token)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    cur.close()
    conn.close()

def user_update_pronoun(token, pronoun):
    """Changes users visibilty

    Args:

    Returns:

    """
    if len(pronoun) < 1 or len(pronoun) > 20:
        raise InputError("Pronoun must be between 1 and 20 characters inclusive")
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
        cur = conn.cursor()
        print(conn)
    except:
        return {
            'status_code': 500,
            'errors': ['Unable to connect to database']
        }
    sql_update_query = """UPDATE users SET users.pronoun = %s, WHERE users.token = %s;"""
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