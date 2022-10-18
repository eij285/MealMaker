import jwt
import psycopg2
from datetime import datetime, timezone, timedelta
from config import DB_CONN_STRING

def connect():
    """Connect to database

    Returns:
        psycopg2.connect: connection
        None if error
    """
    connection = None
    try:
        print('Conencting to the database...')
        connection = psycopg2.connect(database="meal_maker",host="localhost",user="postgres",password="000000",port="5432")
        #connection =  psycopg2.connect(database="codechefs-db")
        cur = connection.cursor()
        print('PostgreSQL database version: ')
        cur.execute('SELECT version()')
        return connection
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

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
        CREATE TABLE recipe(
            recipe_id SERIAL PRIMARY KEY,
            owner_id SERIAL,
            CONSTRAINT owner_id FOREIGN KEY (owner_id) REFERENCES users(id),
            recipe_name VARCHAR(255) NOT NULL,
            recipe_description VARCHAR(255) NOT NULL,
            methods VARCHAR(255) NOT NULL,
            recipe_status TEXT,
            portion_size INTEGER
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

def remove_recipe_database():
    connection = connect()
    command = ("""
            DROP TABLE recipe CASCADE
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


def database_reset():
    """Resets the database
    
    Drops all tables, stored procedures, triggers, etc and recreates entire
    schema from an sql file

    Returns:
        True if database reset succeeded
        False if database reset failed (requires manual intervention)
    """
    conn = None
    cur = None
    success = False
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        cur.execute(open("schema.sql", "r").read())
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

def files_reset():
    """Files reset
    
    Deletes any files created by the application to reset file content
    back to initial state

    Returns:
        True if file deleted successfully
        False if file deletion failed (requires manual intervention)
    """
    pass