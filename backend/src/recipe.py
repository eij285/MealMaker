import psycopg2
from backend_helper import connect, verify_token
from config import DB_CONN_STRING
   
# def create_recipe_table(connection):
#     cur = connection.cursor()
#     command = ("""
#         CREATE TABLE recipes(
#             recipe_id SERIAL PRIMARY KEY,
#             owner_id INTEGER,
#             recipe_name VARCHAR(255) NOT NULL,
#             recipe_description VARCHAR(255) NOT NULL,
#             methods VARCHAR(255) NOT NULL,
#             is_public BOOLEAN NOT NULL DEFAULT FALSE,
#             recipe_method INTEGER
#         )"""
#     )
#     try:
#         cur.execute(command)
#         connection.commit()
#         return {
#             'status_code': 200
#         }
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#         return {
#             'status_code': 400
#         }
    

def recipe_create(name, description, servings, recipe_status, token):
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
                recipes(owner_id, recipe_name, recipe_description, servings, recipe_status)
            VALUES
                (%s, %s, %s, %s, %s)
            RETURNING
                recipe_id
            """)
        cur.execute(query, (owner_id, name, description, servings, recipe_status,))
        conn.commit()
        recipe_id = cur.fetchone()[0]
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 201,
            'body': {
                'recipe_id': recipe_id
            }
        }
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to create recipe"
        }


def publish_recipe(recipe_id, publish):
    
    # Start connection to database
    connection = connect()
    cur = connection.cursor()
    
    # Publish recipe
    try:
        command = ("""
            UPDATE recipe
            SET recipe_status = %s
            WHERE recipe_id = %s
            """)
        cur.execute(command, (publish, recipe_id,))
        connection.commit()
        
        # Close connection
        connection.close()
        cur.close()
        return {
            'status_code': 200
        }
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        cur.close()
        return {
            'status_code': 400,
            'error': None
        }

def recipe_fetch_ingredients(recipe_id):
    """
    Update ingredients for a given recipe (this function must only be used
    withing this module)
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        query = ("""SELECT ingredient_id, ingredient_name, quantity, unit
            FROM recipe_ingredients WHERE recipe_id = %s""")
        cur.execute(query, (str(recipe_id),))
        output = cur.fetchall()
        ingredients_list = []
        for ingredient in output:
            ingredients_list.append({
                'ingredient_id': ingredient[0],
                'ingredient_name': ingredient[1],
                'quantity': ingredient[2],
                'unit': ingredient[3]
            })
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        raise Exception
    return ingredients_list


