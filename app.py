#Modulos de Python
import sys
import psycopg2
from pathlib import Path
from datetime import date

#Modulos de Terceros
from PyQt5.QtWidgets import (QApplication,QMessageBox, QMainWindow,
                              QLabel, QVBoxLayout, QWidget,
                              QSplitter,QSizePolicy,QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,  QIcon

#Importaciones Internas
from Utils.QtUtils import delete_widgets
from Ventas.clientes import ClientListView
from Ventas.venta import Venta
from Ventas.encargo import Encargo
from Ventas.cambios import Cambio
from Analitica.movimientos import Movimientos
from Analitica.gastos import Gastos
from Inventarios.Inventario.inventario import Inventario
from Utils.util_sql import connectsql
from Utils.style import Palette, PushButton,show_beg


app = QApplication(sys.argv)
app.setStyle("Windows")
app.setPalette(Palette())
font = QFont()
font.setPointSize(20)
font.setBold(True)
font.setFamily("Verdana")
app.setFont(font)
ruta_icono = Path("icon.png")
app.setWindowIcon(QIcon(str(ruta_icono)))

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ip = '127.0.0.1'
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("INICIO")

    def menu_bar(self):

        menubar = self.menuBar()

        ########Conexión:       
        conect_menu = menubar.addMenu("CLIENTES")
        #realizar:
        self.clients = QAction('Ver', self)
        self.clients.setShortcut("Ctrl+P")
        self.clients.triggered.connect(self.show_clients)
        conect_menu.addAction(self.clients)

        ########VENTAS:       
        venta_menu = menubar.addMenu("VENTAS")
        #realizar:
        self.make_ventas = QAction('Realizar', self)
        self.make_ventas.setShortcut("Ctrl+V")
        self.make_ventas.triggered.connect(self.make_ventas_show)
        #ver:
        self.show_ventas = QAction('Ver', self)
        self.show_ventas.setShortcut("Ctrl+S")
        self.show_ventas.triggered.connect(self.show_ventas_show)
        #add_aactions
        venta_menu.addActions([self.make_ventas,self.show_ventas])

        #######ENCARGO:
        encargo_menu = menubar.addMenu("ENCARGOS")
        #realizar:
        self.make_encargo = QAction('Realizar', self)
        self.make_encargo.setShortcut("Ctrl+E")
        self.make_encargo.triggered.connect(self.make_encargo_show)
        #ver:
        self.show_encargo = QAction('Ver', self)
        self.show_encargo.setShortcut("Ctrl+D")
        self.show_encargo.triggered.connect(self.show_encargo_show)
        #ver:
        self.show_yomber = QAction('Yombers', self)
        self.show_yomber.setShortcut("Ctrl+Y")
        self.show_yomber.triggered.connect(self.show_yomber_show)
        #add_aactions
        encargo_menu.addActions([self.make_encargo,self.show_encargo,self.show_yomber])

        ########CAMBIOS:
        cambio_menu = menubar.addMenu("CAMBIOS")
        #realizar:
        self.make_cambios = QAction('Realizar', self)
        self.make_cambios.setShortcut("Ctrl+K")
        self.make_cambios.triggered.connect(self.make_cambios_show)
        #ver:
        self.show_cambios = QAction('Ver', self)
        self.show_cambios.setShortcut("Ctrl+T")
        self.show_cambios.triggered.connect(self.show_cambios_show)
        #add_aactions
        cambio_menu.addActions([self.make_cambios,self.show_cambios])


        #######MOVIMIENTOS:
        register_menu = menubar.addMenu("REGISTROS")
        ##Movimientos de Efectivo
        self.show_moves = QAction('Movimientos', self)
        self.show_moves.setShortcut("Ctrl+M")
        self.show_moves.triggered.connect(self.movimientos_show)
        ##GASTOS
        self.show_gastos = QAction('Gastos', self)
        self.show_gastos.setShortcut("Ctrl+G")
        self.show_gastos.triggered.connect(self.gastos_show)
        #add_aactions
        register_menu.addActions([self.show_moves,self.show_gastos])

        
        #######iNVENTARIOS:
        inventario_menu = menubar.addMenu("INVENTARIOS")
        ##Movimientos de Efectivo
        self.show_inv = QAction('Inventario Prendas', self)
        self.show_inv.setShortcut("Ctrl+I")
        self.show_inv.triggered.connect(self.inventario_show)
        inventario_menu.addActions([self.show_inv])

        #######iNVENTARIOS:
        check_menu = menubar.addMenu("CHECK")
        ##Movimientos de Efectivo
        self.check = QAction('CONEXION', self)
        self.check.setShortcut("Ctrl+N")
        self.check.triggered.connect(self.check_connection)
        check_menu.addActions([self.check])

    def show_clients(self):
        delete_widgets(self.layoutapp)
        self.clients_window = ClientListView(self)
        self.layoutapp.addWidget(self.clients_window)

    def make_cambios_show(self):
        self.cambio = Cambio(self)
        self.cambio.insertData()

    def show_cambios_show(self):
        delete_widgets(self.layoutapp)
        self.cambio_window = Cambio(self).openData()
        self.layoutapp.addWidget(self.cambio_window)

    def initUI(self):
        
        self.menu_bar()
     
         # Agregar los widgets a un layout 
        self.layoutapp = QVBoxLayout()
        # Agregar un mensaje de bienvenida
        label = QLabel("BIENVENIDO A TU NEGOCIO", self)
        # Agregar un botón para ir al menú principal
        self.layoutapp.addWidget(label, alignment=Qt.AlignCenter)
        today = date.today()
        label_date = QLabel(today.strftime("%B %d, %Y"))
        label_date.setAlignment(Qt.AlignCenter)
        self.layoutapp.addWidget(label_date,alignment=Qt.AlignCenter)

        self.splitter = QSplitter(Qt.Horizontal)
        main_widget = QWidget()
        main_widget.setLayout(self.layoutapp)
        main_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.splitter.addWidget(main_widget)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: rgb(0,100,30); }")
        self.splitter.setSizes([50, 50])
        self.splitter.setHandleWidth(3)

        self.setCentralWidget(self.splitter)
        self.showMaximized()

    def make_ventas_show(self):
        self.venta = Venta(self)
        self.venta.insertData()
   

    def show_ventas_show(self):
        delete_widgets(self.layoutapp)
        self.ventas_window = Venta(self).openData()
        self.layoutapp.addWidget(self.ventas_window)

    def show_yomber_show(self):
        delete_widgets(self.layoutapp)
        self.yombers_window = Encargo(self).showYomber()
        self.layoutapp.addWidget(self.yombers_window)

    def make_encargo_show(self):
        self.encargo = Encargo(self)
        self.encargo.insertData()


    def show_encargo_show(self):
        delete_widgets(self.layoutapp)
        self.encargos_window = Encargo(self).openData()
        self.layoutapp.addWidget(self.encargos_window)

    def inventario_show(self):
        delete_widgets(self.layoutapp)
        self.inventario_window = Inventario(self).openTotal()
        self.layoutapp.addWidget(self.inventario_window)


    def gastos_show(self):
        delete_widgets(self.layoutapp)
        self.gastos_window = Gastos(self).openData()
        self.layoutapp.addWidget(self.gastos_window)

    def movimientos_show(self):
        delete_widgets(self.layoutapp)
        self.moves_window = Movimientos(self).openData()
        self.layoutapp.addWidget(self.moves_window)


    def check_connection(self): #'192.168.0.18' #
        try:
            conn, cursor = connectsql(self.ip) 
            success =  QMessageBox.about(self,'Conexión Exitosa','''Conexión establecida a la Base de Datos, puedes usar la app''')
        except psycopg2.OperationalError:
            error = QMessageBox.warning(self,'Error en la Base de Datos','''La Base de Datos no esta corriendo en la IP que seleccionaste. Selecciona otra IP ''')
        

if __name__ == "__main__":

    # Crea y muestra el splash screen
    welcome_window = WelcomeWindow()   

    #Ejecutar pantalla de Espera.
    # show_beg(app,welcome_window)
    
    welcome_window.show()
    sys.exit(app.exec_())

    