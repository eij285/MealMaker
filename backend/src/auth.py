import psycopg2

# TODO: This is an incomplete solution to registration
def auth_register(username, email, password):
    """Registers a new user

    Registers a user by adding them to the database if they were not already
    registered and information provided is valid. Should return a success/fail
    status message, as well as a JWT token so they can immediately start
    browsing.

    Args:
        username (str): 
        email (str):
        password (str):

    Returns:
        ...

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

def auth_login():
    """Logins a user
    
    Logins a user and assigns them a new JWT token for the current session.
    Checks that the user login information correctly corresponds to a registered
    user in the database.

    Args:
        ...

    Returns:
        ...
    
    """
    pass

def auth_update_pw():
    """Updates an authenticated user's password
    
    ...
    
    Args:
        ...
        
    Returns:
        ...
    
    """

def auth_reset_pw():
    """Resets an authenticated user's password
    
    ...
    
    Args:
        ...
        
    Returns:
        ...
        
    """
    pass
    