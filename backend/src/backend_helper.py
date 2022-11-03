import jwt
import psycopg2
from datetime import datetime, timezone, timedelta
from config import DB_CONN_STRING, SQL_SCHEMA, SQL_DATA


def connect():
    """Connect to database

    Returns:
        psycopg2.connect: connection
        None if error
    """
    connection = None
    try:
        print('Conencting to the database...')
        # connecting to different database config? change in config.py
        connection = psycopg2.connect(DB_CONN_STRING)
        cur = connection.cursor()
        print('PostgreSQL database version: ')
        cur.execute('SELECT version()')
        return connection
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

def create_user_database():
    connection = connect()
    command = ("""
        CREATE TABLE users (
            id              SERIAL,
            pronoun         VARCHAR(20),
            given_names     VARCHAR(20),
            last_name       VARCHAR(20),
            display_name    VARCHAR(30) NOT NULL,
            email           VARCHAR(60) NOT NULL UNIQUE,
            password        CHAR(60) NOT NULL,
            password_reset  CHAR(32),
            base64_image    TEXT,
            country         VARCHAR(20),
            about           TEXT,
            visibility      VARCHAR(7) NOT NULL DEFAULT ('private'),
            breakfast       BOOLEAN NOT NULL DEFAULT TRUE,
            lunch           BOOLEAN NOT NULL DEFAULT TRUE,
            dinner          BOOLEAN NOT NULL DEFAULT TRUE,
            snack           BOOLEAN NOT NULL DEFAULT TRUE,
            vegetarian      BOOLEAN NOT NULL DEFAULT FALSE,
            vegan           BOOLEAN NOT NULL DEFAULT FALSE,
            kosher          BOOLEAN NOT NULL DEFAULT FALSE,
            halal           BOOLEAN NOT NULL DEFAULT FALSE,
            dairy_free      BOOLEAN NOT NULL DEFAULT FALSE,
            gluten_free     BOOLEAN NOT NULL DEFAULT FALSE,
            nut_free        BOOLEAN NOT NULL DEFAULT FALSE,
            egg_free        BOOLEAN NOT NULL DEFAULT FALSE,
            shellfish_free  BOOLEAN NOT NULL DEFAULT FALSE,
            soy_free        BOOLEAN NOT NULL DEFAULT FALSE,
            units           VARCHAR(8) NOT NULL DEFAULT ('Metric'),
            efficiency      VARCHAR(12) NOT NULL DEFAULT ('Intermediate'),
            last_request    TIMESTAMP,
            token           TEXT,
            CONSTRAINT valid_visibility CHECK (visibility in ('private', 'public')),
            CONSTRAINT valid_units CHECK (units in ('Metric', 'Imperial')),
            CONSTRAINT valid_efficiency CHECK (efficiency in ('Beginner', 'Intermediate', 'Expert')),
            PRIMARY KEY (id)
        )

        """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def create_recipe_database():
    connection = connect()
    command = ("""
        CREATE TABLE recipes (
            recipe_id       SERIAL,
            owner_id        INTEGER NOT NULL,
            recipe_name     VARCHAR(255) NOT NULL,
            recipe_description TEXT NOT NULL,
            recipe_photo    TEXT,
            recipe_status   VARCHAR(9) NOT NULL DEFAULT ('draft'),
            recipe_method   TEXT,
            created_on      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            edited_on       TIMESTAMP,
            preparation_hours INTEGER,
            preparation_minutes INTEGER,
            servings        INTEGER NOT NULL,
            energy          INTEGER,
            protein         INTEGER,
            carbohydrates   INTEGER,
            fats            INTEGER,
            cuisine         VARCHAR(30),
            breakfast       BOOLEAN NOT NULL DEFAULT FALSE,
            lunch           BOOLEAN NOT NULL DEFAULT FALSE,
            dinner          BOOLEAN NOT NULL DEFAULT FALSE,
            snack           BOOLEAN NOT NULL DEFAULT FALSE,
            vegetarian      BOOLEAN NOT NULL DEFAULT FALSE,
            vegan           BOOLEAN NOT NULL DEFAULT FALSE,
            kosher          BOOLEAN NOT NULL DEFAULT FALSE,
            halal           BOOLEAN NOT NULL DEFAULT FALSE,
            dairy_free      BOOLEAN NOT NULL DEFAULT FALSE,
            gluten_free     BOOLEAN NOT NULL DEFAULT FALSE,
            nut_free        BOOLEAN NOT NULL DEFAULT FALSE,
            egg_free        BOOLEAN NOT NULL DEFAULT FALSE,
            shellfish_free  BOOLEAN NOT NULL DEFAULT FALSE,
            soy_free        BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT valid_status CHECK (recipe_status in ('draft', 'published')),
            PRIMARY KEY (recipe_id),
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()
    
def create_recipe_reviews_database():
    connection = connect()
    command = ("""
        CREATE TABLE recipe_reviews (
            review_id       SERIAL,
            recipe_id       INTEGER NOT NULL,
            user_id         INTEGER NOT NULL,
            rating          INTEGER NOT NULL,
            comment         TEXT,
            reply           TEXT,
            created_on      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (review_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT one_review_per_recipe UNIQUE(recipe_id, user_id)
        )
        """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def create_recipe_user_likes_database():
    connection = connect()
    command = ("""
        CREATE TABLE recipe_user_likes (
            like_id         SERIAL,
            user_id         INTEGER NOT NULL,
            recipe_id       INTEGER NOT NULL,
            PRIMARY KEY (like_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
            CONSTRAINT one_like_per_recipe UNIQUE(user_id, recipe_id)
        )
        """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()


def remove_user_database():
    connection = connect()
    command = ("""
            DROP TABLE users CASCADE
            """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def remove_recipe_ingredient_database():
    connection = connect()
    command = ("""
            DROP TABLE recipe_ingredients CASCADE
            """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def remove_recipe_database():
    connection = connect()
    command = ("""
            DROP TABLE recipes CASCADE
            """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def remove_recipe_reviews_database():
    connection = connect()
    command = ("""
            DROP TABLE recipe_reviews CASCADE
            """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def remove_recipe_user_likes_database():
    connection = connect()
    command = ("""
            DROP TABLE recipe_user_likes CASCADE
            """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def verify_token(token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    cur.execute("SELECT id FROM users WHERE token = %s;", (token,))
    
    sql_result = cur.fetchall()
    if not sql_result:
        return {
            'status_code': 400,
            'error': 'Token does not match any active tokens on server'
        }

    id_db, = sql_result[0]

    try:
        decoded_jwt = jwt.decode(token, "SECRET", algorithms='HS256')
    except:
        return {
            'status_code': 400,
            'error': 'Token cannot be decoded'
        }
    
    id_decoded = decoded_jwt['u_id']

    print(type(id_db))
    print(type(id_decoded))

    if id_db == id_decoded:
        sql_query = "UPDATE users SET last_request = %s WHERE id = %s;"
        cur.execute(sql_query, (datetime.now(tz=timezone.utc), str(id_db)))

        conn.commit()
        cur.close()
        conn.close()

        return True
    else:
        conn.commit()
        cur.close()
        conn.close()

        return False


def fetch_database(database):
    """
    Fetch all info in a database
    
    Input:
        database: name of database as a string
        
    Return:
        list of dictionary, with head as column name
        e.g.
        [
            {
                'id': 123,
                'name': ABC
            },
            {
                'id': 234,
                'name': BCD
            }
        
        ]"""
    connection = connect()
    command = ("SELECT * FROM " + database)
    cur = connection.cursor()
    cur.execute(command)
    out_data = cur.fetchall()
    command = ("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION"""
            )
    cur.execute(command, (database,))
    out_header = cur.fetchall()
    out_dict = {}
    out_list = []
    len_data = len(out_data)
    len_header = len(out_header)
    for i in range(len_data):
        for j in range(len(out_data[i])):
            k = j if j < len_header else j % len_header
            out_dict[out_header[k][0]] = out_data[i][j]
        out_list.append(out_dict)
        out_dict = {}
    connection.close()
    cur.close()
    return out_list


def database_file_ops(filename):
    """Import filename into database (schema, data or both)
    
    Args:
        SQL filename: should contain DDL or/and DML statements

    Returns:
        True if database operation executed successfully
        False if database operation failed (requires manual intervention)
    """
    conn = None
    cur = None
    success = False
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        cur.execute(open(filename, "r").read())
        conn.commit()
        success = True
    except psycopg2.Error as err:
        print(f"DB error: {err}")
    except OSError as err:
        print(f"OS error: {err}")
    except:
        print("Unspecified error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return success

def database_reset():
    """Resets the database
    
    Drops all tables, stored procedures, triggers, etc and recreates entire
    schema from an sql file

    Returns:
        True if database reset succeeded
        False if database reset failed (requires manual intervention)
    """
    return database_file_ops(SQL_SCHEMA)


def database_populate():
    """Populates the database with sample (demo) data

    Returns:
        True if database reset succeeded
        False if database reset failed (requires manual intervention)
    """
    return database_file_ops(SQL_DATA)


def create_recipe_ingredient_database():
    """
    Create recipe_ingredient database
    """
    
    connection = connect()
    command = ("""
        CREATE TABLE recipe_ingredients (
            ingredient_id   SERIAL,
            recipe_id       INTEGER NOT NULL,
            ingredient_name VARCHAR(30) NOT NULL,
            quantity        INTEGER NOT NULL,
            unit            VARCHAR(10) NOT NULL,
            PRIMARY KEY (ingredient_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
        )
        """)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()

def create_ingredient_for_testing(ingredient_name):
    """create a dummy ingredient based on given ingredient name, with id being 0

    Args:
        ingredient_name (string): name of ingredients

    Returns:
        pydict: a pydict of ingredient type
        {
            'ingredient_id': int,
            'ingredient_name': string,
            'quantity': int,
            'unit': string,
        }
    """
    
    return {
        'ingredient_id': 0,
        'ingredient_name': ingredient_name,
        'quantity': 1,
        'unit': ""
    }
    
    
def fetch_recipe_by_id(recipe_id):
    """fetch recipe details by given recipe_id

    Args:
        recipe_id (int): recipe id

    Returns:
        pydict: a dictionary of all columns in recipe table
    """
    # Start connection to database
    conn = connect()
    if not conn:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    cur = conn.cursor()
    query = "SELECT * FROM recipes WHERE recipe_id = %s"
    cur.execute(query, (recipe_id))
    out = cur.fetchall()
    print(out)