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