def recipe_edit(recipe_id, token):
    """
    Retrieves the information from the database for the recipe to edit
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
        query = ("""SELECT recipe_name, recipe_description, recipe_photo,
            recipe_status, recipe_method, created_on, edited_on,
            preparation_hours, preparation_minutes, servings, energy, protein,
            carbohydrates, fats, cuisine, breakfast, lunch, dinner, snack,
            vegetarian, vegan, kosher, halal, dairy_free, gluten_free, nut_free,
            egg_free, shellfish_free, soy_free
            FROM recipes WHERE recipe_id = %s AND owner_id = %s""")
        cur.execute(query, (str(recipe_id), str(owner_id)))
        recipe = cur.fetchone()
        if not recipe:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find recipe id"
        }
    cur.close()
    conn.close()

    try:
        ingredients_list = recipe_fetch_ingredients(recipe_id)
        
    except:
        # Close connection
        return {
            'status_code': 400,
            'error': "cannot find ingredients"
        }
    
    return {
        'status_code': 200,
        'body': {
            'recipe_name': recipe[0],
            'recipe_description': recipe[1],
            'recipe_photo': recipe[2],
            'recipe_status': recipe[3],
            'recipe_method': recipe[4],
            'created_on': str(recipe[5]),
            'edited_on': str(recipe[6]),
            'preparation_hours': recipe[7],
            'preparation_minutes': recipe[8],
            'servings': recipe[9],
            'energy': recipe[10],
            'protein': recipe[11],
            'carbohydrates': recipe[12],
            'fats': recipe[13],
            'cuisine': recipe[14],
            'breakfast': recipe[15],
            'lunch': recipe[16],
            'dinner': recipe[17],
            'snack': recipe[18],
            'vegetarian': recipe[19],
            'vegan': recipe[20],
            'kosher': recipe[21],
            'halal': recipe[22],
            'dairy_free': recipe[23],
            'gluten_free': recipe[24],
            'nut_free': recipe[25],
            'egg_free': recipe[26],
            'shellfish_free': recipe[27],
            'soy_free': recipe[28],
            'ingredients': ingredients_list
        }
    }

def recipe_update_ingredients(recipe_id, ingredients):
    """
    Update ingredients for a given recipe (this function must only be used
    withing this module)
    """
    conn = None
    cur = None
    success = True
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        exist_ings = []
        new_ings = []
        
        for ing in ingredients:
            if ing['ingredient_id'] > 0:
                exist_ings.append(ing)
            else:
                new_ings.append(ing)
        exist_ids = tuple([ing['ingredient_id'] for ing in exist_ings])
        # delete the ingredients for recipe_id not in ingredient_id list
        if exist_ids:
            delete_query = ("""
                DELETE FROM recipe_ingredients WHERE recipe_id = %s AND
                ingredient_id NOT IN %s RETURNING ingredient_id
                """)
            cur.execute(delete_query, (str(recipe_id), exist_ids))
        else:
            delete_query = ("""
                DELETE FROM recipe_ingredients WHERE recipe_id = %s
                RETURNING ingredient_id
                """)
            cur.execute(delete_query, (str(recipe_id),))
        conn.commit()
        print('testing')
        delete_result = cur.fetchall()
        update_query = ("""
            UPDATE recipe_ingredients SET ingredient_name = %s, quantity = %s,
            unit = %s WHERE ingredient_id = %s
            """)
        for ing in exist_ings:
            ingredient_id = ing['ingredient_id']
            ingredient_name = ing['ingredient_name']
            quantity = ing['quantity']
            unit = ing['unit']
            # skip attempt to update deleted record
            if ingredient_id in delete_result:
                continue
            values = (ingredient_name, str(quantity), unit, ingredient_id)
            cur.execute(update_query, values)
            conn.commit()
            # ensure record was updated
            if cur.rowcount < 1:
                raise Exception

        insert_query = ("""
            INSERT INTO recipe_ingredients (recipe_id, ingredient_name,
            quantity, unit) VALUES (%s, %s, %s, %s)
            """)
        for ing in new_ings:
            ingredient_name = ing['ingredient_name']
            quantity = ing['quantity']
            unit = ing['unit']
            values = (str(recipe_id), ingredient_name, str(quantity), unit)
            cur.execute(insert_query, values)
            conn.commit()
            # ensure record was inserted
            if cur.rowcount < 1:
                raise Exception
    except:
        success = False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    return success


def recipe_update(data, token):
    """
    Update the given recipe
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
        recipe_id = data['recipe_id']
        query = ("SELECT COUNT(*) FROM recipes WHERE recipe_id = %s AND owner_id = %s")
        cur.execute(query, (str(recipe_id), str(owner_id)))
        if not cur.fetchone():
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find recipe owned by user"
        }
    
    # Update recipe
    try:
        recipe_name = data['recipe_name']
        recipe_description = data['recipe_description']
        recipe_photo = data['recipe_photo']
        recipe_status = data['recipe_status']
        recipe_method = data['recipe_method']
        preparation_hours = data['preparation_hours']
        preparation_minutes = data['preparation_minutes']
        servings = data['servings']
        energy = data['energy']
        protein = data['protein']
        carbohydrates = data['carbohydrates']
        fats = data['fats']
        cuisine = data['cuisine']
        breakfast = data['breakfast']
        lunch = data['lunch']
        dinner = data['dinner']
        snack = data['snack']
        vegetarian = data['vegetarian']
        vegan = data['vegan']
        kosher = data['kosher']
        halal = data['halal']
        dairy_free = data['dairy_free']
        gluten_free = data['gluten_free']
        nut_free = data['nut_free']
        egg_free = data['egg_free']
        shellfish_free = data['shellfish_free']
        soy_free = data['soy_free']
        ingredients = data['ingredients']

        params = (recipe_name, recipe_description, recipe_photo, recipe_status,\
            recipe_method, preparation_hours, preparation_minutes, servings, \
            energy, protein, carbohydrates, fats, cuisine, breakfast, lunch, \
            dinner, snack, vegetarian, vegan, kosher, halal, dairy_free, \
            gluten_free, nut_free, egg_free, shellfish_free, soy_free, \
            recipe_id)

        query = ("""
            UPDATE recipes
            SET recipe_name = %s, recipe_description = %s, recipe_photo = %s,
            recipe_status = %s, recipe_method = %s, preparation_hours = %s,
            preparation_minutes = %s, servings = %s, energy = %s, protein = %s,
            carbohydrates = %s, fats = %s, cuisine = %s, breakfast = %s,
            lunch = %s, dinner = %s, snack = %s, vegetarian = %s, vegan = %s,
            kosher = %s, halal = %s, dairy_free = %s, gluten_free = %s,
            nut_free = %s, egg_free = %s, shellfish_free = %s, soy_free = %s,
            edited_on = CURRENT_TIMESTAMP
            WHERE recipe_id = %s
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

    if recipe_update_ingredients(recipe_id, ingredients):
        return {
                'status_code': 200
            }
    else:
        return {
            'status_code': 400,
            'error': "Ingredients update failure"
        }


def recipe_clone(recipe_id, token):
    """
    Clone recipe with given id (only recipe owner permitted to do that)
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
        query = ("SELECT COUNT(*) FROM recipes WHERE recipe_id = %s AND owner_id = %s")
        cur.execute(query, (str(recipe_id), str(owner_id)))
        if not cur.fetchone():
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find recipe owned by user"
        }
    
    try:
        query = ("""
        INSERT INTO recipes (owner_id, recipe_name, recipe_description,
        recipe_photo, recipe_status, recipe_method, preparation_hours,
        preparation_minutes, servings, energy, protein, carbohydrates, fats,
        cuisine, breakfast, lunch, dinner, snack, vegetarian, vegan, kosher,
        halal, dairy_free, gluten_free, nut_free, egg_free, shellfish_free,
        soy_free)
        SELECT owner_id, recipe_name, recipe_description, recipe_photo,
        recipe_status, recipe_method, preparation_hours, preparation_minutes,
        servings, energy, protein, carbohydrates, fats, cuisine, breakfast,
        lunch, dinner, snack, vegetarian, vegan, kosher, halal, dairy_free,
        gluten_free, nut_free, egg_free, shellfish_free, soy_free
        FROM recipes WHERE recipe_id = %s RETURNING recipe_id
        """)
        cur.execute(query, (str(recipe_id)))
        conn.commit()
        new_recipe_id = cur.fetchone()[0]
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "problem cloning recipe"
        }

    try:
        query = ("""
            INSERT INTO recipe_ingredients
            (recipe_id, ingredient_name, quantity, unit)
            SELECT %s, ingredient_name, quantity, unit
            FROM recipe_ingredients WHERE recipe_id = %s
            """)
        cur.execute(query, (str(new_recipe_id), str(recipe_id)))
        conn.commit()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "problem cloning recipe ingredients"
        }
    cur.close()
    conn.close()
    return {
        'status_code': 200,
        'body': {
            'recipe_id': new_recipe_id
        }
    }

