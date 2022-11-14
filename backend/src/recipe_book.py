import psycopg2
from backend_helper import connect, verify_token
from config import DB_CONN_STRING
from recipe import recipe_details
from notifications import notification_auth_send

def cookbook_create(name, status, description, token):
    """Create a new cookbook (token must be valid)
    
    Args:
        name            (String): cookbook name
        description     (String): cookbook description
        cookbook_status (String): 'draft' or 'published'
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - cookbook created successfully, returning body (dict)
                     containing cookbook_id (Integer)
        Status 400 - failure to create cookbook
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
    
    query = ("SELECT visibility FROM users WHERE token = %s")
    cur.execute(query, (str(token),))
    visibility, = cur.fetchone()
    if visibility == 'private':
        return {
            'status_code': 400,
            'error': "private users cannot create cookbooks"
        }
    
    # Add new cookbook to system
    try:
        query = ("""
            INSERT INTO
                cookbooks(owner_id, cookbook_name, cookbook_description, cookbook_status)
            VALUES
                (%s, %s, %s, %s)
            RETURNING
                cookbook_id
            """)
        cur.execute(query, (owner_id, name, description, status,))
        conn.commit()
        cookbook_id, = cur.fetchone()
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

def cookbook_publish(cookbook_id, publish_status, token):
    """Publish or unpublish cookbook (token must be valid)
    
    Args:
        cookbook_id     (Integer): the cookbook id to publish/unpublish
        publish_status  (String): the new value - 'published' or 'draft'
        token           (String): token of authenticated user
        
    Returns:
        Status 201 - success
        Status 400 - failure to publish or unpublish cookbook
        Status 401 - invalid or no token
        Status 404 - cannot find cookbook
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
        query = ("""
            SELECT COUNT(c.*) FROM cookbooks c
            JOIN users u ON (c.owner_id = u.id)
            WHERE c.cookbook_id = %s AND u.token = %s
            """)
        cur.execute(query, (cookbook_id, token))
        cookbook_cnt, = cur.fetchone()
        if cookbook_cnt < 1:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 404,
            'error': "cannot find cookbook owned by user"
        }
    # Publish/Unpublish cookbook
    try:
        query = ("""
            UPDATE cookbooks
            SET cookbook_status = %s
            WHERE cookbook_id = %s
            """)
        cur.execute(query, (publish_status, cookbook_id))
        conn.commit()
        
        # Close connection
        conn.close()
        cur.close()
    except:
        # Close connection
        conn.close()
        cur.close()
        return {
            'status_code': 400,
            'error': f'cookbook could not set to {publish_status}'
        }
    return {
        'status_code': 200,
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
                cookbook_description   (String)
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
        query = ("""SELECT cookbook_name, cookbook_photo, cookbook_status, cookbook_description
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
            'cookbook_description': cookbook[3],
        }
    }

def cookbook_all_recipes(cookbook_id, token):
    """
    Retrieves recipes summary for all recipes in a given cookbook
    Note: this is only available to the cookbook owner

    Args:
        cookbook_id   (Integer): the cookbook id to fetch data for
        token         (String): token of authenticated user
        
    Returns:
        Status 200 - success
            body    (dict of atomic values)
                recipe_id       (Integer)
                recipe_name     (String)
                recipe_photo    (String)
                recipe_status   (String)
                cuisine         (String)
                review_cnt      (Integer)
                rating_avg      (String): JSON cannot contain decimal
                likes_cnt       (Integer)
                

        Status 400 - failure to find cookbook id
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
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
        query = ("SELECT COUNT(*) FROM cookbooks WHERE cookbook_id = %s AND owner_id = %s")
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        cookbook_count, = cur.fetchone()
        if cookbook_count == 0:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find cookbook owned by user"
        }

    try:
        query = ("""
            SELECT r.recipe_id, r.recipe_name, r.recipe_photo, r.recipe_status,
            r.cuisine, s.review_cnt, s.rating_avg, v.likes_cnt
            FROM recipes r 
            INNER JOIN cookbook_recipes cr ON (cr.recipe_id = r.recipe_id)
            INNER JOIN cookbooks c ON (c.cookbook_id = cr.cookbook_id)
            LEFT OUTER JOIN (
                SELECT COUNT(*) review_cnt, AVG(rating) rating_avg, recipe_id
                FROM recipe_reviews GROUP BY recipe_id
            ) s ON (r.recipe_id = s.recipe_id)
            LEFT OUTER JOIN (
				SELECT COUNT(*) likes_cnt, recipe_id
				FROM recipe_user_likes GROUP BY recipe_id
			) v ON (r.recipe_id = v.recipe_id)
            WHERE c.cookbook_id = %s AND c.owner_id = %s
            """)
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        output = cur.fetchall()
        recipes_list = []
        for recipe in output:
            # need average but json in flask doesn't like decimal data
            recipe_id, recipe_name, recipe_photo, recipe_status, cuisine, \
                tmp_review_cnt, tmp_rating_avg, tmp_likes_cnt = recipe
            review_cnt = tmp_review_cnt if tmp_review_cnt is not None else 0
            likes_cnt = tmp_likes_cnt if tmp_likes_cnt is not None else 0
            if tmp_rating_avg is None:
                rating_avg = '0.0'
            else:
                rating_avg = f'{tmp_rating_avg:.1f}'
            recipes_list.append({
                'recipe_id': recipe_id,
                'recipe_name': recipe_name,
                'recipe_photo': recipe_photo,
                'recipe_status': recipe_status,
                'cuisine': cuisine,
                'review_cnt': review_cnt,
                'rating_avg': rating_avg,
                'likes_cnt': likes_cnt
            })
    except:
        return {
            'status_code': 400,
            'error': "cannot find cookbook recipes"
        }
    return {
        'status_code': 200,
        'recipes': recipes_list
    }

def cookbook_update(data, token):
    """
    Update the given cookbook

    Args:
        data    (dict of atomic values and collections): values to update
                cookbook_name         (String)
                cookbook_photo        (String)
                cookbook_description   (String)
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
        cookbook_description = data['cookbook_description']
        params = (cookbook_name, cookbook_photo, cookbook_status, cookbook_description,\
            cookbook_id)

        query = ("""
            UPDATE cookbooks
            SET cookbook_name = %s, cookbook_photo = %s, cookbook_status = %s, cookbook_description = %s WHERE cookbook_id = %s
            """)
        cur.execute(query, params)
        conn.commit()
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 200
        }
        
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
    
    # unfollow all cookbook followers when deleted
    sql_delete_query = ("""
        DELETE FROM cookbook_followers WHERE cookbook_id = %s
        """)
    cur.execute(sql_delete_query, (str(cookbook_id),))
    conn.commit()
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
                        cookbook_id         (Integer)
                        cookbook_name       (String)
                        cookbook_photo      (String)
                        cookbook_description (String)
                        cookbook_status     (String)

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
            SELECT cookbook_id, cookbook_name, cookbook_photo, cookbook_status, cookbook_description
            FROM cookbooks
            WHERE owner_id = %s
            """)
        cur.execute(query, (owner_id,))
        output = cur.fetchall()
        cookbooks_list = []
        for cookbook in output:
            # need average but json in flask doesn't like decimal data
            cookbook_id, cookbook_name, cookbook_photo, cookbook_status, cookbook_description = cookbook
            cookbooks_list.append({
                'cookbook_id': cookbook_id,
                'cookbook_name': cookbook_name,
                'cookbook_photo': cookbook_photo,
                'cookbook_status': cookbook_status,
                'cookbook_description': cookbook_description,
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
                        cookbook_description   (String)

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
            SELECT cookbook_id, cookbook_name, cookbook_photo, cookbook_description
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
                'cookbook_photo': cookbook[2],
                'cookbook_description': cookbook[3],
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
        token         (String): token of authenticated user
    Returns:
        Status 200 - success
            body    (dict of atomic values and lists)
                cookbook_name         (String)
                cookbook_photo        (String)
                cookbook_status       (String)
                cookbook_description  (String)
                author_id             (Integer)
                author_display_name   (String)
                author_image          (String)
                is_owner              (Boolean)
                is_following          (Boolean)
                recipes               (list of dictionaries)

        Status 400 - failure to find cookbook id
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
        if token:
            user_query = ("SELECT id FROM users WHERE token = %s")
            cur.execute(user_query, (str(token),))
            user_id, = cur.fetchone()
        else:
            user_id = -1
        
        query = ("""SELECT c.cookbook_name, c.cookbook_photo, c.cookbook_status,
            c.owner_id, c.cookbook_id, c.cookbook_description, u.display_name,
            u.base64_image
            FROM cookbooks c JOIN users u ON (u.id = c.owner_id)
            WHERE cookbook_id = %s AND
            (cookbook_status = 'published' OR owner_id = %s)""")
        cur.execute(query, (str(cookbook_id), str(user_id)))
        cookbook = cur.fetchone()
        if not cookbook:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot view private cookbook unless owner"
        }
    
    try:
        is_owner = user_id == cookbook[3]
        subs_query = """
            SELECT r.recipe_id FROM cookbook_recipes c
            JOIN recipes r ON c.recipe_id = r.recipe_id
            WHERE c.cookbook_id = %s
            """
        cur.execute(subs_query, (cookbook[4],))
        recipes = cur.fetchall()
        recipe_list = []
        for r in recipes:
            recipe_list.append(recipe_details(r[0], token))
        # determine if cookbook is followed by authenticated user to enable
        # follow and unfollow function on cookbook page
        if user_id >= 0 and not is_owner:
            query = ("""
                SELECT COUNT(*) FROM cookbook_followers
                WHERE cookbook_id = %s AND follower_id = %s
                """)
            cur.execute(query, (cookbook[4], str(user_id)))
            is_following = cur.fetchone()[0] > 0
        else:
            is_following = False
        cur.close()
        conn.close()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to fetch cookbook recipes"
        }
    
    return {
        'status_code': 200,
        'body': {
            'cookbook_name': cookbook[0],
            'cookbook_photo': cookbook[1],
            'cookbook_status': cookbook[2],
            'cookbook_description': cookbook[5],
            'author_id': cookbook[3],
            'author_display_name': cookbook[6],
            'author_image': cookbook[7],
            'is_owner': is_owner,
            'is_following': is_following,
            'recipes': recipe_list
        }
    }

