from Utils.util_sql import connect, execute_query
from Utils.style import PushButton, adj_left, adj_right
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QMainWindow, QMessageBox, QHeaderView,QLabel, QVBoxLayout, QWidget
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
        conn, cursor = connect('negocio2023')
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

  
    