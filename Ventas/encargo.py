from Utils.QtUtils import ShowData
from Ventas._clientes import Client

class Encargo(Client):
    def __init__(self, main_window):
        super().__init__()
        self.up = main_window
        self.filter = ['fecha_entrega','fecha_encargo']
        self.ip = self.up.ip
        self.table_name = 'encargos'
        self.add_row_bool = False
        self.operation = 'informe'
        self.filtro = ['nombre','telefono','entregarel','saldo','encargado']
        self.show_query = f''' SELECT encargos.id, clientes.nombre,clientes.telefono,
        date_trunc('day',encargos.fecha_encargo) AS Encargado,
        date_trunc('day',encargos.fecha_entrega) AS EntregarEl,
        encargos.saldo,encargos.metodo_pago,encargos.observaciones,encargos.entregado 
        FROM encargos JOIN clientes ON encargos.id_cliente = clientes.id
         ORDER BY encargos.id DESC;'''

    def showYomber(self):
        query='SELECT * FROM yombers_encargados;'
        self.show_yomber = ShowData(main_window=self.up,
                                  table_name='yombers_encargados',
                                  ip=self.ip,
                                  query=query,
                                  add_row=False,
                                  filtro=self.filtro)
        return self.show_yomber

        
