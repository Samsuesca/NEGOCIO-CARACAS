import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,QGridLayout
from PyQt5.QtCore import Qt
from datetime import date
from windows import MenuVentas, MenuInventarios, MenuBDH, MenuAnalitica



class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida
        label = QLabel("BIENVENIDO A NEGOCIO CARACAS", self)
        label.setAlignment(Qt.AlignCenter)


        today = date.today()
        label_date = QLabel(today.strftime("%B %d, %Y"))
        label_date.setAlignment(Qt.AlignCenter)

        # Agregar un botón para ir al menú principal
        btn_menu = QPushButton("Ir al menú principal", self)
        btn_menu.clicked.connect(self.openMenu)
        
        # Agregar los widgets a un layout y establecerlo como el layout principal de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label_date)
        layout.addWidget(btn_menu)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("INICIO")
        self.setGeometry(100, 100, 300, 150)
        
    def openMenu(self):
        # Cerrar la ventana de bienvenida
        self.close()
        
        # Abrir la ventana del menú principal
        self.menu_window = MenuWindow()
        self.menu_window.show()

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):

        # Crear los botones
        button1 = QPushButton("VENTAS")
        button1.clicked.connect(self.openVentas)
        button2 = QPushButton("INVENTARIOS")
        button1.clicked.connect(self.openInventarios)
        button3 = QPushButton("BASES DE DATOS \n   HISTÓRICAS")
        button1.clicked.connect(self.openBDH)
        button4 = QPushButton("ANALÍTICA")
        button1.clicked.connect(self.openAnalitica)
        button1.setFixedSize(200, 100)
        button2.setFixedSize(200, 100)
        button3.setFixedSize(200, 100)
        button4.setFixedSize(200, 100)

        # Crear el layout de la cuadrícula y agregar los botones
        grid_layout = QGridLayout()
        grid_layout.addWidget(button1, 0, 0)
        grid_layout.addWidget(button2, 0, 1)
        grid_layout.addWidget(button3, 1, 0)
        grid_layout.addWidget(button4, 1, 1)
        
        # Agregar el widget al layout principal de la ventana

        widget = QWidget(self)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Menú principal")
        self.setGeometry(400, 500, 600, 250)

    def openVentas(self):
        # Crear una instancia de la ventana del menú 1 y mostrarla
        self.menu1_window = MenuVentas()
        self.menu1_window.show()
        
        # Cerrar la ventana actual
        self.close()

    def openInventarios(self):
        # Crear una instancia de la ventana del menú 1 y mostrarla
        self.menu1_window = MenuInventarios()
        self.menu1_window.show()
        
        # Cerrar la ventana actual
        self.close()

    def openBDH(self):
        # Crear una instancia de la ventana del menú 1 y mostrarla
        self.menu1_window = MenuBDH()
        self.menu1_window.show()
        
        # Cerrar la ventana actual
        self.close()
    def openAnalitica(self):
        # Crear una instancia de la ventana del menú 1 y mostrarla
        self.menu1_window = MenuAnalitica()
        self.menu1_window.show()
        
        # Cerrar la ventana actual
        self.close()

# Crear una aplicación y mostrar la ventana de bienvenida
if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())