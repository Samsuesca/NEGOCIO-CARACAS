from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDesktopWidget, QPushButton
from PyQt5.QtGui import QFont

def Palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255,255,255))
    palette.setColor(QPalette.WindowText, QColor(1,100,30))
    palette.setColor(QPalette.Base, QColor(255,230,82))
    palette.setColor(QPalette.AlternateBase, QColor(255,230,82))
    palette.setColor(QPalette.ToolTipBase, QColor(0,100,30))
    palette.setColor(QPalette.ToolTipText, QColor(0,100,30))
    palette.setColor(QPalette.Text, QColor(0,100,30))
    palette.setColor(QPalette.Button, QColor(255,230,82))
    palette.setColor(QPalette.ButtonText, QColor(0,100,30))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(233,33,38))
    palette.setColor(QPalette.Highlight, QColor(233,33,38))
    palette.setColor(QPalette.HighlightedText, QColor(255,255,255))
    return palette

def adj_middle(menu_w):
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
        
    # Calcular la posición para centrar la ventana
    x = (screen_width - menu_w.width()) // 2
    y = (screen_height - menu_w.height()) // 2
    menu_w.move(x,y)
    return x,y
 
def adj_left(menu_w):
    screen = QDesktopWidget().screenGeometry()
    screen_height = screen.height()
    
    # Colocar la ventana en la esquina superior izquierda
    x = 0
    y = (screen_height - menu_w.height()) // 2
    return x,y

def adj_right(menu_w,ratio=1):
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    
    # Colocar la ventana en la esquina superior derecha
    x = screen_width - menu_w.width()//ratio
    y = (screen_height - menu_w.height()) // 2
    menu_w.move(x,y)
    return x,y

def adj_sup_center(window):
    # Obtener el tamaño de la pantalla
    desktop_rect = QDesktopWidget().availableGeometry()

    # Obtener el tamaño de la ventana
    window_rect = window.geometry()

    # Calcular la posición para que la ventana quede en el centro superior
    x = desktop_rect.width() / 2 - window_rect.width() / 2
    y = 0
    # Mover la ventana a la posición calculada
    window.move(x, y)

class PushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("PushButton { min-width: 160px; min-height: 80px; }")

def font(self,scale):
    font = QFont()
    font.setPointSize(scale)
    self.setFont(font)