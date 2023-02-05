from Ventas._clientes import Client

class Cambio(Client):
    def __init__(self, main_window):
        super().__init__()
        self.show_query = f'''SELECT cambios.id, clientes.nombre,clientes.telefono,cambios.fecha AS fecha,
        cambios.total_entrada,cambios.total_salida,cambios.finalizado,cambios.observaciones FROM cambios JOIN clientes ON cambios.id_cliente = clientes.id ORDER BY cambios.id DESC;'''
        self.up = main_window
        self.table_name = 'cambios'
        self.operation = 'informe'
        self.filtro = ['nombre','telefono','fecha','total_entrada','total_salida']
        self.ip = self.up.ip
        self.add_row_bool = False


        
