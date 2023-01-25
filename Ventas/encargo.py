from PyQt5.QtWidgets import QInputDialog,QMainWindow,QLineEdit
from Utils.QtUtils import ShowData
from Ventas.detalles import DetallesEncargo
from Ventas.clientes import clients, create_operation

class Encargo(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.up = main_window
        self.filter = ['fecha_entrega','fecha_encargo']
        self.ip = self.up.ip
        self.table_name = 'encargos'
        self.add_row_bool = False
        self.filtro = ['nombre','telefono','entregarel','saldo','encargado']
        self.query = f''' SELECT encargos.id, clientes.nombre,clientes.telefono,
        date_trunc('day',encargos.fecha_encargo) AS Encargado,
        date_trunc('day',encargos.fecha_entrega) AS EntregarEl,
        encargos.saldo,encargos.metodo_pago,encargos.observaciones,encargos.entregado 
        FROM encargos JOIN clientes ON encargos.id_cliente = clientes.id
         ORDER BY encargos.id DESC;'''

    def openData(self):
        self.show_data = ShowData(main_window=self.up,
                                  table_name=self.table_name,
                                  ip=self.ip,
                                  query=self.query,
                                  add_row=self.add_row_bool,
                                  filtro=self.filtro)
        return self.show_data

    def insertData(self): 
        plazo, ok2 = QInputDialog.getText(self, 'Realizar Encargo',
                                                       'Inserta el plazo del encargo',
                                                         QLineEdit.Normal, "10")
        if  plazo and ok2:
            self.id_cliente, self.bool = clients(self,self.table_name)
            if self.bool:
                query = f'''INSERT INTO public.{self.table_name} (id_cliente)
                            VALUES ({self.id_cliente});'''
                self.id_encargo = create_operation(parent=self,
                                                query=query,
                                                id_cliente=self.id_cliente,
                                                type=self.table_name)
        else: 
            self.bool = False         

    def detalles(self):
        if self.bool:
            self.show_detalles = DetallesEncargo(self,self.id_encargo[0])
            return self.show_detalles
        else:
            return None
    
    def showYomber(self):
        query='SELECT * FROM yombers_encargados;'
        self.show_yomber = ShowData(main_window=self.up,
                                  table_name='yombers_encargados',
                                  ip=self.ip,
                                  query=query,
                                  add_row=False,
                                  filtro=self.filtro)
        return self.show_yomber

        
