from PyQt5.QtWidgets import QMainWindow,QLabel, QWidget,QVBoxLayout, QHBoxLayout,QGridLayout ,QTextEdit
from PyQt5.QtCore import Qt,QRect
from Ventas.encargo import Encargo
from Ventas.venta import Venta
from Utils.style import PushButton, adj_left,adj_right,adj_middle, font
from Inventarios.Inventario.inventario import Inventario


class   MenuVentas(QMainWindow):
        def __init__(self,return_window):
            super().__init__()
            self.initUI()
            self.return_window = return_window
            self.setGeometry(100,100,700,500)
    
        def initUI(self):
            label = QLabel('Bienvenido a tu Menú de Ventas')
            # Creamos un objeto QTextEdit y establecemos su contenido
            text_wel = QTextEdit()
            text_wel.setReadOnly(True)
            text_wel.setHtml(
                   "<p>En este menú podrás encontrar 4 botones que te permiten acceder a:</p>"
                   "<p>-El primer botón te llevará al menú para realizar una venta</p>"
                    "<p>-El segundo botón te llevará al menú para realizar una encargo</p>"
                    "<p>-El tercer botón te llevará al menú principal de inventarios</p>"
                   "<p>-Igualmente con el último botón, puedes retroceder al menú anterior.</p>")

            font(text_wel,16)

            hbox1 = QHBoxLayout()
            hbox1.addWidget(text_wel)
            
            btn_venta = PushButton("VENTA", self)
            btn_venta.clicked.connect(self.openVenta)
            btn_enc = PushButton("ENCARGO", self)
            btn_enc.clicked.connect(self.openEncargo)
            inv_btn = PushButton("INVENTARIO PRINCIPAL", self)
            inv_btn.clicked.connect(self.openInventario)
            btn_back = PushButton("VOLVER", self)
            btn_back.clicked.connect(self.returnToMenu)

            
            # layout.addWidget(label)
            # layout.addWidget(text_wel,alignment=Qt.AlignCenter)
            hbox2 = QGridLayout()
            hbox2.addWidget(btn_venta,0,0)
            hbox2.addWidget(btn_enc,0,1)
            hbox2.addWidget(inv_btn,1,0)
            hbox2.addWidget(btn_back,1,1)
            
            # Agregar los widgets al layout principal de la ventana
            layout = QVBoxLayout()
            # hbox1.addStretch(1)
            hbox1.setGeometry(QRect(0,0,int(self.width()),350))
            hbox2.setGeometry(QRect(0,0,int(self.width()),100))

            layout.addStretch(0)
            layout.addWidget(label, alignment=Qt.AlignHCenter)
            layout.addStretch(0.1)
            layout.addLayout(hbox1)
            layout.addStretch(0.1)
            layout.addLayout(hbox2)
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)
        
        def returnToMenu(self):
            # Mostrar la ventana del menú principal y cerrar la ventana actual
            self.return_window.show()
            self.close()

        def openInventario(self):
            # Cerrar la ventana 
            x1,y1 = adj_left(self)
            self.move(x1,y1)
            # Abrir la ventana del menú principal
            self.inventario = Inventario(self)
            x,y = adj_right(self.inventario)
            self.inventario.move(x,y)
            self.inventario.show()

        def openVenta(self):
            self.close()
            self.venta = Venta(self,'ventas')
            x,y = adj_middle(self.venta)
            self.venta.move(x,y)
            self.venta.show()

        def openEncargo(self):
            self.close()
            self.encargo = Encargo(self,'encargos')
            x,y = adj_middle(self.encargo)
            self.encargo.move(x,y)
            self.encargo.show()