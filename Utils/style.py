from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDesktopWidget

def Palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
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

