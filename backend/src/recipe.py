import psycopg2
from backend_helper import connect
   
# def create_recipe_table(connection):
#     cur = connection.cursor()
#     command = ("""
#         CREATE TABLE recipe(
#             recipe_id SERIAL PRIMARY KEY,
#             owner_id INTEGER,
#             recipe_name VARCHAR(255) NOT NULL,
#             recipe_description VARCHAR(255) NOT NULL,
#             methods VARCHAR(255) NOT NULL,
#             is_public BOOLEAN NOT NULL DEFAULT FALSE,
#             total_star INTEGER,
#             review_count INTEGER,
#             portion_size INTEGER
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
    

def create_recipe(name, description, method, portion_size, token):
    # Start connection to database
    connection = connect()
    cur = connection.cursor()

    # Retrieve user id based on token
    if token == None:
        return {
            'status_code': 401,
            'error': None
        }
    
    try:
        command = ("""
            SELECT 
                id 
            FROM 
                users 
            WHERE token = %s""")
        cur.execute(command, (str(token),))
        owner_id = cur.fetchall()[0][0]
    except:
        return {
            'status_code': 400,
            'error': None
        }
        
    # Add new recipe to system
    try:
        command = ("""
            INSERT INTO
                recipe(owner_id, recipe_name, recipe_description, methods, portion_size)
            VALUES
                (%s, %s, %s, %s, %s)
            RETURNING
                recipe_id
            """)
        cur.execute(command, (owner_id, name, description, method, portion_size,))
        connection.commit()
        recipe_id = cur.fetchone()[0]
        # Close connection
        connection.close()
        return {
            'status_code': 201,
            'body': {
                'recipe_id': recipe_id
            }
        }
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        return {
            'status_code': 400,
            'error': None
        }


def publish_recipe(recipe_id, publish):
    
    # Start connection to database
    connection = connect()
    cur = connection.cursor()
    
    # Publish recipe
    try:
        command = ("""
            UPDATE recipe
            SET is_public = %s
            WHERE recipe_id = %s
            """)
        cur.execute(command, (publish, recipe_id,))
        connection.commit()
        
        # Close connection
        connection.close()
        return {
            'status_code': 200
        }
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        return {
            'status_code': 400,
            'error': None
        }
        
    

def edit_recipe(name, description, methods, portion_size, recipe_id):
    
    # Start connection to database
    connection = connect()
    cur = connection.cursor()
    
    # Update recipe
    try:
        command = ("""
            UPDATE recipe
            SET recipe_name = %s, recipe_description = %s, methods = %s, portion_size = %s
            WHERE recipe_id = %s
            """)
        cur.execute(command, (name, description, methods, portion_size, recipe_id,))
        connection.commit()
        # Close connection
        connection.close()
        return {
            'status_code': 200
        }
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
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
        return {
            'status_code':200,
            'body': output
        }
        
    except (Exception, psycopg2.DatabaseError) as error:
        # Close connection
        connection.close()
        return {
            'status_code':400,
            'error': None
        }


if __name__ == "__main__":
    all_recipe = fetch_all_recipe()
    print(all_recipe['body'])