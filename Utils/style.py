from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDesktopWidget, QPushButton

def Palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 100))
    palette.setColor(QPalette.WindowText, QColor(135, 206, 235))
    palette.setColor(QPalette.Base, QColor(176, 224, 230))
    palette.setColor(QPalette.AlternateBase, QColor(0, 0, 100))
    palette.setColor(QPalette.ToolTipBase, QColor(135, 206, 235))
    palette.setColor(QPalette.ToolTipText, QColor(135, 206, 235))
    palette.setColor(QPalette.Text, QColor(0, 0, 139))
    palette.setColor(QPalette.Button, QColor(0, 0, 128))
    palette.setColor(QPalette.ButtonText, QColor(135, 206, 235))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    return palette

def adj_middle(menu_w):
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
        
    # Calcular la posición para centrar la ventana
    x = (screen_width - menu_w.width()) // 2
    y = (screen_height - menu_w.height()) // 2
    return x,y
 
def adj_left(menu_w):
    screen = QDesktopWidget().screenGeometry()
    screen_height = screen.height()
    
    # Colocar la ventana en la esquina superior izquierda
    x = 0
    y = (screen_height - menu_w.height()) // 2
    return x,y

def adj_right(menu_w):
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    
    # Colocar la ventana en la esquina superior derecha
    x = screen_width - menu_w.width()
    y = (screen_height - menu_w.height()) // 2
    return x,y

class PushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("PushButton { min-width: 140px; min-height: 80px; }")

