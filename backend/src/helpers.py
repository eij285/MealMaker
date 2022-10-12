import psycopg2
from config import DB_CONN_STRING

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