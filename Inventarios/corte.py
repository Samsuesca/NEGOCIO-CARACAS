from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget,QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from Utils.data_treat import ShowData
from Utils.style import adj_right, adj_left, PushButton
from Utils.util_sql import connect, make_query, uptade_date, delete_date, edit_id

class Corte(QMainWindow):
    def __init__(self, main_window):
        self.main_window = main_window
        self.table_name = 'cortes'
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel("Este es el Inventario de Cortes", self)
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
        self.show_data = ShowData(self.main_window,'telas')
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)

    def insertData(self): 
        id, ok1 = QInputDialog.getText(self, 'Insertar Corte', 'Ingresa el ID de la prenda:')
        quantity, ok = QInputDialog.getDouble(self, 'Insertar Corte', 'Ingresa la cantidad:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un nombre válido, continuar con la inserción
        if ok1 and id and ok and quantity:
            
            # Conectarse a la base de datos y obtener un cursor
            conn, cursor = connect('negocio2023')
            # Construir la consulta para insertar una nueva fila
            query = f"INSERT INTO public.{self.table_name} (id_prenda, cantidad) VALUES ('{id}', {quantity})"
            # Ejecutar la consulta
            make_query(conn,cursor, query)
            self.openData()

    def editData(self):
        # Obtener el ID de la fila seleccionada
        row_id, ok = QInputDialog.getInt(self, 'Editar Corte', 'Ingresa el ID de la fila que deseas editar:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la edición
        if ok and row_id:
            row = edit_id(self.table_name,row_id)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                id, ok1 = QInputDialog.getText(self, 'Insertar Corte', 'Ingresa el ID de la prenda:')
                quantity, ok = QInputDialog.getDouble(self, 'Insertar Corte', 'Ingresa la cantidad:')
                uptade_date(self,ok1,id,row_id,'id_prenda')
                uptade_date(self,ok,quantity,row_id,'cantidad')
            

    def deleteData(self):
        # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Tela', 'Ingresa el ID de la tela que deseas eliminar:')
        if ok and row_id:
            row = edit_id(self.table_name,row_id)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id)
        

    

        
