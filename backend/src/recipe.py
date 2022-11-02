from re import S
import psycopg2
from backend_helper import connect, verify_token
from review import review_details
from algorithm import calculate_similarity, take_second
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
            'recipe_id': recipe_id
        }
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
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        cur.close()
        return {
            'status_code': 400,
            'error': 'recipe could not be published'
        }
    return {
        'status_code': 200
    }

def recipe_fetch_ingredients(recipe_id):
    """
    Update ingredients for a given recipe (this function must only be used
    within this module, only where recipe_id definitely exists)
    
    Args:
        recipe_id   (Integer): the recipe id to fetch ingredient list for
        
    Returns:
        ingredient_list     (list of dict)
                            [{
                                ingredient_id     (Integer)
                                ingredient_name   (String)
                                quantity          (Integer)
                                unit              (String)
                            }]
    
    Raises:
        Exception: if fails to retrieve ingredients list
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

    Args:
        recipe_id   (Integer): the recipe id to fetch data for
        token       (String): token of authenticated user
        
    Returns:
        Status 200 - success
            body    (dict of atomic values and lists)
                recipe_name         (String)
                recipe_description  (String)
                recipe_photo        (String)
                recipe_status       (String)
                recipe_method       (String)
                created_on          (String)
                edited_on           (String)
                preparation_hours   (String)
                preparation_minutes (String)
                servings            (Integer)
                energy              (Integer)
                protein             (Integer)
                carbohydrates       (Integer)
                fats                (Integer)
                cuisine             (String)
                breakfast           (Boolean)
                lunch               (Boolean)
                dinner              (Boolean)
                snack               (Boolean)
                vegetarian          (Boolean)
                vegan               (Boolean)
                kosher              (Boolean)
                halal               (Boolean)
                dairy_free          (Boolean)
                gluten_free         (Boolean)
                nut_free            (Boolean)
                egg_free            (Boolean)
                shellfish_free      (Boolean)
                soy_free            (Boolean)
                ingredients         (list of dict)
                        ingredient_id     (Integer)
                        ingredient_name   (String)
                        quantity          (Integer)
                        unit              (String)

        Status 400 - failure to find recipe id or ingredients
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
    Update ingredients for a given recipe (internal use only - this function
    must only be used withing this module, must never be called by server)

    Args:
        recipe_id   (Integer): the recipe id to fetch data for
        ingredients (list of dict)
                ingredient_id     (Integer)
                ingredient_name   (String)
                quantity          (Integer)
                unit              (String)
    
    Returns:
        success     True if ingredients updated successfully otherwise False
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

    Args:
        data    (dict of atomic values and collections): values to update
                recipe_name         (String)
                recipe_description  (String)
                recipe_photo        (String)
                recipe_status       (String)
                recipe_method       (String)
                created_on          (String)
                edited_on           (String)
                preparation_hours   (Integer)
                preparation_minutes (Integer)
                servings            (Integer)
                energy              (Integer)
                protein             (Integer)
                carbohydrates       (Integer)
                fats                (Integer)
                cuisine             (String)
                breakfast           (Boolean)
                lunch               (Boolean)
                dinner              (Boolean)
                snack               (Boolean)
                vegetarian          (Boolean)
                vegan               (Boolean)
                kosher              (Boolean)
                halal               (Boolean)
                dairy_free          (Boolean)
                gluten_free         (Boolean)
                nut_free            (Boolean)
                egg_free            (Boolean)
                shellfish_free      (Boolean)
                soy_free            (Boolean)
                ingredients         (list of dicts)
                        ingredient_id     (Integer)
                        ingredient_name   (String)
                        quantity          (Integer)
                        unit              (String)

        token   (String): token of authenticated user
        
    Returns:
        Status 200 - success
        Status 400 - failure to update recipe or ingredients
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

    Args:
        recipe_id       (Integer): the recipe to clone
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - recipe and ingredients cloned successfully
                body containing dictionary with cloned recipe_id (Integer)

        Status 400 - failure to clone recipe or/and ingredients
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
        cur.execute(query, (str(recipe_id),))
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

    Args:
        recipe_id       (Integer): the recipe to delete
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - recipe and ingredients deleted successfully
                body containing dictionary with deleted recipe_id (Integer)

        Status 400 - failure to delete recipe or/and ingredients
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
    Fetch own recipes (private, accessible only by recipe owner)

    Args:
        token   (String): token of authenticated user
        
    Returns:
        Status 200 - successful return of user's recipes
                body    (list of dict)
                        recipe_id       (Integer)
                        recipe_name     (String)
                        recipe_photo    (String)
                        recipe_status   (String)
                        cuisine         (String)
                        review_cnt      (Integer)
                        rating_avg      (String): JSON cannot contain decimal
                        likes_cnt       (Integer)

        Status 400 - failure to fetch recipe
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
            SELECT r.recipe_id, r.recipe_name, r.recipe_photo, r.recipe_status,
            r.cuisine, s.review_cnt, s.rating_avg, v.likes_cnt
            FROM recipes r LEFT OUTER JOIN (
                SELECT COUNT(*) review_cnt, AVG(rating) rating_avg, recipe_id
                FROM recipe_reviews GROUP BY recipe_id
            ) s ON (r.recipe_id = s.recipe_id)
            LEFT OUTER JOIN (
				SELECT COUNT(*) likes_cnt, recipe_id
				FROM recipe_user_likes GROUP BY recipe_id
			) v ON (r.recipe_id = v.recipe_id)
            WHERE r.owner_id = %s
            """)
        cur.execute(query, (owner_id,))
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
        'body': recipes_list
    }

