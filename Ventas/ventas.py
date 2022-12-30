from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import Qt

class MenuVentas(QMainWindow):
    def __init__(self, menu_window):
        super().__init__()
        self.menu_window = menu_window
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("¡Bienvenido al menú 1!", self)
        label.setAlignment(Qt.AlignCenter)
        btn_back = QPushButton("Volver al menú principal", self)
        btn_back.clicked.connect(self.returnToMenu)
        
        # Agregar los widgets al layout principal de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(btn_back, alignment=Qt.AlignRight)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Menú 1")
        self.setGeometry(100, 100, 300, 150)
        
    def returnToMenu(self):
        # Mostrar la ventana del menú principal y cerrar la ventana actual
        self.menu_window.show()
        self.close()

