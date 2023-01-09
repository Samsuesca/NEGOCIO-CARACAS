import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,QGridLayout,QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,  QPixmap, QIcon
from datetime import date
from  Inventarios.inventarios import MenuInventarios
from Ventas.ventas import MenuVentas
from BDH.bdh import MenuBDH
from Analitica.analitica import MenuAnalitica
from Utils.style import adj_middle, Palette, PushButton

app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setPalette(Palette())
font = QFont()
font.setPointSize(20)
font.setBold(True)
font.setFamily("Verdana")
app.setFont(font)
app.setWindowIcon(QIcon('icon.png'))

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("INICIO")
        self.setGeometry(250, 250, 500, 250)
        x,y = adj_middle(self)
        self.move(x,y)
        #self.setWindowIcon(QIcon('icon.png'))
        
    def initUI(self):
        # Agregar un mensaje de bienvenida
        label = QLabel("BIENVENIDO A NEGOCIO CARACAS", self)
        label.setAlignment(Qt.AlignCenter)


        today = date.today()
        label_date = QLabel(today.strftime("%B %d, %Y"))
        label_date.setAlignment(Qt.AlignCenter)

        # Agregar un botón para ir al menú principal
        btn_menu = PushButton("Ir al menú principal", self)
        btn_menu.clicked.connect(self.openMenu)
        
        # Agregar los widgets a un layout y establecerlo como el layout principal de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label_date)
        layout.addWidget(btn_menu)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def openMenu(self):
        # Cerrar la ventana de bienvenida
        self.close()
        
        # Abrir la ventana del menú principal
        self.menu_window = MenuWindow()
        x,y = adj_middle(self.menu_window)
        self.menu_window.move(x,y)
        self.menu_window.show()


class MenuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Menú Principal")
        self.setGeometry(400, 500, 600, 250)
        
    def initUI(self):
        # Crear los botones
        button1 = PushButton("VENTAS")
        button1.clicked.connect(self.openVentas)
        button2 = PushButton("INVENTARIOS")
        button2.clicked.connect(self.openInventarios)
        button3 = PushButton("BASES DE DATOS \n   HISTÓRICAS")
        button3.clicked.connect(self.openBDH)
        button4 = PushButton("ANALÍTICA")
        button4.clicked.connect(self.openAnalitica)

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
        self.menu1_window = MenuVentas(self)
        x,y = adj_middle(self.menu1_window)
        self.menu1_window.move(x,y)
        self.menu1_window.show()

        # Cerrar la ventana actual
        self.close()

    def openInventarios(self):
        # Crear una instancia de la ventana del menú  y mostrarla
        self.menu2_window = MenuInventarios(self)
        x,y = adj_middle(self.menu2_window)
        self.menu2_window.move(x,y)
        self.menu2_window.show()
        
        # Cerrar la ventana actual
        self.close()

    def openBDH(self):
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

if __name__ == "__main__":

    # Crea y muestra el splash screen
    splash_pix = QPixmap('icon.png')
    splash = QSplashScreen(
        splash_pix,
        Qt.WindowStaysOnTopHint
    )
    splash.setEnabled(False)
    splash.show()
    # splash.setGeometry(100,100,200,200)
    adj_middle(splash)
 
    # Esto es un simple contador/temporizador para mostrar en pantalla
    # el splash screen. En el futuro haremos que esto sea más útil.
    for i in range(0, 3): 
        msg = ( 
            '<h1><font color="black">' 
             f'Iniciando en {3-i}s' 
             '</font></h1>' 
        ) 
        splash.showMessage( 
            msg, 
            int(Qt.AlignBottom) | int(Qt.AlignHCenter),  
            Qt.black  
        ) 
        time.sleep(1) 
        app.processEvents() 

    welcome_window = WelcomeWindow()
    # splash.finish(welcome_window)
    welcome_window.show()
    sys.exit(app.exec_())