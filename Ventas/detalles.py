from PyQt5.QtWidgets import QMainWindow,QWidget,QGridLayout
from Utils.style import PushButton
from Utils.QtUtils import detalles_venta, informe_venta


class Detalles(QMainWindow):
    def __init__(self, main_window, id_venta) -> None:
        super().__init__() 
        self.main_window = main_window
        self.id_venta = id_venta
        self.initUI()
        
    def initUI(self):
       
        # Crear los botones
        button1 = PushButton("CAMISETAS")
        button1.clicked.connect(self.openCamisetas)
        button2 = PushButton("SUDADERAS")
        button2.clicked.connect(self.openSudaderas)
        button3 = PushButton("CHOMPA AZÚL")
        button3.clicked.connect(self.openChompaAzul)
        button4 = PushButton("CHOMPA GRIS")
        button4.clicked.connect(self.openChompaGris)
        button5 = PushButton("JEANS")
        button5.clicked.connect(self.openJeans)
        button6 = PushButton("BLUSAS")
        button6.clicked.connect(self.openBlusas)
        button7 = PushButton("MEDIAS")
        button7.clicked.connect(self.openMedias)
        button8 = PushButton("YOMBER")
        button8.clicked.connect(self.openYomber)
        button9 = PushButton("FINALIZAR",self)
        button9.clicked.connect(self.openFinalizar)
        button10 = PushButton("CANCELAR")
        button10.clicked.connect(self.openYomber)
    
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
        grid_layout.addWidget(button9, 4, 0)
        grid_layout.addWidget(button10, 4, 1)

        # Agregar el widget al layout principal de la ventana
        widget = QWidget(self)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)

    def openCamisetas(self):
        detalles_venta(self,'camisetas')

    def openChompaAzul(self):
        detalles_venta(self,'chazul')
        

    def openChompaGris(self):
        detalles_venta(self,'chgris')
        
    def openSudaderas(self):
        detalles_venta(self,'sudaderas')
        
    def openJeans(self):
        detalles_venta(self,'jeans')
    
    def openBlusas(self): 
        detalles_venta(self,'blusas')

    def openMedias(self):
        detalles_venta(self,'Medias')
    
    def openYomber(self): ### CONECTAR A ENCARGO
        pass
    def openFinalizar(self):
        informe_venta(self.id_venta)
    
    
        