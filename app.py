#Modulos de Python
import sys
import psycopg2
from pathlib import Path
from datetime import date

#Modulos de Terceros
from PyQt5.QtWidgets import QApplication,QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,  QIcon

#Importaciones Internas
from menu import MenuWindow
from Utils.util_sql import connectsql
from Utils.style import adj_middle, Palette, PushButton,show_beg


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
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("INICIO")
        self.setGeometry(250, 250, 500, 350)
        x,y = adj_middle(self)
        self.move(x,y)
        
        
    def initUI(self):
        # Agregar un mensaje de bienvenida
        label = QLabel("BIENVENIDO A NEGOCIO CARACAS", self)
        label.setAlignment(Qt.AlignCenter)


        today = date.today()
        label_date = QLabel(today.strftime("%B %d, %Y"))
        label_date.setAlignment(Qt.AlignCenter)

        # Agregar un botón para ir al menú principal
        btn_menu = PushButton("Ir al menú principal", self)
        btn_menu.clicked.connect(self.let_ip)
        
        # Agregar los widgets a un layout y establecerlo como el layout principal de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label_date)
        layout.addWidget(btn_menu)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def let_ip(self):
        # if self.label1.text()=="HOGAR":
        self.ip = '127.0.0.1' #'192.168.0.18' #
        try:
            conn, cursor = connectsql(self.ip)
            self.openMenu()
        except psycopg2.OperationalError:
            error = QMessageBox
            error.warning(self,'Error en la Base de Datos','''La Base de Datos no esta corriendo en la IP que seleccionaste. Selecciona otra IP ''')
        
    def openMenu(self):
        # Abrir la ventana del menú principal
        # Cerrar la ventana de bienvenida
        self.close()
        self.menu_window = MenuWindow(self.ip)
        x,y = adj_middle(self.menu_window)
        self.menu_window.move(x,y)
        self.menu_window.show()

if __name__ == "__main__":

    # Crea y muestra el splash screen
    welcome_window = WelcomeWindow()   

    #Ejecutar pantalla de Espera.
    # show_beg(app,welcome_window)
    
    welcome_window.show()
    sys.exit(app.exec_())

    