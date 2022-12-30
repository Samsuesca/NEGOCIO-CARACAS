import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QTabWidget,QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        # Establece el título y el ícono de la ventana
        self.setWindowTitle('Mi ventana')
        self.setWindowIcon(QIcon('icon.png'))

        # Establece el tamaño y la posición de la ventana
        self.setGeometry(100, 100, 800, 600)



        pestanas = QTabWidget(self)
        pestanas.addTab(Pagina1(), 'Página 1')
        pestanas.addTab(Pagina2(), 'Págipyna 2')
        pestanas.addTab(Pagina3(), 'Página 3')

        pestanas.resize(800, 600)
        pestanas.move(0, 0)
        pestanas.show()

    def mostrar_mensaje(self):
        QMessageBox.information(self, 'Mensaje', 'Hola mundo')

class Pagina1(QWidget):
    def __init__(self):
        super().__init__()

        # Crea widgets y los añade a la página
        etiqueta = QLabel('Hola mundo', self)
        etiqueta.move(100, 100)

class Pagina2(QWidget):
    def __init__(self):
        super().__init__()

        # Crea widgets y los añade a la página
        etiqueta = QLabel('Hola mundo', self)
        etiqueta.move(100, 100)

class Pagina3(QWidget):
    def __init__(self):
        super().__init__()

        # Crea widgets y los añade a la página
        etiqueta = QLabel('Hola mundo', self)
        etiqueta.move(100, 100)
app = QApplication(sys.argv)
ventana = MiVentana()
ventana.show()
sys.exit(app.exec_())