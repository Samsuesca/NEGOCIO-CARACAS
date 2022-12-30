from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget,QTableWidgetItem
from PyQt5.QtCore import Qt
from Utils.util_sql  import connect, execute_query

class Inventario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("Este es el inventario Telas!", self)
        label.setAlignment(Qt.AlignCenter)
        show = QPushButton("Mostrar Datos", self)
        show.clicked.connect(self.show_data)
        
        # Agregar los widgets al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_table_data(self,table_name):
        conn, cursor = connect('negocio', 'root', 'negocio2023')
        results = execute_query(conn, cursor, f'SELECT * FROM {table_name}')
        column_names = [column[0] for column in cursor.description]
        return results, column_names
    
    def show_data(self):
        # Obtener los datos de la tabla "telas"
        results, column_names = self.get_table_data('telas')
        # Crear la tabla y establecer los encabezados de las columnas
        table = QTableWidget(self)
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