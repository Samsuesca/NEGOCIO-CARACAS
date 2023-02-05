from Ventas._clientes import Client

class Venta(Client):
    def __init__(self, main_window):
        super().__init__()
        self.show_query = f''' SELECT ventas.id, clientes.nombre,clientes.telefono,ventas.fecha AS fecha,
        ventas.total,ventas.metodo_pago,ventas.observaciones FROM ventas JOIN clientes ON ventas.id_cliente = clientes.id ORDER BY ventas.id DESC;'''
        self.up = main_window
        self.table_name = 'ventas'
        self.filtro = ['nombre','telefono','total']
        self.ip = self.up.ip
        self.operation = 'informe'
        self.add_row_bool = False

##### prueba github destop
        

    

        

        