def recipes_user_published(user_id):
    """
    Fetch recipes for user id (public, accessible to everyone)

    Args:
        user_id     (Integer): user id to fetch published recipes for
        
    Returns:
        Status 200 - successful return of user's published recipes
                recipes (list of dict)
                        recipe_id           (Integer)
                        recipe_name         (String)
                        recipe_photo        (String)
                        created_on          (String)
                        preparation_hours   (Integer)
                        preparation_minutes (Integer)
                        cuisine             (String)
                        breakfast           (Boolean)
                        lunch               (Boolean)
                        dinner              (Boolean)
                        snack               (Boolean)
                        vegetarian          (Boolean)
                        vegan               (Boolean)
                        kosher              (Boolean)
                        halal               (Boolean)
                        dairy_free          (Boolean)
                        gluten_free         (Boolean)
                        nut_free            (Boolean)
                        egg_free            (Boolean)
                        shellfish_free      (Boolean)
                        soy_free            (Boolean)
                        review_cnt      (Integer)
                        rating_avg      (String): JSON cannot contain decimal
                        likes_cnt       (Integer)

        Status 400 - failure to fetch recipe
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
            SELECT r.recipe_id, r.recipe_name, r.recipe_photo, r.created_on,
            r.preparation_hours, r.preparation_minutes, r.cuisine, r.breakfast,
            r.lunch, r.dinner, r.snack, r.vegetarian, r.vegan, r.kosher,
            r.halal, r.dairy_free, r.gluten_free, r.nut_free, r.egg_free,
            r.shellfish_free, r.soy_free, s.review_cnt, s.rating_avg,
            v.likes_cnt
            FROM recipes r LEFT OUTER JOIN (
                SELECT COUNT(*) review_cnt, AVG(rating) rating_avg, recipe_id
                FROM recipe_reviews GROUP BY recipe_id
            ) s ON (r.recipe_id = s.recipe_id)
            LEFT OUTER JOIN (
				SELECT COUNT(*) likes_cnt, recipe_id
				FROM recipe_user_likes GROUP BY recipe_id
			) v ON (r.recipe_id = v.recipe_id)
            WHERE r.owner_id = %s AND r.recipe_status = 'published'
            """)
        cur.execute(query, (user_id,))
        output = cur.fetchall()
        recipes_list = []
        for recipe in output:
            # need average but json in flask doesn't like decimal data
            recipes_list.append({
                'recipe_id': recipe[0],
                'recipe_name': recipe[1],
                'recipe_photo': recipe[2],
                'created_on': str(recipe[3]),
                'preparation_hours': recipe[4],
                'preparation_minutes': recipe[5],
                'cuisine': recipe[6],
                'breakfast': recipe[7],
                'lunch': recipe[8],
                'dinner': recipe[9],
                'snack': recipe[10],
                'vegetarian': recipe[11],
                'vegan': recipe[12],
                'kosher': recipe[13],
                'halal': recipe[14],
                'dairy_free': recipe[15],
                'gluten_free': recipe[16],
                'nut_free': recipe[17],
                'egg_free': recipe[18],
                'shellfish_free': recipe[19],
                'soy_free': recipe[20],
                'review_cnt': 0 if recipe[21] is None else recipe[21],
                'rating_avg': '0.0' if recipe[22] is None else f'{recipe[22]:.1f}',
                'likes_cnt': 0 if recipe[23] is None else recipe[23]
            })
        cur.close()
        conn.close()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code':400,
            'error': 'could not fetch recipes'
        }
    return {
        'status_code':200,
        'recipes': recipes_list
    }

