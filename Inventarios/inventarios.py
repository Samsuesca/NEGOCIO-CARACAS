from PyQt5.QtWidgets import QMainWindow, QTabWidget
from Inventarios.Pestañas.show_inventario import ShowInventarios
from Inventarios.Pestañas.telas import Telas
from Inventarios.Pestañas.confeccion import Confeccion
from Inventarios.Pestañas.bordados import Bordados
from Inventarios.Pestañas.corte import Corte
from Inventarios.Pestañas.empaque import Empaq

    
class MenuInventarios(QMainWindow):
    def __init__(self, return_window):
        super().__init__()
        self.return_window = return_window
        self.initUI()

        # Establecer título y tamaño de la ventana
        self.setWindowTitle("Inventarios")
        self.setGeometry(100, 100, 700, 500)  
    
        # Crea una lista para almacenar las ventanas secundarias
        self.secondary_windows = [] 
        
    def initUI(self):
        #Crear Menu de pestañas
        self.pestanas = QTabWidget(self)
        self.pestanas.addTab(ShowInventarios(self.return_window,self), 'Inicio')
        self.pestanas.addTab(Telas(self,'telas'), 'Telas')
        self.pestanas.addTab(Corte(self,'cortes'), 'Corte')
        self.pestanas.addTab(Bordados(self,'bordados'), 'Bordados')
        self.pestanas.addTab(Confeccion(self,'confeccion'), 'Confección')
        self.pestanas.addTab(Empaq(self,'empaque'), 'Empaque')
        self.pestanas.resize(700, 500)
        self.pestanas.move(0, 0)
        self.pestanas.show()   



