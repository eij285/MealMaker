from datetime import datetime, timezone, timedelta
import psycopg2
import json
import bcrypt
import jwt
import re

def check_valid_password(password):
    """Password validity checker
    
    """
    special_chars = "`~!@#$%^&*()-_=+;:'“,<.>/?"
    errors = []

    # Check that the password is of suitable length
    if len(password) < 8:
        errors.append("Password is less than 8 characters")

    # Check that the password contains a lower-case character
    lower_chars = [x for x in password if x.islower()]
    if not lower_chars:
        errors.append("Password does not contain a lower-case character")
    
    # Check that the passworde contains an upper-case character
    upper_chars = [x for x in password if x.isupper()]
    if not upper_chars:
        errors.append("Password does not contain an upper-case character")

    # Check that the password contains a decimal digit
    dec_digits = [x for x in password if x.isdecimal()]   
    if not dec_digits:
        errors.append("Password does not contain a decimal digit")

    # Check that the password contains a special character
    special_chars = [x for x in password if x in special_chars]
    if not special_chars:
        errors.append("Password does not contain a special character")

    # If errors are empty (i.e. password is valid)
    if not errors:
        return True, errors
    else:
        return False, errors

def auth_register(display_name, email, password):
    """Registers a new user

    Registers a user by adding them to the database if they were not already
    registered and email and password provided is valid. If so, their login 
    details should be saved (with password hashed using bcrypt) for future
    logins. It should also return a JWT token so that the user can immediately
    begin browsing the product.

    https://zetcode.com/python/bcrypt/

    Args:
        display_name(String): name to be used for displaying
        email       (String): email to be used in future logins
        password    (String): password to be used in future logins

    Returns:
        Status 201
            token:  String
            user: {
                email: String
                password: Byte String
            }
        Status 400
            errors: [String]

    """
    
    # Connect to database
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

    # TODO: Check that the password is valid
    password_valid, errors = check_valid_password(password)
    if not password_valid:
        return {
            'status_code': 400,
            'errors': errors
        }

    # Encrypt password
    encoded_pw = password.encode('utf8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(encoded_pw, salt)

    print(type(hashed_pw))

    # Add user to database
    sql_query = "INSERT INTO users (email, display_name, password) VALUES \
                 (%s, %s, %s) RETURNING id;"
    cur.execute(sql_query, (email, display_name, hashed_pw.decode('utf-8')))

    u_id = cur.fetchone()[0]

    #TODO: Generate JWT token
    key = "SECRET"
    encoded_jwt = jwt.encode(
        {
            'u_id': u_id,
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
        },
        key, algorithm='HS256'
    )

    conn.commit()

    cur.close()
    conn.close()
    
    return {
        'status_code': 200,
        'body': []
    }

def auth_login(email, password):
    """Logins a user
    
    Logins a user and assigns them a new JWT token for the current session.
    Checks that the user login information correctly corresponds to a registered
    user in the database.

    Args:
        email       (String): email being used to login
        password    (String): password being used to login

    Returns:
        Status 200
            token:  String
        Status 400
            errors: [String]
    
    """
    pass

def auth_update_pw(token, password):
    """Updates an authenticated user's password
    
    Updates a user's password after confirming they are a valid authenticated
    user. New password must meet the minimum requirements.
    
    Args:
        token       (String): token of authenticated user
        password    (String): new password to replace old password of
                              authenticated user

        
    Returns:
        Status 200
        Status 400
        Status 401
    
    """

def auth_reset_link(email):
    """Sends a link to reset user's password
    
    Allows a user to reset their password if they forgot it. This function sends
    an email containing a secure link which allows them to reset their password.
    A reset code is generated which is saved on the database, and a url query
    string containing the email and reset code (32 bit hashed) is sent.

    https://stackoverflow.com/questions/15799696/how-to-build-urls-in-python
    
    Args:
        email       (String): email that the reset link will be sent to
        
    Returns:
        Status 200
        Status 400
        
    """
    pass

def auth_reset_pw(password):
    """Updates password from reset link
    
    Args:
        password    (String):
        
    Returns:
        Status 200
        Status 400
        
    """
    pass
    