def recipe_fetch_user_likes(recipe_id, auth_user_id):
    """
    Returns the total number of likes for a recipe and whether an authenticated
    user has liked the recipe (internal use only)

    Args:
        recipe_id       (Integer): the recipe to delete
        auth_user_id    (Integer): authenticated user to find likes for
        
    Returns:
        (dict)
            likes_count (Integer): total likes for recipe
            has_liked   (Boolean): True if user has liked otherwise False

    Raises:
        Exception: if fails to retrive likes count or user like status
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        query = "SELECT COUNT(*) FROM recipe_user_likes WHERE recipe_id = %s"
        cur.execute(query, (recipe_id,))
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

    Args:
        recipe_id       (Integer): the recipe to delete
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - successful return of user's published recipes
                body (dict of atomic values and lists)
                        author_id           (Integer)
                        author_display_name (String)
                        author_image        (String)
                        recipe_name         (String)
                        recipe_description  (String)
                        recipe_photo        (String)
                        recipe_status       (String)
                        recipe_method       (String)
                        created_on          (String) - timestamp as string
                        edited_on           (String) - timestamp as string
                        preparation_hours   (Integer)
                        preparation_minutes (Integer)
                        servings            (Integer)
                        energy              (Integer)
                        protein             (Integer)
                        carbohydrates       (Integer)
                        fats                (Integer)
                        cuisine             (String)
                        breakfast           (Boolean)
                        lunch               (Boolean)
                        dinner              (Boolean)
                        snack               (Boolean)
                        vegetarian          (Boolean)
                        vegan               (Boolean)
                        kosher              (Boolean)
                        halal               (Boolean)
                        dairy_free          (Boolean)
                        gluten_free         (Boolean)
                        nut_free            (Boolean)
                        egg_free            (Boolean)
                        shellfish_free      (Boolean)
                        soy_free            (Boolean)
                        units               (String)
                        efficiency          (String)
                        ingredients     (list of dicts)
                                ingredient_id     (Integer)
                                ingredient_name   (String)
                                quantity          (Integer)
                                unit              (String)
                        reviews     (list of dicts)
                                user_id             (Integer)
                                display_name        (String)
                                user_image          (String)
                                user_visibility     (String)
                                review_id           (Integer)
                                rating              (Integer)
                                comment             (String)
                                reply               (String)
                                created_on          (String): from timestamp
                                upvote_count        (Integer)
                                downvote_count      (Integer)
                                cur_user_vote       (String or Boolean)
                        likes   (dict)
                                likes_count (Integer)
                                has_liked   (Boolean): for authenticated user
                        user_is_author  (Boolean)
                        is_subscribed   (Boolean): for authenticated user

        Status 400 - failure to fetch recipe
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
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
        user_results = None
        if token:
            query = ("""
                SELECT id, units, efficiency FROM users
                WHERE token IS NOT NULL AND token = %s
                """)
            cur.execute(query, (str(token),))
            user_results = cur.fetchone()
        if user_results is not None:
            user_id, units, efficiency = user_results
        else:
            user_id, units, efficiency, = -1, 'Metric', 'Intermediate'

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
            (u.id = %s OR r.recipe_status = 'published')
        """)
        cur.execute(query, (recipe_id, str(user_id)))
        recipe = cur.fetchone()
        if not recipe:
            raise Exception
        owner_id = recipe[0]
        if token and user_id != owner_id:
            subs_query = ("""
                SELECT COUNT(*) FROM subscriptions
                WHERE following_id = %s AND follower_id = %s
                """)
            cur.execute(subs_query, (owner_id, user_id))
            subs_count, = cur.fetchone()
            is_subscribed = True if subs_count > 0 else False
        else:
            is_subscribed = False
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 404,
            'error': "recipe does not exist"
        }

    try:
        ingredients_list = recipe_fetch_ingredients(recipe_id)
        reviews = review_details(recipe_id, user_id)
        likes = recipe_fetch_user_likes(recipe_id, user_id)
    except:
        return {
            'status_code': 400,
            'error': "cannot fetch recipe"
        }

    return {
        'status_code': 200,
        'body': {
            'author_id': recipe[0],
            'author_display_name': recipe[1],
            'author_image': recipe[2],
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
            'likes': likes,
            'user_is_author': user_id == recipe[0],
            'is_subscribed': is_subscribed
        }
    }