def recipe_delete(recipe_id, token):
    """
    Delete recipe with given id (only recipe owner permitted to do that)
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
            DELETE FROM recipes WHERE recipe_id = %s AND owner_id = %s
            RETURNING recipe_id
            """)
        cur.execute(query, (str(recipe_id), str(owner_id)))
        conn.commit()
        deleted_recipe_id, = cur.fetchone()
        if recipe_id != deleted_recipe_id:
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
            'recipe_id': deleted_recipe_id
        }
    }

    
def recipes_fetch_own(token):
    """
    Fetch own recipes
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
            SELECT recipe_id, recipe_name, recipe_photo, recipe_status, cuisine 
            FROM recipes WHERE owner_id = %s""")
        cur.execute(query, (owner_id,))
        output = cur.fetchall()
        recipes_list = []
        for recipe in output:
            recipes_list.append({
                'recipe_id': recipe[0],
                'recipe_name': recipe[1],
                'recipe_photo': recipe[2],
                'recipe_status': recipe[3],
                'cuisine': recipe[4]
            })

        # Close connection
        return {
            'status_code':200,
            'body': recipes_list
        }
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code':400,
            'error': None
        }

def recipe_review_details(recipe_id, auth_user_id):
    """
    Returns the review details
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        reviews_list = []
        query = ("""
            SELECT u.id, u.display_name, u.base64_image, r.review_id,
            r.rating, r.comment, r.reply, r.created_on
            FROM users u JOIN recipe_reviews r ON (u.id = r.user_id)
            WHERE r.recipe_id = %s and u.visibility = 'public'
        """)
        cur.execute(query, (recipe_id,))
        sql_result = cur.fetchall()
        reviews_list = []
        votes_query = ("""
            SELECT COUNT(*) FROM recipe_reviews_votes
            WHERE review_id = %s AND is_upvote = %s
        """)
        user_vote = ("""
            SELECT is_upvote FROM recipe_reviews_votes
            WHERE review_id = %s
        """)
        for review in sql_result:
            user_id, display_name, user_image, review_id, rating, comment, \
                reply, created_on = review

            cur.execute(votes_query, (review_id, True))
            upvotes, = cur.fetchone()

            cur.execute(votes_query, (review_id, False))
            downvotes, = cur.fetchone()

            if auth_user_id:
                cur.execute(user_vote, (review_id, False))
                cur_user_vote, = cur.fetchone()
            else:
                cur_user_vote = None
            
            reviews_list.append({
                'user_id': user_id,
                'display_name': display_name,
                'user_image': user_image,
                'review_id': review_id,
                'rating': rating,
                'comment': comment if comment else '',
                'reply': reply if reply else '',
                'created_on': created_on,
                'upvote_count': upvotes,
                'downvote_count': downvotes,
                'cur_user_vote': cur_user_vote if cur_user_vote is not None else ''
            })

        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        raise Exception
    return reviews_list


def recipe_fetch_user_likes(recipe_id, auth_user_id):
    """
    Returns the review details
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        query = "SELECT COUNT(*) FROM recipe_user_likes WHERE recipe_id = %s"
        cur.execute(query, (recipe_id))
        likes_count, = cur.fetchone()
        if auth_user_id:
            query = ("""
            SELECT like_id FROM recipe_user_likes WHERE recipe_id = %s
            AND user_id = %s
            """)
        cur.execute(query, (recipe_id, auth_user_id))
        has_liked = cur.rowcount > 0
        
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        raise Exception
    return {
        'likes_count': likes_count,
        'has_liked': has_liked
    }


