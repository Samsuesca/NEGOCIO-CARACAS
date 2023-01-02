from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from Inventarios.telas import Telas
from Inventarios.confeccion import Confeccion
from Inventarios.bordados import Bordados
from Inventarios.corte import Corte
from Inventarios.empaque import Empaq
from Inventarios.inventa import Inventario
from Utils.style import PushButton
    
class   ShowInventarios(QMainWindow):
        def __init__(self,return_window,to_close):
            super().__init__()
            self.return_window = return_window
            self.to_close = to_close

            label = QLabel("Bienvenido a tu Menú de Inventarios", self)
            label.setAlignment(Qt.AlignCenter)

            btn_back = PushButton("Volver al menú principal", self)
            btn_back.clicked.connect(self.returnToMenu)

             # Agregar los widgets al layout principal de la ventana
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(btn_back, alignment=Qt.AlignCenter)
            
            widget = QWidget(self)
            widget.setLayout(layout)
            self.setCentralWidget(widget)
        
        def returnToMenu(self):
            # Mostrar la ventana del menú principal y cerrar la ventana actual
            self.return_window.show()
            self.to_close.close()

class MenuInventarios(QMainWindow):
    def __init__(self, return_window):
        super().__init__()
        self.return_window = return_window
        self.initUI()

    # Establecer título y tamaño de la ventana
        self.setWindowTitle("Inventarios")
        self.setGeometry(100, 100, 600, 500)  

    
        # Crea una lista para almacenar las ventanas secundarias
        self.secondary_windows = [] 
        
    def initUI(self):
        self.pestanas = QTabWidget(self)
        self.pestanas.addTab(ShowInventarios(self.return_window,self), 'Página Principal')
        self.pestanas.addTab(Telas(self), 'Telas')
        self.pestanas.addTab(Corte(self), 'Corte')
        self.pestanas.addTab(Bordados(), 'Bordados')
        self.pestanas.addTab(Confeccion(), 'Confección')
        self.pestanas.addTab(Empaq(self), 'Empaque')
        self.pestanas.addTab(Inventario(), 'Para Venta')
        self.pestanas.resize(600, 500)
        self.pestanas.move(0, 0)
        self.pestanas.show()   


    def closeEvent(self, event):
        # Itera sobre la lista de ventanas secundarias y ciérralas
        for window in self.secondary_windows:
            window.close()

        # Luego cierra la ventana principal
        super().closeEvent(event)
  
    