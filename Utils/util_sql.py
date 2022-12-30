import psycopg2

def connect(dbname, user, password):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host='localhost')
    cursor = conn.cursor()
    return conn, cursor

def execute_query(conn, cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results