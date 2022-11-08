import psycopg2
from backend_helper import connect, verify_token
from config import DB_CONN_STRING
from recipe import recipe_details
def book_create(name, status, token):
    """Create a new recipe (token must be valid)
    
    Args:
        name            (String): recipe name
        description     (String): recipe description
        servings        (Integer): number of servings
        recipe_status   (String): 'draft' or 'published'
        token           (String): token of authenticated user
        
    Returns:
        Status 201 - recipe created successfully, returning body (dict)
                     containing recipe_id (Integer)
        Status 400 - failure to create recipe
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }
    # Add new recipe to system
    try:
        query = ("""
            INSERT INTO
                cookbooks(owner_id, cookbook_name, cookbook_status)
            VALUES
                (%s, %s, %s, %s, %s)
            RETURNING
                recipe_id
            """)
        cur.execute(query, (owner_id, name, status,))
        conn.commit()
        cookbook_id = cur.fetchone()[0]
        # Close connection
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to create recipe"
        }
    return {
        'status_code': 201,
        'body': {
            'cookbook_id': cookbook_id
        }
    }

def publish_cookbook(cookbook_id, publish):
    
    # Start connection to database
    connection = connect()
    cur = connection.cursor()
    
    # Publish recipe
    try:
        command = ("""
            UPDATE cookbooks
            SET cookbook_status = %s
            WHERE cookbook_id = %s
            """)
        cur.execute(command, (publish, cookbook_id,))
        connection.commit()
        
        # Close connection
        connection.close()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        cur.close()
        return {
            'status_code': 400,
            'error': 'cookbook could not be published'
        }
    return {
        'status_code': 200
    }

def cookbook_edit(cookbook_id, token):
    """
    Retrieves the information from the database for the cookbook to edit

    Args:
        cookbook_id   (Integer): the cookbook id to fetch data for
        token       (String): token of authenticated user
        
    Returns:
        Status 200 - success
            body    (dict of atomic values and lists)
                cookbook_name         (String)
                cookbook_photo        (String)
                cookbook_status       (String)

        Status 400 - failure to find cookbook id
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }

    try:
        query = ("""SELECT cookbook_name, cookbook_photo, cookbook_status
            FROM cookbooks WHERE cookbook_id = %s AND owner_id = %s""")
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        cookbook = cur.fetchone()
        if not cookbook:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find cookbook id"
        }
    cur.close()
    conn.close()
    
    return {
        'status_code': 200,
        'body': {
            'cookbook_name': cookbook[0],
            'cookbook_photo': cookbook[1],
            'cookbook_status': cookbook[2],
        }
    }
def cookbook_update(data, token):
    """
    Update the given cookbook

    Args:
        data    (dict of atomic values and collections): values to update
                cookbook_name         (String)
                cookbook_photo        (String)
                cookbook_status       (String)
        token   (String): token of authenticated user
        
    Returns:
        Status 200 - success
        Status 400 - failure to update cookbook
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }
    
    try:
        cookbook_id = data['cookbook_id']
        query = ("SELECT COUNT(*) FROM cookbooks WHERE cookbook_id = %s AND owner_id = %s")
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        if not cur.fetchone():
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find cookbook owned by user"
        }
    
    # Update recipe
    try:
        cookbook_name = data['cookbook_name']
        cookbook_photo = data['cookbook_photo']
        cookbook_status = data['cookbook_status']

        params = (cookbook_name, cookbook_photo, cookbook_status,\
            cookbook_id)

        query = ("""
            UPDATE cookbooks
            SET cookbook_name = %s, cookbook_photo = %s, cookbook_status = %s WHERE recipe_id = %s
            """)
        cur.execute(query, params)
        conn.commit()
        # Close connection
        cur.close()
        conn.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': None
        }

def cookbook_delete(cookbook_id, token):
    """
    Delete cookbook with given id (only cookbook owner permitted to do that)

    Args:
        cookbook_id     (Integer): the cookbook to delete
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - cookbook deleted successfully
                body containing dictionary with deleted cookbook_id (Integer)

        Status 400 - failure to delete cookbook
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }

    # no need to handle deleting child records that are handled by
    # delete cascade
    try:
        query = ("""
            DELETE FROM cookbooks WHERE cookbook_id = %s AND owner_id = %s
            RETURNING cookbook_id
            """)
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        conn.commit()
        deleted_cookbook_id, = cur.fetchone()
        if cookbook_id != deleted_cookbook_id:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to delete specified"
        }
    cur.close()
    conn.close()

    return {
        'status_code': 200,
        'body': {
            'cookbook_id': deleted_cookbook_id
        }
    }

