import psycopg2

def connect(password='miakhalifA07',dbname='negocio', user='postgres',host='192.168.0.18'):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host) # U = '10.161.49.171', # MICEL = '192.168.214.173', # HOUSE = '192.168.0.18'
    cursor = conn.cursor()
    return conn, cursor


#Realiza una consulta en la cual se necesitan datos como un resultado
def execute_query(conn,cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
     # Realizar el commit para guardar los cambios
    conn.commit()
    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()
    return results

#No se reciben resultados de la consulta
def make_query(conn,cursor, query):
    cursor.execute(query)
     # Realizar el commit para guardar los cambios
    conn.commit()
    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

def uptade_date(self,ok,date,row_id,col_name):
    if ok and date:
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connect()
        # Construir la consulta para insertar una nueva fila 
        query = f"UPDATE public.{self.table_name} SET {col_name}='{date}' WHERE id={row_id}"
        # Ejecutar la consulta
        make_query(conn,cursor, query)
        self.openData()

def delete_date(self,ok,id):
    # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la eliminación
    if ok and id:
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connect()
        # Construir la consulta para eliminar la fila con el ID especificado
        query = f"DELETE FROM public.{self.table_name} WHERE ID = {id}"
        # Ejecutar la consulta
        make_query(conn,cursor, query)
        self.openData()

def get_id(table_name,row):
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connect()
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = {row}")
        # Realizar el commit para guardar los cambios
        conn.commit()
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()
        return row