def recipe_like(recipe_id, token):
    """
    Like toggle a given recipe (like => unlike, unlike => like). Recipe author
    cannot like/unlike their own recipe.

    Args:
        recipe_id       (Integer): the recipe to like or unlike
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - successful like or unlike of recipe
                likes_count (Integer): total number of likes for recipe
                has_liked   (Boolean): whether the user has liked or unliked

        Status 400 - failure to like or unlike recipe
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
    """
    # error if no token
    if not token or not verify_token(token):
        return {
            'status_code': 401,
            'error': "only authenticated users can like a recipe"
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
            'error': "only authenticated users can like a recipe"
        }

    try:
        query = ("""
            SELECT owner_id FROM recipes WHERE recipe_id = %s
            AND recipe_status = 'published'
            """)
        cur.execute(query, (recipe_id,))
        owner_id, = cur.fetchone()
        
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code':400,
            'error': "cannot find recipe id"
        }

    if user_id == owner_id:
        return {
            'status_code':400,
            'error': "cannot like or unlike own recipe"
        }

    try:
        query = ("""
            SELECT like_id FROM recipe_user_likes
            WHERE recipe_id = %s AND user_id = %s
        """)
        cur.execute(query, (recipe_id, user_id))
        sql_result = cur.fetchone()
        if sql_result:
            like_id, = sql_result
            delete_query = "DELETE FROM recipe_user_likes WHERE like_id = %s"
            cur.execute(delete_query, (like_id,))
            conn.commit()
            has_liked = False
        else:
            insert_query = ("""
                INSERT INTO recipe_user_likes(user_id, recipe_id)
                VALUES (%s, %s)
                """)
            cur.execute(insert_query, (user_id, recipe_id))
            conn.commit()
            has_liked = True
        count_query = ("""SELECT COUNT(*) FROM recipe_user_likes
            WHERE recipe_id = %s
            """)
        cur.execute(count_query, (recipe_id,))
        likes_count, = cur.fetchone()
        cur.close()
        conn.close()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code':400,
            'error': "cannot like or unlike recipe"
        }
    
    return {
        'status_code': 200,
        'body': {
            'likes_count': likes_count,
            'has_liked': has_liked
        }
    }

def recipe_related(recipe_id):
    """
    Return list of recipes most similar to current recipe based on user ratings

    Args:

    Returns:
    
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
    
    # Get largest user_id
    max_uid = 0

    cur.execute("SELECT MAX(user_id) FROM recipe_reviews;")
    sql_result = cur.fetchall()

    if sql_result:
        max_uid, = sql_result[0]
    
    # Get largest recipe_id
    max_rid = 0
    
    cur.execute("SELECT MAX(recipe_id) FROM recipe_reviews;")
    sql_result = cur.fetchall()

    if sql_result:
        max_rid, = sql_result[0]

    # Collect all ratings info from database
    cur.execute("SELECT recipe_id, user_id, rating FROM recipe_reviews;")

    sql_result = cur.fetchall()

    # If empty results, then return empty body
    if not sql_result:
        cur.close()
        conn.close()

        return {
            'status_code': 200,
            'body': {}
        }
    
    # Otherwise, initialise 2d array with recipes as rows and users as columns
    ratings = [[0 for x in range(max_uid)] for y in range(max_rid)]

    for rating_info in sql_result:
        rid, uid, rating = rating_info
        ratings[rid - 1][uid - 1] = rating

    # Calculate similarity of all recipes and add them to recommendations
    recommendations = []

    for idx, recipe_ratings in enumerate(ratings):
        # Skip the targeted recipe itself as not to recommend itself
        if idx + 1 == recipe_id:
            continue

        # Skip the recipe if it is a draft
        sql_query = "SELECT * FROM recipes WHERE recipe_id = %s \
                     AND recipe_status = 'published'"
        cur.execute(sql_query, (idx + 1,))

        sql_result = cur.fetchall()
        if not sql_result:
            continue

        sim = calculate_similarity(ratings[recipe_id - 1], recipe_ratings)
        recommendations.append((idx + 1, sim))

    # Sort recommendations by largest similarity
    recommendations.sort(key=take_second, reverse=True)

    # For each recipe_id, add recipe details to body content
    body_content = []
    
    for recommendation in recommendations:
        r_id = recommendation[0]
        r_details = recipe_details(r_id, None)

        # Check that fetching recipe details is successful
        if r_details['status_code'] != 200:
            cur.close()
            conn.close()

            return r_details
        
        # Otherwise add details to body_content
        else:
            body_content.append(r_details['body'])

    return {
        'status_code': 200,
        'body': body_content
    }
