import psycopg2
from PyQt5.QtWidgets import (QLabel,QTextEdit,QVBoxLayout,
                             QPushButton,QHBoxLayout,QDialog)
          #conectarse a una base de datos
def connectsql(host):
    conn = psycopg2.connect(dbname='negocio', user='postgres', password='miakhalifA07', host=host) # U = '10.161.49.171', # MICEL = '192.168.214.173', # HOUSE = '192.168.0.18'
    cursor = conn.cursor()
    return conn, cursor

#Realiza una consulta en la cual se necesitan datos como un resultado
def execute_query(query,ip,get_conncur=False):
    conn,cursor = connectsql(ip)
    cursor.execute(query)
    results = cursor.fetchall()
     # Realizar el commit para guardar los cambios
    if get_conncur:
        return results,conn,cursor
    else:
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

#Actualizar una tabla
def uptade_date(self,ok,date,row_id,col_name,ip):
    if ok and date:
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connectsql(host=ip)
        # Construir la consulta para insertar una nueva fila 
        query = f"UPDATE public.{self.table_name} SET {col_name}='{date}' WHERE id={row_id}"
        # Ejecutar la consulta
        make_query(conn,cursor, query)
        self.openData()

#Eliminar de una tabla
def delete_date(self,ok=False,id='',ip=''):
    # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la eliminación
    if ok and id:
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connectsql(host=ip)
        # Construir la consulta para eliminar la fila con el ID especificado
        query = f"DELETE FROM public.{self.table_name} WHERE ID = {id}"
        # Ejecutar la consulta
        make_query(conn,cursor, query)
        try:
            self.openData()
        except AttributeError:
            pass

#Obtener una fila:
def get_id(table_name,row,ip):
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connectsql(host=ip)
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = {row}")
        # Realizar el commit para guardar los cambios
        conn.commit()
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()
        return row

def get_id_prenda(talla,table,ip):
    conn, cursor = connectsql(host=ip)
    query = f"SELECT id FROM {table} WHERE talla = '{talla.upper()}'"
    cursor.execute(query)
    id_prenda = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return id_prenda


class ExecuteSQLWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ip = parent.ip

        # Crea una etiqueta para mostrar un texto para introducir la consulta
        self.label = QLabel("Introduzca la sentencia SQL:")

        # Crea un widget de texto para introducir la consulta
        self.text_edit = QTextEdit()

        # Crea un botón de envío
        self.submit_button = QPushButton("Enviar")
        self.submit_button.clicked.connect(self.submit_query)

        # Crea una layout horizontal para los widgets
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label)
        h_layout.addWidget(self.text_edit)

        # Crea una layout vertical para los widgets
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.submit_button)

        # Establece la layout principal
        self.setLayout(v_layout)

    def submit_query(self):
        # Obtiene la sentencia SQL del widget de texto
        query = self.text_edit.toPlainText()

        # Ejecuta la sentencia SQL en la base de datos
        conn, cursor = connectsql(self.ip)
        make_query(conn, cursor, query)

        # Cierra la ventana
        self.close()