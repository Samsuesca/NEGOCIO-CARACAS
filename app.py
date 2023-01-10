import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication,QMessageBox, QComboBox, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,  QIcon
from datetime import date
from menu import MenuWindow
from Utils.style import adj_middle, Palette, PushButton
from Utils.QtUtils import show_beg

app = QApplication(sys.argv)
app.setStyle("Fusion")
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
        self.setGeometry(250, 250, 500, 250)
        x,y = adj_middle(self)
        self.move(x,y)
        
        
    def initUI(self):
        # Agregar un mensaje de bienvenida
        label = QLabel("BIENVENIDO A NEGOCIO CARACAS", self)
        label.setAlignment(Qt.AlignCenter)

        # Crear una lista desplegable
        combo = QComboBox()

        # Añadir elementos a la lista
        combo.addItems(["LISTA DE IPS","HOGAR", "UNIVERSIDAD", "DATOS"])

        # Crear una etiqueta para mostrar el elemento seleccionado
        self.label1 = QLabel()
        self.label1.setText("Seleccione una IP")

        # Conectar la señal currentTextChanged con la función update_label
        combo.currentTextChanged.connect(self.label1.setText)
       

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
        layout.addWidget(combo)
        layout.addWidget(self.label1,alignment=Qt.AlignCenter)
        layout.addWidget(btn_menu)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def openMenu(self):
        # Cerrar la ventana de bienvenida
        self.close()
        if self.label1.text()=="HOGAR":
            self.ip = '192.168.0.18'
        elif self.label1.text()=="DATOS":
            self.ip = '192.168.214.173'
        elif self.label1.text()=="UNIVERSIDAD":
            self.ip = '10.161.49.171'
        else: 
            self.ip = ''
            QMessageBox.warning(self,'No puedes continuar','Debes seleccionar una IP')
        
        # Abrir la ventana del menú principal
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
    