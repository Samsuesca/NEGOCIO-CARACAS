from PyQt5.QtWidgets import QMainWindow, QLabel,QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from Utils.data_treat import ShowData
from Utils.style import adj_right, adj_left, PushButton

class Empaq(QMainWindow):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("Este es el inventario Telas!", self)
        label.setAlignment(Qt.AlignCenter)
        show = PushButton("Mostrar Datos", self)
        show.clicked.connect(self.openData)
        
        # Agregar los widgets al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        
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


    

        
 