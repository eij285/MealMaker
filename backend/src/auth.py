import psycopg2

# TODO: This is an incomplete solution to registration
def auth_register(username, email, password):
    """Registers a new user

    Registers a user by adding them to the database if they were not already
    registered and email and password provided is valid. If so, their login 
    details should be saved (with password hashed using bcrypt) for future
    logins. It should also return a JWT token so that the user can immediately
    begin browsing the product.

    https://zetcode.com/python/bcrypt/

    Args:
        username    (String): username to be used in future logins
        email       (String): email to be used in future logins
        password    (String): password to be used in future logins

    Returns:
        Status 201
            token:  String
        Status 400
            errors: [String]

    """
    
    # Connect to database
    try:
        conn = psycopg2.connect("dbname=codechefs-db")
        cur = conn.cursor()
        print(conn)
    except:
        # TODO: Should return relevant error here
        return None

    # Adds user to database
    # TODO: Does not check for valid information
    cur.execute("INSERT INTO Users VALUES ('JohnDoe', 'sample@gmail.com', 'pw')")

    conn.close()
    pass

def auth_login(login, password):
    """Logins a user
    
    Logins a user and assigns them a new JWT token for the current session.
    Checks that the user login information correctly corresponds to a registered
    user in the database.

    Args:
        login       (String): username or email being used to login
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

def auth_reset_pw(email):
    """Resets a user's password
    
    Allows a user to reset their password if they forgot it. This is done by
    sending an email containing a secure link which allows them to reset their
    password. Password must meet the minimum requirements.

    url query string containing email and reset code
    reset code 32 bit hashed
    
    Args:
        email       (String): email that the reset link will be sent to
        
    Returns:
        Status 200
        Status 400
        
    """
    pass
    