from Utils.util_sql import connect, execute_query
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QMainWindow,QInputDialog


class ShowData(QMainWindow):

    def __init__(self, table_name) -> None:
        super().__init__()
        self.table_name = table_name
        self.initUI()
        self.setWindowTitle(f"Visualización de {self.table_name}")
        self.setGeometry(250, 250, 500, 250)

    def initUI(self):        
        # Obtener los datos de la tabla "telas"
        results, column_names = self.get_table_data(self.table_name)
        # Crear la tabla y establecer los encabezados de las columnas
        table = QTableWidget()
        table.setRowCount(len(results))
        table.setColumnCount(len(results[0]))
        table.setHorizontalHeaderLabels(column_names)

        # Agregar los datos a la tabla
        for i, row in enumerate(results):
            table.setRowCount(i+1)
            for j, col in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(col)))

        # Mostrar la tabla en la ventana
        self.setCentralWidget(table)

    def get_table_data(self,table_name):
        conn, cursor = connect('negocio2023')
        results = execute_query(cursor, f'SELECT * FROM {table_name}')
        column_names = [column[0] for column in cursor.description]
        return results, column_names

    def insertData(self):
     
        name, ok1 = QInputDialog.getText(self, 'Insertar Tela', 'Ingresa el nombre de la tela:')
        price, ok2 = QInputDialog.getDouble(self, 'Insertar Tela', 'Ingresa el precio por metro:')
        quantity, ok = QInputDialog.getDouble(self, 'Insertar Tela', 'Ingresa la cantidad:')


        # Si el usuario hizo clic en el botón "OK" y proporcionó un nombre válido, continuar con la inserción
        if ok1 and name and ok2 and price and ok and quantity:
            
            # Conectarse a la base de datos y obtener un cursor
            conn, cursor = connect('negocio2023')
            
            
            # Construir la consulta para insertar una nueva fila
            query = f"INSERT INTO public.{self.table_name} (name, precio_mt, cant_metros) VALUES ('{name}', {price}, {quantity})"
            
            # Ejecutar la consulta
            cursor.execute(query)
            
            # Realizar el commit para guardar los cambios
            conn.commit()
            
            # Cerrar la conexión a la base de datos
            cursor.close()
            conn.close()
    