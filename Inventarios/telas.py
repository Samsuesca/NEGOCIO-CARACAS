from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from Utils.data_treat import ShowData
from Utils.style import adj_right, adj_left

class Telas(QMainWindow):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel("Este es el Inventario de Telas!", self)
        label.setAlignment(Qt.AlignCenter)

        # Agregar un botón para mostrar datos
        show = QPushButton("Mostrar Datos", self)
        show.clicked.connect(self.openData)

        # Agregar un botón para insertar datos
        insert = QPushButton("Insertar", self)
        insert.clicked.connect(self.insertData)

        # # Agregar un botón para eliminar datos
        # delete = QPushButton("Eliminar", self)
        # delete.clicked.connect(self.deleteData)

        # # Agregar un botón para editar datos
        # edit = QPushButton("Editar", self)
        # edit.clicked.connect(self.editData)

        # Agregar los botones al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        layout.addWidget(insert, alignment=Qt.AlignCenter)
        # layout.addWidget(delete, alignment=Qt.AlignCenter)
        # layout.addWidget(edit, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def openData(self):
        self.show_data = ShowData('telas')
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)

    def insertData(self):
        ShowData('telas').insertData()

    

        
 

