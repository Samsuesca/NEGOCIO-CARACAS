from PyQt5.QtWidgets import QMainWindow,QWidget,QGridLayout, QStackedLayout
from Utils.style import PushButton, adj_right
from Utils.QtUtils import ShowData

class Inventario(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.up = main_window
        self.ip = self.up.ip
        self.table_name = 'inventario'
        self.add_row_bool = False
        self.operation = 'inventario'
        self.show_query = f'SELECT * FROM total;'
        self.filtro = ['name','talla','precio']
        
    def openTotal(self):
        self.show_data = ShowData(main_window=self.up,
                                    table_name=self.table_name,
                                    ip=self.ip,
                                    query=self.show_query,
                                    add_row=self.add_row_bool,
                                    filtro=self.filtro,
                                    operation=self.operation)
        return self.show_data  