import psycopg2

def connect(password,dbname='negocio', user='root'):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host='192.168.0.18')
    cursor = conn.cursor()
    return conn, cursor

def execute_query(cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results

