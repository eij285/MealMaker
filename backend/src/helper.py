import psycopg2
import jwt

def verify_token(token):

    # Connect to database
    try:
        conn = psycopg2.connect("dbname=meal-maker-db")
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
        #TODO: Update last_request in database
        return True
    else:
        return False