def cookbook_subscribe(token, subscribe_to):
    """subscribe to a cookbook (token must be valid)
    
    Args:
        token           (String): token of authenticated user
        subscribe_to    (Integer): id of cookbook u are subscribing to
        
    Returns:
        Status 200 - cookbook subscribed to successfully
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
        sql_search_query = """SELECT cookbook_status FROM cookbooks WHERE cookbook_id = %s"""
        cur.execute(sql_search_query, (subscribe_to,))
        visibility, = cur.fetchone()
        if visibility == "draft":
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
            SELECT COUNT(*) FROM cookbook_followers
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
            INSERT INTO cookbook_followers (cookbook_id, follower_id)
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
    """unsubscribe to a cookbook (token must be valid)
    
    Args:
        token             (String): token of authenticated user
        unsubscribe_to    (Integer): id of cookbook u are unsubscribing to
        
    Returns:
        Status 200 - cookbook unsubscribed to successfully
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
            SELECT COUNT(*) FROM cookbook_followers
            WHERE cookbook_id = %s AND follower_id = %s 
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
            WHERE cookbook_id = %s and follower_id = %s
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

def cookbook_add_recipe(token, cookbook_id, recipe_id):
    """adds a recipe to a cookbook (token must be valid) and notifys all subscribers with a message
    
    Args:
        token           (String): token of authenticated user
        cookbook_id     (Integer): id of cookbook u are adding recipe to
        recipe_id       (Integer): id of recipe that is being added
        
    Returns:
        Status 200 - recipe added to cookbook successfully
        Status 400 - recipe already in cookbook
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
        query = ("SELECT COUNT(*) FROM cookbooks WHERE cookbook_id = %s AND owner_id = %s")
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        cookbook_count, = cur.fetchone()
        if cookbook_count == 0:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find cookbook owned by user"
        }
    query = ("SELECT COUNT(*) FROM cookbook_recipes WHERE cookbook_id = %s AND recipe_id = %s")
    cur.execute(query, (str(cookbook_id), str(recipe_id)))
    duplicates, = cur.fetchone()
    if duplicates > 0:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "recipe already in cookbook"
        }
    sql_insert_query = """
        INSERT INTO cookbook_recipes (cookbook_id, recipe_id)
        VALUES (%s, %s)
        """
    input_data = (cookbook_id, recipe_id)
    cur.execute(sql_insert_query, input_data)
    conn.commit()

    query = ("SELECT follower_id FROM cookbook_followers WHERE cookbook_id = %s")
    cur.execute(query, (str(cookbook_id),))
    followers = cur.fetchall()
    # notify all followers
    query = ("SELECT cookbook_name FROM cookbooks WHERE cookbook_id = %s")
    cur.execute(query, (str(cookbook_id),))
    name, = cur.fetchone()
    update_msg = f'A recipe has been added to cookbook: {name}!'
    for u in followers:
        notification_auth_send(u[0], update_msg, token)

    cur.close()
    conn.close()
    return {
        'status_code': 200
    }

def cookbook_remove_recipe(token, cookbook_id, recipe_id):
    """removess a recipe to a cookbook (token must be valid) and notifys all subscribers with a message
    
    Args:
        token           (String): token of authenticated user
        cookbook_id     (Integer): id of cookbook u are removing recipe from
        recipe_id       (Integer): id of recipe that is being removed
        
    Returns:
        Status 200 - recipe removed from cookbook successfully
        Status 400 - recipe not already in cookbook
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
        query = ("SELECT COUNT(*) FROM cookbooks WHERE cookbook_id = %s AND owner_id = %s")
        cur.execute(query, (str(cookbook_id), str(owner_id)))
        cookbook_count, = cur.fetchone()
        if cookbook_count == 0:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find cookbook owned by user"
        }
    query = ("SELECT COUNT(*) FROM cookbook_recipes WHERE cookbook_id = %s AND recipe_id = %s")
    cur.execute(query, (str(cookbook_id), str(recipe_id)))
    duplicates, = cur.fetchone()
    if duplicates < 1:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "recipe not in cookbook"
        }
    sql_delete_query = """
        DELETE FROM cookbook_recipes
        WHERE cookbook_id = %s and recipe_id = %s
        """
    input_data = (cookbook_id, recipe_id)
    cur.execute(sql_delete_query, input_data)
    conn.commit()

    query = ("SELECT follower_id FROM cookbook_followers WHERE cookbook_id = %s")
    cur.execute(query, (str(cookbook_id),))
    followers = cur.fetchall()
    # notify all followers
    query = ("SELECT cookbook_name FROM cookbooks WHERE cookbook_id = %s")
    cur.execute(query, (str(cookbook_id),))
    name, = cur.fetchone()
    update_msg = f'A recipe has been removed from cookbook: {name}!'
    for u in followers:
        notification_auth_send(u[0], update_msg, token)

    cur.close()
    conn.close()
    return {
        'status_code': 200
    }
