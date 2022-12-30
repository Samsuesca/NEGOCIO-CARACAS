from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MenuVentas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("¡Bienvenido al menú 1!", self)
        label.setAlignment(Qt.AlignCenter)
        btn_back = QPushButton("Volver al menú principal", self)
        btn_back.clicked.connect(self.close)
        
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

class MenuInventarios(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("¡Bienvenido al menú 1!", self)
        label.setAlignment(Qt.AlignCenter)
        btn_back = QPushButton("Volver al menú principal", self)
        btn_back.clicked.connect(self.close)
        
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

class MenuBDH(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("¡Bienvenido al menú 1!", self)
        label.setAlignment(Qt.AlignCenter)
        btn_back = QPushButton("Volver al menú principal", self)
        btn_back.clicked.connect(self.close)
        
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

class MenuAnalitica(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida y un botón para volver al menú principal
        label = QLabel("¡Bienvenido al menú 1!", self)
        label.setAlignment(Qt.AlignCenter)
        btn_back = QPushButton("Volver al menú principal", self)
        btn_back.clicked.connect(self.close)
        
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
        
