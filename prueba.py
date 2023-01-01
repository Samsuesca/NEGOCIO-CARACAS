# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QTabWidget,QWidget
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt

# class MiVentana(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Establece el título y el ícono de la ventana
#         self.setWindowTitle('Mi ventana')
#         self.setWindowIcon(QIcon('icon.png'))

#         # Establece el tamaño y la posición de la ventana
#         self.setGeometry(100, 100, 800, 600)



#         pestanas = QTabWidget(self)
#         pestanas.addTab(Pagina1(), 'Página 1')
#         pestanas.addTab(Pagina2(), 'Págipyna 2')
#         pestanas.addTab(Pagina3(), 'Página 3')

#         pestanas.resize(800, 600)
#         pestanas.move(0, 0)
#         pestanas.show()

#     def mostrar_mensaje(self):
#         QMessageBox.information(self, 'Mensaje', 'Hola mundo')

# class Pagina1(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Crea widgets y los añade a la página
#         etiqueta = QLabel('Hola mundo', self)
#         etiqueta.move(100, 100)

# class Pagina2(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Crea widgets y los añade a la página
#         etiqueta = QLabel('Hola mundo', self)
#         etiqueta.move(100, 100)

# class Pagina3(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Crea widgets y los añade a la página
#         etiqueta = QLabel('Hola mundo', self)
#         etiqueta.move(100, 100)
# app = QApplication(sys.argv)
# ventana = MiVentana()
# ventana.show()
# sys.exit(app.exec_())


# import sys
# from PyQt5.QtWidgets import QPushButton, QApplication

# class MyObject(QObject):
#     # Declarar la señal personalizada
#     customSignal = pyqtSignal()
    
#     def __init__(self):
#         super().__init__()
        
#         # Crear un botón y conectar su señal "clicked" a un método
#         button = QPushButton("Presiona aquí")
#         button.clicked.connect(self.buttonClicked)
        
#     def buttonClicked(self):
#         # Al presionar el botón, emitir la señal personalizada
#         self.customSignal.emit()

# class MyApp(QApplication):
#     def __init__(self):
#         super().__init__(sys.argv)
#         # Crear un objeto de tipo MyObject
#         obj = MyObject()
        
#         # Conectar la señal personalizada a un método de la aplicación
#         obj.customSignal.connect(self.customSignalReceived)
        
#     def customSignalReceived(self):
#         print("Señal personalizada recibida!")

# # Crear y ejecutar la aplicación
# app = MyApp()
# app.exec_()

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

class  MiWidget(QMainWindow):
    # Declarar la señal
    miSeñal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # Conectar la señal al slot
        self.miSeñal.connect(self.miSlot)
    
    # Declarar el slot
    def miSlot(self):
        print("La señal ha sido emitida")