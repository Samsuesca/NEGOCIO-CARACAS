from Utils.util_sql import connect, execute_query
from Utils.style import PushButton, adj_left, adj_right,adj_sup_center
from PyQt5.QtWidgets import QDialog, QTableWidget,QTableWidgetItem,QGridLayout,QHBoxLayout, QMainWindow, QMessageBox, QHeaderView,QLabel, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtCore import Qt

class ShowData(QMainWindow):

    def __init__(self,main_window, table_name) -> None:
        super().__init__()
        self.table_name = table_name
        self.main_window = main_window
        self.initUI()
        self.setWindowTitle(f"Visualización de {self.table_name.title()}")
        self.setMinimumSize(400, 250)

    def initUI(self):
        try:    
            # Obtener los datos de la tabla "telas"
            results, column_names = self.get_table_data(self.table_name)
            # Crear la tabla y establecer los encabezados de las columnas
            table = QTableWidget()
            table.setRowCount(len(results))
            table.setColumnCount(len(results[0]))
            table.setHorizontalHeaderLabels(column_names)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


            # Agregar los datos a la tabla
            for i, row in enumerate(results):
                table.setRowCount(i+1)
                for j, col in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(col)))
            
           
            # Ajustar el tamaño de la ventana al tamaño mínimo necesario para mostrar todos sus widgets
            table_width = table.sizeHint().width()
            table_height = table.sizeHint().height()
            
            # Mostrar la tabla en la ventana
            self.setCentralWidget(table)
            self.setGeometry(0,0,table_width, table_height)

            
        except IndexError:
            QMessageBox.warning(self.main_window, 'Error', 'Parece que la tabla que tratas de ver esta vacia')


    def get_table_data(self,table_name):
        conn, cursor = connect()
        results = execute_query(conn,cursor, f'SELECT * FROM {table_name}')
        column_names = [column[0] for column in cursor.description]
        return results, column_names

class Pestana(QMainWindow):
    def __init__(self, main_window, table_name):
        self.main_window = main_window
        self.table_name = table_name
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel(f"Este es el Inventario de {self.table_name.title()}", self)
        label.setAlignment(Qt.AlignCenter)

        # Agregar un botón para mostrar datos
        show = PushButton("Mostrar Datos", self)
        show.clicked.connect(self.openData)

        # # Agregar un botón para editar datos
        edit = PushButton("Editar Datos", self)
        edit.clicked.connect(self.editData)

        # Agregar un botón para insertar datos
        insert = PushButton("Insertar Datos", self)
        insert.clicked.connect(self.insertData)

        # # Agregar un botón para eliminar datos
        delete = PushButton("Eliminar Datos", self)
        delete.clicked.connect(self.deleteData)

        # Agregar los botones al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        layout.addWidget(insert, alignment=Qt.AlignCenter)
        layout.addWidget(delete, alignment=Qt.AlignCenter)
        layout.addWidget(edit, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def openData(self):
        self.show_data = ShowData(self.main_window,self.table_name)
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)


class Ventana(QMainWindow):
    def __init__(self, main_window, table_name):
        self.main_window = main_window
        self.table_name = table_name
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel(f"Este es tu menú para {self.table_name.title()}", self)
        label.setAlignment(Qt.AlignCenter)

        # Agregar un botón para mostrar datos
        show = PushButton(f"Mostrar {self.table_name}", self)
        show.clicked.connect(self.openData)

        # # Agregar un botón para editar 
        edit = PushButton(f"Editar {self.table_name}", self)
        edit.clicked.connect(self.editData)

        # Agregar un botón para insertar 
        insert = PushButton(f"Realizar {self.table_name}", self)
        insert.clicked.connect(self.insertData)

        # # Agregar un botón para eliminar 
        delete = PushButton(f"Eliminar {self.table_name}", self)
        delete.clicked.connect(self.deleteData)

        # # Agregar un botón para volver
        volver = PushButton("Volver", self)
        volver.clicked.connect(self.returnback)

        # Agregar los botones al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        layout.addWidget(insert, alignment=Qt.AlignCenter)
        layout.addWidget(delete, alignment=Qt.AlignCenter)
        layout.addWidget(edit, alignment=Qt.AlignCenter)
        layout.addWidget(volver, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def openData(self):
        self.show_data = ShowData(self.main_window,self.table_name)
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)
    
    def returnback(self):
        # Mostrar la ventana del menú principal y cerrar la ventana actual
        self.main_window.show()
        self.close()


