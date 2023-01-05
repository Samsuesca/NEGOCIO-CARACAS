from PyQt5.QtWidgets import QMainWindow, QLabel,QWidget,QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from Utils.style import PushButton, adj_middle

class   ShowInventarios(QMainWindow):
        def __init__(self,return_window,to_close):
            super().__init__()
            self.return_window = return_window
            self.to_close = to_close

            label = QLabel("Bienvenido a tu Menú de Inventarios", self)
            label.setAlignment(Qt.AlignCenter)


            inv_btn = PushButton("INVENTARIO PRINCIPAL", self)
            inv_btn.clicked.connect(self.openInventario)
            btn_back = PushButton("Volver al menú principal", self)
            btn_back.clicked.connect(self.returnToMenu)

             # Agregar los widgets al layout principal de la ventana
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(inv_btn, alignment=Qt.AlignCenter)
            layout.addWidget(btn_back, alignment=Qt.AlignCenter)
            
            widget = QWidget(self)
            widget.setLayout(layout)
            self.setCentralWidget(widget)
        
        def returnToMenu(self):
            # Mostrar la ventana del menú principal y cerrar la ventana actual
            self.return_window.show()
            self.to_close.close()

        def openInventario(self):
            # Cerrar la ventana de bienvenida
            self.to_close.close()
            # Abrir la ventana del menú principal
            self.menu_window = Inventario(self.to_close)
            x,y = adj_middle(self.menu_window)
            self.menu_window.move(x,y)
            self.menu_window.show()


class Inventario(QMainWindow):
    def __init__(self, return_window):
        super().__init__()
        self.initUI()
        self.return_window = return_window

        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Inventario Principal")
        self.setGeometry(400, 500, 600, 250)
    def initUI(self):

        # Crear los botones
        button1 = PushButton("CAMISETAS")
        # button1.clicked.connect(self.returnToInvMenu)
        button2 = PushButton("SUDADERAS")
        # button2.clicked.connect(self.openInventarios)
        button3 = PushButton("CHOMPA AZÚL")
        # button3.clicked.connect(self.openBDH)
        button4 = PushButton("CHOMPA GRIS")
        # button4.clicked.connect(self.openAnalitica)
        button5 = PushButton("JEANS")
        # button5.clicked.connect(self.openAnalitica)
        button6 = PushButton("BLUSAS")
        # button6.clicked.connect(self.openAnalitica)
    
        # Crear el layout de la cuadrícula y agregar los botones
        grid_layout = QGridLayout()
        grid_layout.addWidget(button1, 0, 0)
        grid_layout.addWidget(button2, 0, 1)
        grid_layout.addWidget(button3, 1, 0)
        grid_layout.addWidget(button4, 1, 1)
        grid_layout.addWidget(button5, 2, 0)
        grid_layout.addWidget(button6, 2, 1)
        
        # Agregar el widget al layout principal de la ventana
        widget = QWidget(self)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
    
    # def returnToInvMenu(self):
    #         # Mostrar la ventana del menú principal y cerrar la ventana actual
    #         self.return_window.show()
    #         self.close()