def recipe_details(recipe_id, token):
    """
    Get details for one recipe
    """
    if not recipe_id:
        return {
            'status_code': 400,
            'error': "Bad Request"
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
            SELECT u.id, u.display_name, u.base64_image,
            r.recipe_name, r.recipe_description, r.recipe_photo,
            r.recipe_status, r.recipe_method, r.created_on, r.edited_on,
            r.preparation_hours, r.preparation_minutes, r.servings, r.energy,
            r.protein, r.carbohydrates, r.fats, r.cuisine, r.breakfast, r.lunch,
            r.dinner, r.snack, r.vegetarian, r.vegan, r.kosher, r.halal,
            r.dairy_free, r.gluten_free, r.nut_free, r.egg_free,
            r.shellfish_free, r.soy_free
            FROM users u JOIN recipes r ON (u.id = r.owner_id)
            WHERE r.recipe_id = %s AND
            (u.token = %s OR r.recipe_status = 'published')
        """)
        
        cur.execute(query, (recipe_id, token))
        recipe = cur.fetchone()
        if not recipe:
            raise Exception
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 404,
            'error': "recipe does not exist"
        }

    try:
        if token:
            query = "SELECT id, units, efficiency FROM users WHERE token = %s"
            cur.execute(query, (str(token),))
            user_id, units, efficiency = cur.fetchone()
        else:
            user_id, units, efficiency = None
        ingredients_list = recipe_fetch_ingredients(recipe_id)
        reviews = recipe_review_details(recipe_id, user_id)
        likes = recipe_fetch_user_likes(recipe_id, user_id)
        reviews = []
        likes = []
    except:
        return {
            'status_code': 400,
            'error': "cannot fetch recipe"
        }

    return {
        'status_code': 200,
        'body': {
            'user_id': recipe[0],
            'user_display_name': recipe[1],
            'user_image': recipe[2],
            'recipe_name': recipe[3],
            'recipe_description': recipe[4],
            'recipe_photo': recipe[5],
            'recipe_status': recipe[6],
            'recipe_method': recipe[7],
            'created_on': str(recipe[8]),
            'edited_on': str(recipe[9]),
            'preparation_hours': recipe[10],
            'preparation_minutes': recipe[11],
            'servings': recipe[12],
            'energy': recipe[13],
            'protein': recipe[14],
            'carbohydrates': recipe[15],
            'fats': recipe[16],
            'cuisine': recipe[17],
            'breakfast': recipe[18],
            'lunch': recipe[19],
            'dinner': recipe[20],
            'snack': recipe[21],
            'vegetarian': recipe[22],
            'vegan': recipe[23],
            'kosher': recipe[24],
            'halal': recipe[25],
            'dairy_free': recipe[26],
            'gluten_free': recipe[27],
            'nut_free': recipe[28],
            'egg_free': recipe[29],
            'shellfish_free': recipe[30],
            'soy_free': recipe[31],
            'units': str(units),
            'efficiency': str(efficiency),
            'ingredients': ingredients_list,
            'reviews': reviews,
            'likes': likes
        }
    }
    