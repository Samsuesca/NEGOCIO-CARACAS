'''
Curso de creación de GUIs con Qt5 y Python
 
Author: Kiko Correoso
Website: pybonacci.org 
Licencia: MIT
'''
 
# import os
# os.environ['QT_API'] = 'pyside2'
import sys
from pathlib import Path
 
from PyQt5.QtWidgets import QAction,QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import qtawesome  as qta
 
 
class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self._create_ui()
 
    def _create_ui(self):
        self.resize(500, 300)
        self.move(0, 0)
        self.setWindowTitle('Hola, QMainWindow')
        ruta_icono = Path('.', 'imgs', 'pybofractal.png')
        self.setWindowIcon(QIcon(str(ruta_icono)))
        self.statusBar().showMessage('Ready')
        self._create_menu()
        self.show()
 
    def _create_menu(self):        
        menubar = self.menuBar()
        # File menu and its QAction's
        file_menu = menubar.addMenu('&File')
        exit_action = QAction(qta.icon('fa5.times-circle'),  ## NUEVA LÍNEA
                              '&Exit',  ## NUEVA LÍNEA
                              self) ## NUEVA LÍNEA
        exit_action.setShortcut('Ctrl+Q') ## NUEVA LÍNEA
        exit_action.setStatusTip('Exit application') ## NUEVA LÍNEA
        file_menu.addAction(exit_action) ## NUEVA LÍNEA
        # Help menu and its QAction's
        help_menu = menubar.addMenu('&Help')
        about_action = QAction(qta.icon('fa5s.info-circle'), ## NUEVA LÍNEA 
                               '&Exit',  ## NUEVA LÍNEA
                               self) ## NUEVA LÍNEA
        about_action.setShortcut('Ctrl+I') ## NUEVA LÍNEA
        about_action.setStatusTip('About...') ## NUEVA LÍNEA
        help_menu.addAction(about_action) ## NUEVA LÍNEA
 
if __name__ == '__main__':
 
    app = QApplication(sys.argv)
    w = MiVentana()
    sys.exit(app.exec_())