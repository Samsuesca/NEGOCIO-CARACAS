import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton, QGraphicsAnchorLayout, QGraphicsWidget,QGraphicsView,QGraphicsScene, QGraphicsLayout
from PyQt5.QtCore import Qt
# Crear dos widgets

app = QApplication(sys.argv)

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Establecer título y tamaño de la ventana
        self.setWindowTitle("INICIO")
        self.setGeometry(250, 250, 500, 250)
    def initUI(self):
        # Crear dos widgets
        widget1 = QPushButton("Widget 1")
        widget2 = QPushButton("Widget 2")

        graphicsWidget1 = QGraphicsWidget()
        graphicsWidget1.layout().addWidget(widget1)
        graphicsWidget1.layout().addWidget(widget2)

        # Crear un QGraphicsAnchorLayout y agregar el QGraphicsWidget
        layout = QGraphicsAnchorLayout()
        layout.addAnchor(graphicsWidget1, Qt.AnchorTop, layout, Qt.AnchorTop)

        # Mostrar el QGraphicsWidget en una ventana
        view = QGraphicsView()
        view.setScene(QGraphicsScene(layout))
        view.show()
if __name__ == "__main__":
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())