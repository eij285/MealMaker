from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from config import DB_CONN_STRING, SECRET_KEY, EMAIL_AUTH_ADDR, EMAIL_AUTH_PW
import psycopg2
import bcrypt
import jwt
import re
import urllib
import hashlib
import smtplib
import ssl

def check_valid_password(password):
    """Password validity checker

    Checks the validity of a password based on the following given criteria.
    Password must:
        - be at least 8 characters
        - contain a lower-case character
        - contain an upper-case character
        - contain a decimal digit
        - contain a special character
    Function currently returns just the first one of these conditions that have
    not been satisifed if the password is invalid.

    Args:
        password    (String): password requiring validity check

    Returns:
        Validity    (Boolean): password is valid or not
        Error Msg   (String): reason for password being invalid
    
    """

    special_chars = "`~!@#$%^&*()-_=+;:'“,<.>/?"

    # Check that the password is of suitable length
    if len(password) < 8:
        return False, "Password is less than 8 characters"

    # Check that the password contains a lower-case character
    lower_chars = [x for x in password if x.islower()]
    if not lower_chars:
        return False, "Password does not contain a lower-case character"
    
    # Check that the passworde contains an upper-case character
    upper_chars = [x for x in password if x.isupper()]
    if not upper_chars:
       return False, "Password does not contain an upper-case character"

    # Check that the password contains a decimal digit
    dec_digits = [x for x in password if x.isdecimal()]   
    if not dec_digits:
        return False, "Password does not contain a decimal digit"

    # Check that the password contains a special character
    special_chars = [x for x in password if x in special_chars]
    if not special_chars:
        return False, "Password does not contain a special character"

    return True, ""