def detalles_venta(self,table_name):
    talla, ok = QInputDialog.getText(self,'¿Qué talla se Necesita?','Ingrese la talla')
    if talla and ok:
        # Conectarse a la base de datos y obtener un cursor
        conn, cursor = connect()
        query = f"SELECT id FROM {table_name} WHERE talla = '{talla}'"
        cursor.execute(query)
        id_prenda = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        #Obtener la cantidad
        quantity, ok1 = QInputDialog.getInt(self,'¿Qué cantidad va a llevar?','Ingrese la cantidad')
        if quantity and ok1:
              #Obtener la cantidad del inventario
            conn, cursor = connect()
            query = f"SELECT cantidad FROM inventario WHERE id_prenda = {id_prenda[0]}"
            cursor.execute(query)
            cantidad_inventario = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()

            if cantidad_inventario[0] >= quantity:
                conn, cursor = connect()
                query = f'''INSERT INTO public.detalle_venta (id_venta,id_prenda,cantidad)
                VALUES ({self.id_venta},{id_prenda[0]},{quantity});'''
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()   
                self.initUI()
            else:
                QMessageBox.about(self, "Error", "No hay inventario")

def informe_venta(id_venta):
    conn, cursor = connect()
    query = f''' SELECT clientes.nombre AS "Nombre del cliente",
                    ventas.fecha AS "Fecha",
                    tipo_prendas.name AS "Nombre de la prenda",
                    prendas.talla AS "Talla",
                    prendas.precio AS "Precio",
                    detalle_venta.cantidad AS "Cantidad",
                    (prendas.precio * detalle_venta.cantidad) AS "Total parcial por prenda",
                    ventas.total AS "Total de la Venta"
                    FROM clientes
                    JOIN ventas ON clientes.id = ventas.id_cliente
                    JOIN detalle_venta ON ventas.id = detalle_venta.id_venta
                    JOIN prendas ON detalle_venta.id_prenda = prendas.id
                    JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
                    WHERE ventas.id = {id_venta}'''
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    informe = QDialog()
    informe.setWindowTitle(f'Informe de venta {id_venta}')
    names = [row[2] for row in result]
    sizes = [row[3] for row in result]
    prices = [row[4] for row in result]
    quant = [row[5] for row in result]
    parcial = [row[6] for row in result]
    # Crear los labels para mostrar los datos
    label_cliente = QLabel(f'Nombre del cliente: {result[0][0]}')
    label_fecha = QLabel(f'Fecha: {result[0][1]}')
    grid = QGridLayout()
    ti_name = QLabel("Prenda") 
    ti_size = QLabel("Talla")
    ti_price = QLabel("Precio")
    ti_quant = QLabel("Cantidad")
    ti_parcial = QLabel("Subtotal")
    grid.addWidget(ti_name,0,0)
    grid.addWidget(ti_size,0,1)
    grid.addWidget(ti_price,0,2)
    grid.addWidget(ti_quant,0,3)
    grid.addWidget(ti_parcial,0,4)
    for i in range(len(names)):
        label_name= QLabel(f'{names[i]}')
        label_size= QLabel(f'{sizes[i]}')
        label_prices= QLabel(f'{prices[i]}')
        label_quant= QLabel(f'{quant[i]}')
        label_parcial= QLabel(f'{parcial[i]}')
        grid.addWidget(label_name,i+1,0)
        grid.addWidget(label_size,i+1,1)
        grid.addWidget(label_prices,i+1,2)
        grid.addWidget(label_quant,i+1,3)
        grid.addWidget(label_parcial,i+1,4)
        # grid_layout.addWidget(button2, 0, 1)
    label_total_venta = QLabel(f'Total de la venta: {result[0][7]}')

    # Crear un layout para organizar los labels
    layout = QVBoxLayout()
    layout.addWidget(label_cliente)
    layout.addWidget(label_fecha)
    layout.addLayout(grid)
    layout.addWidget(label_total_venta)

    #Agregar el widget al layout principal de la ventana
    informe.setLayout(layout)
    adj_sup_center(informe)
    informe.exec_()
    



            
        