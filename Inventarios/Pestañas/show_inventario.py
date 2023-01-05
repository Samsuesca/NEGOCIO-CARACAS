from PyQt5.QtWidgets import QMainWindow,QLabel, QWidget,QVBoxLayout, QHBoxLayout,QTextEdit
from PyQt5.QtCore import Qt,QRect
from Utils.style import PushButton, adj_middle, font
from Inventarios.Inventario.inventario import Inventario


class   ShowInventarios(QMainWindow):
        def __init__(self,return_window,to_close):
            super().__init__()
            self.return_window = return_window
            self.to_close = to_close

            label = QLabel('Bienvenido a tu Menú de Inventarios')
            # Creamos un objeto QTextEdit y establecemos su contenido
            text_wel = QTextEdit()
            text_wel.setReadOnly(True)
            text_wel.setHtml(
                   "<p>Este menú contiene diferentes pestañas que te permiten acceder a los menús de inventarios secundarios.</p>"
                   "<p>Además puedes acceder al Menú Principal de Inventarios desde el botón que indica tal acción.</p>"
                   "<p>Igualmente puedes retroceder al menú anterior.</p>")
            font(text_wel,16)

            hbox1 = QHBoxLayout()
            hbox1.addWidget(text_wel)



            inv_btn = PushButton("INVENTARIO PRINCIPAL", self)
            inv_btn.clicked.connect(self.openInventario)
            btn_back = PushButton("Volver al menú principal", self)
            btn_back.clicked.connect(self.returnToMenu)

            
            # layout.addWidget(label)
            # layout.addWidget(text_wel,alignment=Qt.AlignCenter)
            hbox2 = QHBoxLayout()
            hbox2.addWidget(inv_btn, alignment=Qt.AlignCenter)
            hbox2.addWidget(btn_back, alignment=Qt.AlignCenter)
            
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
            self.to_close.close()

        def openInventario(self):
            # Cerrar la ventana de bienvenida
            self.to_close.close()
            # Abrir la ventana del menú principal
            self.menu_window = Inventario(self.to_close)
            x,y = adj_middle(self.menu_window)
            self.menu_window.move(x,y)
            self.menu_window.show()