def send_email_reset_link(email_to, link):
    """Email sender
    
    Sends email from code.chefs.authenticator@gmail.com containing password
    reset information and reset link. 
    
    Args:
        email_to    (String): email address of the recipient
        link        (String): link to add to email body
    
    Returns:
        Nothing
    
    """

    email_from = EMAIL_AUTH_ADDR

    # TODO: Move this password
    email_from_pw = EMAIL_AUTH_PW

    msg_body = f"You've requested a password reset. If this was not you, " + \
               f"please ignore this email.\r\n\r\n" + \
               f"To reset your password, use link {link}."

    em = EmailMessage()
    em['From'] = email_from
    em['To'] = email_to
    em['Subject'] = "Password reset for Meal Maker"
    em.set_content(msg_body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_from, email_from_pw)
        smtp.sendmail(email_from, email_to, em.as_string())

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
            error: String

    """
    
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Check that the email is not already registered in database
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    if cur.fetchall():
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

    # TODO: Check that the password is valid
    password_valid, errors = check_valid_password(password)
    if not password_valid:
        return {
            'status_code': 400,
            'error': errors
        }

    # Encrypt password
    encoded_pw = password.encode('utf8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(encoded_pw, salt)

    # Add user to database
    sql_query = "INSERT INTO users (email, display_name, password) VALUES \
                 (%s, %s, %s) RETURNING id;"
    cur.execute(sql_query, (email, display_name, hashed_pw.decode('utf-8')))

    u_id = cur.fetchone()[0]

    # Create JWT token for old pyjwt ver 1.7
    try:
        encoded_jwt = jwt.encode(
            {
                'u_id': u_id,
                'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
            },
            SECRET_KEY, algorithm='HS256'
        ).decode('utf-8')
    
    # Create JWT token for new pyjwt ver 2.5
    except AttributeError:
        encoded_jwt = jwt.encode(
            {
                'u_id': u_id,
                'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
            },
            SECRET_KEY, algorithm='HS256'
        )

    # Add user's token to database
    sql_query = "UPDATE users SET token = %s WHERE id = %s;"
    cur.execute(sql_query, (encoded_jwt, str(u_id)))

    conn.commit()
    cur.close()
    conn.close()
    
    return {
        'status_code': 200,
        'body': {
            'token': encoded_jwt
        }
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
   
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # Check that email has been registered in database and if so obtain password
    cur.execute("SELECT password FROM users WHERE email = %s;", (email,))

    sql_result = cur.fetchall()
    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Email has not been registered'
        }
    
    # Check that the password matches
    stored_pw, = sql_result[0]

    if not bcrypt.checkpw(password.encode('utf-8'), stored_pw.encode('utf-8')):
        return {
            'status_code': 400,
            'error': 'Incorrect password'
        }

    # TODO: Check that the user is not already logged in
    cur.execute("SELECT id, token FROM users WHERE email = %s;", (email,))
    u_id, token = cur.fetchone()
    if token:
        return {
            'status_code': 400,
            'error': 'User already logged in'
        }

    # Create JWT token for old pyjwt ver 1.7
    try:
        encoded_jwt = jwt.encode(
            {
                'u_id': u_id,
                'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
            },
            SECRET_KEY, algorithm='HS256'
        ).decode('utf-8')
    
    # Create JWT token for new pyjwt ver 2.5
    except AttributeError:
        encoded_jwt = jwt.encode(
            {
                'u_id': u_id,
                'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
            },
            SECRET_KEY, algorithm='HS256'
        )

    # Add new token to database
    sql_query = "UPDATE users SET token = %s WHERE id = %s;"
    cur.execute(sql_query, (encoded_jwt, str(u_id)))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'token': encoded_jwt
        }
    }
    
def auth_logout(token):
    """Logs out a user
    
    Log out a user and remove their JWT token for the current session.

    Args:
        token       (String): token of user logging out

    Returns:
        Status 200
            token:  String
        Status 400
            errors: [String]
    
    """
    
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # Check that the token corresponds to an active user
    cur.execute("SELECT token FROM users WHERE token = %s;", (token,))

    sql_result = cur.fetchall()
    if not sql_result:
        return {
            'status_code': 401,
            'error': 'Token does not correspond to any active user'
        }

    # Remove token from database
    cur.execute("UPDATE users SET token = NULL WHERE token = %s;", (token,))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {

        }
    }

def auth_logout_everywhere(email, password):
    """Logs out a user everywhere
    
    Log out a user and remove their JWT token from the database. This may be
    necessary where someone has gained unauthorised access to the user's login
    or the user has lost their token as a result of clearing their browser
    cache.

    Args:
        email       (String): email of user logging out
        password    (String): password of user logging out

    Returns:
        Status 200
            token:  String
        Status 400
            errors: [String]
    
    """
    
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # Check that email has been registered in database and if so obtain password
    cur.execute("SELECT id, password FROM users WHERE email = %s;", (email,))

    # Check password if account exists for given email, password combination
    sql_result = cur.fetchone()
    u_id, stored_pw = (None, None) if not sql_result else sql_result
    if not stored_pw or not bcrypt.checkpw(password.encode('utf-8'), \
        stored_pw.encode('utf-8')):
        return {
            'status_code': 400,
            'error': 'Account does not exist'
        }

    # Add new token to database
    sql_query = "UPDATE users SET token = NULL WHERE id = %s;"
    cur.execute(sql_query, (str(u_id),))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {

        }
    }

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
    
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # TODO: Verify token

    # Check that the password is valid
    password_valid, errors = check_valid_password(password)
    if not password_valid:
        return {
            'status_code': 400,
            'error': errors
        }

    # Encrypt password
    encoded_pw = password.encode('utf8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(encoded_pw, salt)

    # Update user's password in database
    sql_query = "UPDATE users SET password = %s WHERE token = %s;"
    cur.execute(sql_query, (hashed_pw.decode('utf-8'), token))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'success': True
        }
    }

def auth_reset_link(email, base_url):
    """Sends a link to reset user's password
    
    Allows a user to reset their password if they forgot it. This function sends
    an email containing a secure link which allows them to reset their password.
    A reset code is generated which is saved on the database, and a url query
    string containing the email and reset code (32 bit hashed) is sent.

    https://stackoverflow.com/questions/15799696/how-to-build-urls-in-python
    http://localhost:3000/password-reset?email=someone@gmail.com&code=F05313695A0E6987111344F3D15F01E4
    
    Args:
        email       (String): email that the reset link will be sent to
        base_url    (String): the base url without query string appended
        
    Returns:
        Status 200
        Status 400
        
    """

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # Check that email corresponds to a user in the database
    sql_query = "SELECT id, display_name FROM users WHERE email = %s;"
    cur.execute(sql_query, (email,))

    sql_result = cur.fetchall()
    if not sql_result:
        return {
            'status_code': 200,
            'body': {
                'message': '(shh, this failed) Link sent to email provided'
            }
        }
    
    # Generate url for password reset
    code = hashlib.md5(str(sql_result[0]).encode('utf-8')).hexdigest()
    params = {'email': email, 'code': code}
    url = base_url + urllib.parse.urlencode(params)

    # Send email
    send_email_reset_link(email, url)

    # TODO: Update password_reset with code
    sql_query = "UPDATE users SET password_reset = %s WHERE email = %s;"
    cur.execute(sql_query, (code, email))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'message': 'Link sent to email provided'
        }
    }

def auth_reset_pw(email, code, password):
    """Updates password from reset link
    
    Args:
        email       (String):
        code        (String):
        password    (String):
        
    Returns:
        Status 200
        Status 400
        
    """

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # TODO: Check the reset-code of user matches
    cur.execute("SELECT password_reset FROM users WHERE email = %s;", (email,))

    sql_result = cur.fetchall()
    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Email does not match any user on server'
        }

    code_db, = sql_result[0]

    if code_db != code:
        return {
            'status_code': 400,
            'error': 'Code does not match code stored on server'
        }

    # Check that the password is valid
    password_valid, errors = check_valid_password(password)
    if not password_valid:
        return {
            'status_code': 400,
            'error': errors
        }

    # Encrypt password
    encoded_pw = password.encode('utf8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(encoded_pw, salt)

    # Update user's password in database
    sql_query = "UPDATE users SET password = %s WHERE email = %s;"
    cur.execute(sql_query, (hashed_pw.decode('utf-8'), email))

    conn.commit()
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'success': True
        }
    }
