from PyQt5.QtWidgets import QMainWindow
from Utils.QtUtils import ShowData
from Ventas.detalles import DetallesCambio
from Ventas.clientes import clients, create_operation

class Cambio(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.query = f'''SELECT cambios.id, clientes.nombre,clientes.telefono,cambios.fecha AS fecha,
        cambios.total_entrada,cambios.total_salida,cambios.metodo_pago,cambios.observaciones FROM cambios JOIN clientes ON cambios.id_cliente = clientes.id ORDER BY cambios.id DESC;'''
        self.up = main_window
        self.table_name = 'cambios'
        self.filtro = ['nombre','telefono','fecha','total_entrada','total_salida']
        self.ip = self.up.ip
        self.add_row_bool = False

    def openData(self):
        self.show_data = ShowData(main_window=self.up,
                                  table_name=self.table_name,
                                  ip=self.ip,
                                  query=self.query,
                                  add_row=self.add_row_bool,
                                  filtro=self.filtro)
        return self.show_data    

    def insertData(self): 
        self.id_cliente, self.bool = clients(self,self.table_name)
        if self.bool:
            query = f'''INSERT INTO public.{self.table_name} (id_cliente)
                        VALUES ({self.id_cliente});'''
            self.id_cambio = create_operation(parent=self,
                                            query=query,
                                            id_cliente=self.id_cliente,
                                            type=self.table_name)   
                              
    def detalles(self):
        if self.bool:
            self.show_detalles = DetallesCambio(self,self.id_cambio[0])
            return self.show_detalles
        else:
            return None

        
