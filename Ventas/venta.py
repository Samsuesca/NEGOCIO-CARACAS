from PyQt5.QtWidgets import QMainWindow
from Utils.QtUtils import ShowData
from Ventas.detalles import DetallesVenta
from Ventas.clientes import clients, create_operation

class Venta(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.query = f''' SELECT ventas.id, clientes.nombre,clientes.telefono,ventas.fecha AS fecha,
        ventas.total,ventas.metodo_pago,ventas.observaciones FROM ventas JOIN clientes ON ventas.id_cliente = clientes.id ORDER BY ventas.id DESC;'''
        self.up = main_window
        self.table_name = 'ventas'
        self.filtro = ['nombre','telefono','fecha','total']
        self.ip = self.up.ip
        self.add_row_bool = False

    def openData(self):
        self.show_data = ShowData(main_window=self.up,
                                  table_name=self.table_name,
                                  ip=self.ip,
                                  query=self.query,
                                  add_row=self.add_row_bool,
                                  filtro=self.filtro,
                                  operation='informe')
        return self.show_data    

    def insertData(self): 
        self.id_cliente, self.bool = clients(self,self.table_name)
        if self.bool:
            query = f'''INSERT INTO public.{self.table_name} (id_cliente)
                        VALUES ({self.id_cliente});'''
            self.id_venta = create_operation(parent=self,
                                            query=query,
                                            id_cliente=self.id_cliente,
                                            type=self.table_name)   

    def detalles(self):
        if self.bool:
            self.show_detalles = DetallesVenta(self,self.id_venta[0],f'Venta #{self.id_venta[0]}',self.ip)
            return self.show_detalles
        else:
            return None

        

    

        

        
