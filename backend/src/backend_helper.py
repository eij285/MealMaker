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

    if id_db == id_decoded:
        sql_query = "UPDATE users SET last_request = %s WHERE id = %s;"
        cur.execute(sql_query, (datetime.now(tz=timezone.utc), str(id_db)))

        conn.commit()
        cur.close()
        conn.close()

        return id_decoded
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

def fetch_all_with_condition(database, col_name, values):
    """ Fetch info from database using col_name = values
    
    Args:
        database (str): name of database to search from
        col_name (str): which col to search values for
        values (str): values to search for
        
    Return:
        pydict: a pydict with head as column and row data as values
    """
    connection = connect()
    command = "SELECT * FROM " + database + " WHERE " + col_name + " = " + str(values)
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
