from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QTableWidget,QTableWidgetItem
import Utils.util_sql as uptsql

class MenuInventarios(QMainWindow):
    def __init__(self, menu_window):
        super().__init__()
        self.menu_window = menu_window
        self.initUI()
        
    def initUI(self):
               # Crea el widget QComboBox y lo agrega al layout principal de la ventana
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Selecciona:")
        self.combo_box.addItem("Telas")
        self.combo_box.addItem("Bordados")
        self.combo_box.addItem("Prendas")
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Conecta la señal "currentIndexChanged" del QComboBox con el slot "optionSelected"
        self.combo_box.currentIndexChanged.connect(self.optionSelected)
        
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Inventarios")
        self.setGeometry(100, 100, 300, 150)
    
    def optionSelected(self, index):
        if index == 0:
            self.show_data('telas')
        elif index == 1:
            self.show_data('telas')
        elif index == 2:
            self.show_data('telas')
    
    def get_table_data(self,table_name):
        conn, cursor = uptsql.connect('negocio', 'root', 'negocio2023')
        results = uptsql.execute_query(conn, cursor, f'SELECT * FROM {table_name}')
        column_names = [column[0] for column in cursor.description]
        return results, column_names
    
    def show_data(self,table_name):
        # Obtener los datos de la tabla "telas"
        results, column_names = self.get_table_data(table_name)
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
    