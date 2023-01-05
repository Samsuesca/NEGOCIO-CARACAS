from PyQt5.QtWidgets import QMainWindow,QWidget,QGridLayout, QStackedLayout
from Utils.style import PushButton, adj_left, adj_right
from Utils.QtUtils import ShowData

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
        button1.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(0))
        button2 = PushButton("SUDADERAS")
        button2.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(1))
        button3 = PushButton("CHOMPA AZÚL")
        button3.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(2))
        button4 = PushButton("CHOMPA GRIS")
        button4.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(3))
        button5 = PushButton("JEANS")
        button5.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(4))
        button6 = PushButton("BLUSAS")
        button6.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(5))
        button7 = PushButton("TOTAL")
        button7.clicked.connect(lambda:self.Inv(self).stacked_layout.setCurrentIndex(6))
        button8 = PushButton("VOLVER")
        button8.clicked.connect(self.returnToInvMenu)
    
        # # Crear el layout de la cuadrícula y agregar los botones
        grid_layout = QGridLayout()
        grid_layout.addWidget(button1, 0, 0)
        grid_layout.addWidget(button2, 0, 1)
        grid_layout.addWidget(button3, 1, 0)
        grid_layout.addWidget(button4, 1, 1)
        grid_layout.addWidget(button5, 2, 0)
        grid_layout.addWidget(button6, 2, 1)
        grid_layout.addWidget(button7, 3, 0)
        grid_layout.addWidget(button8, 3, 1)

        # Agregar el widget al layout principal de la ventana
        widget = QWidget(self)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
    
    class Inv(QMainWindow):
        def __init__(self,up) -> QStackedLayout():
            self.stacked_layout = QStackedLayout()
            self.up = up
            super().__init__()
            self.stacked_layout.addWidget(self.openCamisetas())
            self.stacked_layout.addWidget(self.openSudaderas())
            self.stacked_layout.addWidget(self.openChompaAzul())
            self.stacked_layout.addWidget(self.openChompaGris())
            self.stacked_layout.addWidget(self.openBlusas())
            self.stacked_layout.addWidget(self.openJeans())
            self.stacked_layout.addWidget(self.openTotal())
            widget = QWidget(self)
            widget.setLayout(self.stacked_layout)
            self.setMinimumSize(500, 350)
            self.setCentralWidget(widget)
            self.show()

        def openTotal(self):
            show_data = ShowData(self,'total')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.up.move(x,y)
            return show_data

        def openCamisetas(self):
            show_data = ShowData(self,'camisetas')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.move(x,y)
            return show_data

        def openChompaAzul(self):
            show_data = ShowData(self,'chazul')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.up.move(x,y)
            return show_data
        def openChompaGris(self):
            show_data = ShowData(self,'chgris')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.up.move(x,y)
            return show_data
        def openSudaderas(self):
            show_data = ShowData(self,'sudaderas')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.up.move(x,y)
            return show_data
        def openJeans(self):
            show_data = ShowData(self,'jeans')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.up.move(x,y)
            return show_data
        def openBlusas(self):
            show_data = ShowData(self,'blusas')
            x,y = adj_right(show_data)
            show_data.move(x,y)
            show_data.show()
            x,y = adj_left(self)
            self.up.move(x,y)
            return show_data
    
    
    def returnToInvMenu(self):
        # Mostrar la ventana del menú principal y cerrar la ventana actual
        self.return_window.show()
        self.close()
