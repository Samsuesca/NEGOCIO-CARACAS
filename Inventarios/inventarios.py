from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from Inventarios.telas import Telas
from Inventarios.confeccion import Confeccion
from Inventarios.bordados import Bordados
from Inventarios.corte import Corte
from Inventarios.empaque import Empaq
from Inventarios.inventa import Inventario


    
class   ShowInventarios(QMainWindow):
        def __init__(self,return_window,to_close):
            super().__init__()
            self.return_window = return_window
            self.to_close = to_close
            label = QLabel("Bienvenido a tu Menú de Inventarios", self)
            label.setAlignment(Qt.AlignCenter)
            btn_back = QPushButton("Volver al menú principal", self)
            btn_back.clicked.connect(self.returnToMenu)
             # Agregar los widgets al layout principal de la ventana
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(btn_back, alignment=Qt.AlignCenter)
            
            widget = QWidget(self)
            widget.setLayout(layout)
            self.setCentralWidget(widget)
        
        def returnToMenu(self):
            # Mostrar la ventana del menú principal y cerrar la ventana actual
            self.return_window.show()
            self.to_close.close()

class MenuInventarios(QMainWindow):
    def __init__(self, return_window):
        super().__init__()
        self.return_window = return_window
        self.initUI()

    # Establecer título y tamaño de la ventana
        self.setWindowTitle("Inventarios")
        self.setGeometry(100, 100, 600, 200)   
        
    def initUI(self):
        self.pestanas = QTabWidget(self)
        self.pestanas.addTab(ShowInventarios(self.return_window,self), 'Página Principal')
        self.pestanas.addTab(Telas(self), 'Telas')
        self.pestanas.addTab(Corte(), 'Corte')
        self.pestanas.addTab(Bordados(), 'Bordados')
        self.pestanas.addTab(Confeccion(), 'Confección')
        self.pestanas.addTab(Empaq(), 'Empaque')
        self.pestanas.addTab(Inventario(), 'Para Venta')
        self.pestanas.resize(600, 200)
        self.pestanas.move(0, 0)
        self.pestanas.show()   
    


    # def optionSelected(self, index):
    #     if index == 0:
            
    #     elif index == 1:
    #         self.openTelas()
    #     elif index == 2:
    #         self.openCorte()
    #     elif index == 3:
    #         self.openBordados()
    #     elif index == 4:
    #         self.openConfeccion()
    #     elif index == 5:
    #         self.openEmpaq()
    #     elif index == 6:
    #         self.openInvVenta()

    # def openTelas(self):
    #     # Cerrar la ventana de bienvenida
    #     self.close()
    #     # Abrir la ventana del menú principal
    #     self.menu_window = Telas(self)
    #     x,y = Utils.style.adj_middle(self.menu_window)
    #     self.menu_window.move(x,y)
    #     self.menu_window.show()

    # def openCorte(self):
    #     # Cerrar la ventana de bienvenida
    #     self.close()
    #     # Abrir la ventana del menú principal
    #     self.menu_window = Corte(self)
    #     x,y = Utils.style.adj_middle(self.menu_window)
    #     self.menu_window.move(x,y)
    #     self.menu_window.show()
    
    # def openBordados(self):
    #     # Cerrar la ventana de bienvenida
    #     self.close()
    #     # Abrir la ventana del menú principal
    #     self.menu_window = Bordados(self)
    #     x,y = Utils.style.adj_middle(self.menu_window)
    #     self.menu_window.move(x,y)
    #     self.menu_window.show()

    # def openConfeccion(self):
    #     # Cerrar la ventana de bienvenida
    #     self.close()
    #     # Abrir la ventana del menú principal
    #     self.menu_window = Confeccion(self)
    #     x,y = Utils.style.adj_middle(self.menu_window)
    #     self.menu_window.move(x,y)
    #     self.menu_window.show()

    # def openEmpaq(self):
    #     # Cerrar la ventana de bienvenida
    #     self.close()
    #     # Abrir la ventana del menú principal
    #     self.menu_window = Empaq(self)
    #     x,y = Utils.style.adj_middle(self.menu_window)
    #     self.menu_window.move(x,y)
    #     self.menu_window.show()

    # def openInvVenta(self):
    #     # Cerrar la ventana de bienvenida
    #     self.close()
    #     # Abrir la ventana del menú principal
    #     self.menu_window = Inventario(self)
    #     x,y = Utils.style.adj_middle(self.menu_window)
    #     self.menu_window.move(x,y)
    #     self.menu_window.show()



    