def cookbook_fetch_own(token):
    """
    Fetch own cookbook (private, accessible only by cookbook owner)

    Args:
        token   (String): token of authenticated user
        
    Returns:
        Status 200 - successful return of user's recipes
                body    (list of dict)
                        cookbook_id       (Integer)
                        cookbook_name     (String)
                        cookbook_photo    (String)
                        cookbook_status   (String)

        Status 400 - failure to fetch cookbook
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }

    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    try:
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }
    
    try:
        query = ("""
            SELECT cookbook_id, cookbook_name, cookbook_photo, cookbook_status
            FROM cookbooks
            WHERE owner_id = %s
            """)
        cur.execute(query, (owner_id,))
        output = cur.fetchall()
        cookbooks_list = []
        for cookbook in output:
            # need average but json in flask doesn't like decimal data
            cookbook_id, cookbook_name, cookbook_photo, cookbook_status = cookbook
            cookbooks_list.append({
                'cookbook_id': cookbook_id,
                'cookbook_name': cookbook_name,
                'cookbook_photo': cookbook_photo,
                'cookbook_status': cookbook_status,
            })
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code':400,
            'error': 'could not fetch recipes'
        }
    return {
        'status_code':200,
        'body': cookbooks_list
    }

def cookbooks_user_published(user_id):
    """
    Fetch cookbooks for user id (public, accessible to everyone)

    Args:
        user_id     (Integer): user id to fetch published cookbooks for
        
    Returns:
        Status 200 - successful return of user's published cookbooks
                cookbooks (list of dict)
                        cookbook_id           (Integer)
                        cookbook_name         (String)
                        cookbook_photo        (String)

        Status 400 - failure to fetch cookbook
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        query = "SELECT COUNT(*) FROM users WHERE id = %s"
        cur.execute(query, (str(user_id),))
        if cur.fetchone()[0] == 0:
            raise Exception
        
        query = ("""
            SELECT cookbook_id, cookbook_name, cookbook_photo
            WHERE owner_id = %s AND cookbook_status = 'published'
            """)
        cur.execute(query, (user_id,))
        output = cur.fetchall()
        cookbook_list = []
        for cookbook in output:
            # need average but json in flask doesn't like decimal data
            cookbook_list.append({
                'cookbook_id': cookbook[0],
                'cookbook_name': cookbook[1],
                'cookbook_photo': cookbook[2]
            })
        cur.close()
        conn.close()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code':400,
            'error': 'could not fetch cookbooks'
        }
    return {
        'status_code':200,
        'cookbooks': cookbook_list
    }

def cookbook_view(cookbook_id, token):
    """
    Retrieves the information from the database for the cookbook and contained recipes

    Args:
        cookbook_id   (Integer): the cookbook id to fetch data for
        token       (String): token of authenticated user
        
    Returns:
        Status 200 - success
            body    (dict of atomic values and lists)
                cookbook_name         (String)
                cookbook_photo        (String)
                cookbook_status       (String)

        Status 400 - failure to find cookbook id
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        user_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }

    try:
        query = ("""SELECT cookbook_name, cookbook_photo, cookbook_status, owner_id, cookbook_id
            FROM cookbooks WHERE cookbook_id = %s AND cookbook_status = %s""")
        cur.execute(query, (str(cookbook_id), 'published'))
        cookbook = cur.fetchone()
        if not cookbook or (cookbook[3] is not user_id):
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot view private cookbook unless owner"
        }
    
    cur.close()
    conn.close()
    subs_query = """
        SELECT r.recipe_id FROM cookbook_recipes c
        JOIN recipes r ON c.recipe_id = r.recipe_id
        WHERE c.cookbook_id = %s
        """
    cur.execute(subs_query, (token, cookbook[5]))
    recipes = cur.fetchall()
    recipe_list = []
    for r in recipes:
        recipe_list.append(recipe_details(r[0], token))
    return {
        'status_code': 200,
        'body': {
            'cookbook_name': cookbook[0],
            'cookbook_photo': cookbook[1],
            'cookbook_status': cookbook[2],
            'recipes': recipe_list
        }
    }

def cookbook_subscribe(token, subscribe_to):
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        sql_search_query = """SELECT cookbook_status FROM cookbooks WHERE cookbook_id = %s"""
        cur.execute(sql_search_query, (subscribe_to,))
        visibility, = cur.fetchone()
        if visibility is "draft":
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'Cannot subscribe to a private cookbook'
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
            SELECT COUNT(*) FROM cookbook_followers cf
            WHERE cookbook_id = %s AND follower_id = %s 
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
            INSERT INTO cookbook_followers (following_id, follower_id)
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
            'error': 'Problem subscribing to cookbook'
        }
    return {
        'status_code': 200
    }

def cookbook_unsubscribe(token, unsubscribe_to):
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
            SELECT COUNT(*) FROM cookbook_followers cf
            WHERE following_id = %s AND follower_id = %s 
            """
        cur.execute(sql_search_query, (unsubscribe_to, u_id))
        subscribed, = cur.fetchone()
        if subscribed == 0:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'not currently subscribed to cookbook'
            }
        sql_delete_query = """
            DELETE FROM cookbook_followers
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
            'error': 'Problem unsubscribing from cookbook'
        }
    return {
        'status_code': 200
    }