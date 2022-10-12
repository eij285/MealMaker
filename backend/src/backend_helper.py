import jwt
import psycopg2

def connect():
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
    connection = connect()
    cur = connection.cursor()
    command = ("SELECT token FROM users")
    cur.execute(command)
    out = cur.fetchall()
    connection.close()
    cur.close()
    all_token = out[0]
    return token in all_token

def fetch_user_id_from_token(token):
    connection = connect()
    command = ("SELECT id FROM users WHERE token = %s")
    cur = connection.cursor()
    cur.execute(command, (token,))
    out = cur.fetchall()
    connection.close()
    return out

def fetch_database(database):
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
            out_dict[out_header[k][0]] = out_data[0][j]
        out_list.append(out_dict)
        out_dict = {}
    connection.close()
    cur.close()
    return out_list