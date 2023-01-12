from PyQt5.QtWidgets import  QMainWindow, QWidget,QGridLayout
from  Inventarios.inventarios import MenuInventarios
from Ventas.ventas import MenuVentas
from Analitica.analitica import MenuAnalitica
from Gas
from Utils.style import adj_middle, PushButton


class MenuWindow(QMainWindow):

    def __init__(self,ip):
        super().__init__()
        self.initUI()
        self.ip = ip
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Menú Principal")
        self.setGeometry(400, 500, 600, 250)
        
    def initUI(self):
        # Crear los botones
        button1 = PushButton("VENTAS")
        button1.clicked.connect(self.openVentas)
        button2 = PushButton("INVENTARIOS")
        button2.clicked.connect(self.openInventarios)
        button3 = PushButton("GASTOS")
        button3.clicked.connect(self.openGastos)
        # button4 = PushButton("ANALÍTICA")
        # button4.clicked.connect(self.openAnalitica)

        # Crear el layout de la cuadrícula y agregar los botones
        grid_layout = QGridLayout()
        grid_layout.addWidget(button1, 0, 0)
        grid_layout.addWidget(button2, 0, 1)
        # grid_layout.addWidget(button3, 1, 0)
        # grid_layout.addWidget(button4, 1, 1)
        
        # Agregar el widget al layout principal de la ventana
        widget = QWidget(self)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)

    def openVentas(self):
        # Crear una instancia de la ventana del menú 1 y mostrarla
        self.menu1_window = MenuVentas(self,self.ip)
        x,y = adj_middle(self.menu1_window)
        self.menu1_window.move(x,y)
        self.menu1_window.show()

        # Cerrar la ventana actual
        self.close()

    def openInventarios(self):
        # Crear una instancia de la ventana del menú  y mostrarla
        self.menu2_window = MenuInventarios(self,self.ip)
        x,y = adj_middle(self.menu2_window)
        self.menu2_window.move(x,y)
        self.menu2_window.show()
        
        # Cerrar la ventana actual
        self.close()

    def openGastos(self):
        # Crear una instancia de la ventana del menú  y mostrarla
        self.menu3_window = MenuBDH(self)
        x,y = adj_middle(self.menu3_window)
        self.menu3_window.move(x,y)
        self.menu3_window.show()
        
        # Cerrar la ventana actual
        self.close()

    def openAnalitica(self):
        # Crear una instancia de la ventana del menú 1 y mostrarla
        self.menu4_window = MenuAnalitica(self)
        x,y = adj_middle(self.menu4_window)
        self.menu4_window.move(x,y)
        self.menu4_window.show()
        
        # Cerrar la ventana actual
        self.close()