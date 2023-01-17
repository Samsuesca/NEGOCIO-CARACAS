#Modulos de Terceros
from PyQt5.QtWidgets import QMainWindow,QWidget,QGridLayout

#Modulos Internos
from Utils.style import PushButton
from Utils.QtUtils import INFO
from Utils.util_sql import delete_date


class Detalles(QMainWindow):
    def __init__(self, main_window, id_venta,title,ip) -> None:
        super().__init__() 
        self.main_window = main_window
        self.id_venta = id_venta
        self.ti = title
        self.table_name = self.ti.split()[0].lower() + 's'
        self.setWindowTitle(self.ti)
        self.initUI()
        self.ip = ip
        
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
        button8 = PushButton("OTROS")
        button8.clicked.connect(self.openOtros)
        print(type(self.ti))
        button9 = PushButton(f"VER {self.ti.split()[0].upper()}",self)
        button9.clicked.connect(self.openFinalizar)
        button10 = PushButton("CANCELAR")
        button10.clicked.connect(self.cancelar)
    
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
        INFO(self).detalles_venta('camisetas')

    def openChompaAzul(self):
        INFO(self).detalles_venta('chazul')
        
    def openChompaGris(self):
        INFO(self).detalles_venta('chgris')
        
    def openSudaderas(self):
        INFO(self).detalles_venta('sudaderas')
        
    def openJeans(self):
        INFO(self).detalles_venta('jeans')
    
    def openBlusas(self): 
        INFO(self).detalles_venta('blusas')

    def openMedias(self):
        INFO(self).detalles_venta('Medias')
    
    def openOtros(self): ### CONECTAR A ENCARGO
        INFO(self).detalles_venta('otros')

    def openFinalizar(self):
        INFO(self).informe_venta()

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()
    
    
        