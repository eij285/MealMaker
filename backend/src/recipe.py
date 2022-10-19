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
        cur.close()
        conn.close()
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
            'soy_free': recipe[28]
        }
    }


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
    

def fetch_all_recipe():
    # Start connection to database
    connection = connect()
    cur = connection.cursor()
    
    try:
        command = ("SELECT * FROM recipe")
        cur.execute(command)
        output = cur.fetchall()
        # Close connection
        connection.close()
        cur.close()
        return {
            'status_code':200,
            'body': output
        }
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        cur.close()
        return {
            'status_code':400,
            'error': None
        }
