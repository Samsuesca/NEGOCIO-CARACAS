from PyQt5.QtWidgets import (QTableWidget,QLineEdit,QHBoxLayout,
                            QMainWindow,QListWidget,QVBoxLayout,
                            QPushButton,QListWidgetItem,QLabel,
                            QWidget,QGridLayout,QTabWidget)
from PyQt5.QtCore import QSize
from fuzzywuzzy import fuzz
##Internas
from Ventas.encargo import Encargo
from Ventas.venta import Venta
from Ventas.cambios import Cambio
from Utils.QtUtils import ShowData
from Utils.util_sql import execute_query,make_query,connectsql

class ClientListView(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.up = parent
        self.ip = parent.ip     

        #Widgets
        self.label_name = QLabel('Buscar por Nombre')
        self.label_phone = QLabel('Buscar por Telefono')
        self.search_bar_name = QLineEdit('')
        self.search_bar_phone = QLineEdit('')
        self.search_bar_name.textChanged.connect(self.filter_list)
        self.search_bar_phone.textChanged.connect(self.filter_list)
        self.list_view =  QListWidget()
        self.list_view.itemClicked.connect(self.itemClick)
        self.button_new_client = QPushButton('Nuevo Cliente')
        self.button_new_client.clicked.connect(self.new_client)
        self.button_depurar_client = QPushButton('Depurar Clientes')
        self.button_depurar_client.clicked.connect(self.depurar_clientes)
        query1 = "SELECT id, nombre, telefono FROM clientes WHERE nombre != '' AND telefono != '3000000000' ORDER BY nombre "
        self.all_clients = execute_query(query1,self.ip)
        # Populate the list with client names
        self.add_clients(self.all_clients)
        
        grid_box = QGridLayout()
        int_label = QLabel('|')
        grid_box.addWidget(self.label_name,0,0)
        grid_box.addWidget(self.label_phone,0,1)
        grid_box.addWidget(self.search_bar_name,1,0)
        grid_box.addWidget(self.search_bar_phone,1,1)

        layout = QVBoxLayout()
        layout.addLayout(grid_box)
        layout.addWidget(self.list_view)
        layout.addWidget(self.button_new_client)
        layout.addWidget(self.button_depurar_client)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def depurar_clientes(self):
        query = f'''DELETE FROM clientes
        WHERE NOT EXISTS (SELECT * FROM encargos WHERE encargos.id_cliente = clientes.id)
        AND NOT EXISTS (SELECT * FROM ventas WHERE ventas.id_cliente = clientes.id)
        AND NOT EXISTS (SELECT * FROM cambios WHERE cambios.id_cliente = clientes.id) ;'''  
        conn,cursor = connectsql(self.ip)
        make_query(conn,cursor,query)

    def new_client(self):
        from Ventas._clientes import Client
        self.new_cliente = Client(self.ip,False)
        self.new_cliente.insertData()
        if self.new_cliente.cliente is not None:
            self.new_client_id = self.new_cliente.return_client()
            self.window_info(self.new_client_id)
        
    def filter_list(self):
        self.list_view.clear()
        st = [75,60]
        self.similar_clients = []
        self.name = self.search_bar_name.text()
        self.phone = self.search_bar_phone.text()

        if self.name == '' and self.phone == '':
            print('1')
            self.add_clients(self.all_clients)
        elif len(self.name) < 3 and len(self.phone) <3:
            self.add_clients(self.all_clients)
            print('2')
        else:
            print('3')
            for client in self.all_clients:
                id, nombre, telefono = client
                name_similarity = fuzz.token_set_ratio(nombre, self.name)
                if len(self.phone) < 5:
                    phone_similarity = fuzz.token_set_ratio(str(telefono)[0:5], self.phone)
                elif len(self.phone) in range(5,7):
                    phone_similarity = fuzz.token_set_ratio(str(telefono)[0:7], self.phone)
                else:
                    phone_similarity = fuzz.token_set_ratio(str(telefono), self.phone)

                if len(self.name) >= 3 and len(self.phone) > 5:   
                    if name_similarity > st[0] and phone_similarity > st[1]:
                        self.similar_clients.append((id, nombre, telefono))
                else:
                    if name_similarity > st[0] or phone_similarity > st[1]:
                        self.similar_clients.append((id, nombre, telefono))
            self.add_clients(self.similar_clients)
        print('4')

    def add_clients(self,list):
        for client in list:
            item = QListWidgetItem(f"ID: {client[0]} - Nombre: {client[1]} - Tel: {client[2]}")
            self.list_view.addItem(item)

    def itemClick(self, item):
        # Handle item clicked event
        self.selected_client = item.text()
        self.get_client_info()

    def get_client_info(self):
      
        id_and_name,self.client_phone = self.selected_client.split(" - Tel: ")
        # Split the selected client string to get the name and phone number
        id_label, self.client_name = id_and_name.split(" - Nombre: ")
        nomatter_label,self.client_id = id_label.split(" ")

        self.define_querys()

        self.client_data_ventas = execute_query(self.ventas_query, self.ip)
        self.client_data_encargos = execute_query(self.encargos_query, self.ip)
        self.client_data_cambios = execute_query(self.cambios_query, self.ip)
        self.window_info()


    def window_info(self,id=None):
        self.window_ = QMainWindow()
        if id is not None:
            self.client_id = id
            self.define_querys()
            self.client_data_ventas = execute_query(self.ventas_query, self.ip)
            self.client_data_encargos = execute_query(self.encargos_query, self.ip)
            self.client_data_cambios = execute_query(self.cambios_query, self.ip)
        # Labels para mostrar el nombre y teléfono del cliente
        self.label_client_name = QLabel("Nombre: " + self.client_name)
        self.label_client_phone = QLabel("Teléfono: " + self.client_phone)

        # Tab Widget para mostrar los cambios, compras y encargos del cliente
        self.tab_widget = QTabWidget()

        # Tab para cambios
        if len(self.client_data_cambios)>0:
            self.table_cambios = self.openData(self.cambios_query,'cambios')
        else:
            self.table_cambios = QTableWidget()
        self.tab_cambios = QWidget()
        self.button_cambios = QPushButton('Agregar Cambio')
        self.button_cambios.clicked.connect(self.make_cambio)
        layout_cambios = QVBoxLayout()
        layout_cambios.addWidget(self.button_cambios)
        layout_cambios.addWidget(self.table_cambios)
        self.tab_cambios.setLayout(layout_cambios)


        # Tab para compras
        if len(self.client_data_ventas)>0:
            self.table_compras = self.openData(self.ventas_query,'ventas')
        else:
            self.table_compras = QTableWidget()
        self.tab_compras = QWidget()
        self.button_compras = QPushButton('Agregar Venta')
        self.button_compras.clicked.connect(self.make_venta)
        layout_compras = QVBoxLayout()
        layout_compras.addWidget(self.button_compras)
        layout_compras.addWidget(self.table_compras)
        self.tab_compras.setLayout(layout_compras)
        
        # Tab para encargos
        if len(self.client_data_encargos)>0:
            self.table_encargos = self.openData(self.encargos_query,'encargos')
        else:
            self.table_encargos =QTableWidget()
        self.tab_encargos = QWidget()
        self.button_encargos = QPushButton('Agregar Encargo')
        self.button_encargos.clicked.connect(self.make_encargo)
        layout_encargos = QVBoxLayout()
        layout_encargos.addWidget(self.button_encargos)
        layout_encargos.addWidget(self.table_encargos)
        self.tab_encargos.setLayout(layout_encargos)
        
        self.tab_logic()

        hbox = QHBoxLayout()
        hbox.addWidget(self.label_client_name)
        hbox.addWidget(self.label_client_phone)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.tab_widget)
        widget = QWidget()
        widget.setLayout(vbox)
        self.window_.setCentralWidget(widget)
        self.window_.resize(QSize(850,250))
        self.window_.show()

    def make_encargo(self):
        encargo = Encargo(self.up,second=True)
        encargo.openLogic(self.client_id)

    def make_venta(self):
        venta = Venta(self.up,second=True)
        venta.openLogic(self.client_id)

    def make_cambio(self):
        cambio = Cambio(self.up,second=True)
        cambio.openLogic(self.client_id)
        
    def tab_logic(self):

        if len(self.client_data_cambios) >= len(self.client_data_ventas) >= len(self.client_data_encargos):
            self.tab_widget.addTab(self.tab_cambios, "Cambios") 
            self.tab_widget.addTab(self.tab_compras, "Compras")
            self.tab_widget.addTab(self.tab_encargos,"Encargos")   
        elif len(self.client_data_ventas) >= len(self.client_data_encargos) >= len(self.client_data_cambios):
            self.tab_widget.addTab(self.tab_compras, "Compras")
            self.tab_widget.addTab(self.tab_encargos,"Encargos")
            self.tab_widget.addTab(self.tab_cambios, "Cambios")
        else:
            self.tab_widget.addTab(self.tab_encargos,"Encargos")
            self.tab_widget.addTab(self.tab_cambios, "Cambios")
            self.tab_widget.addTab(self.tab_compras, "Compras")
             

    def openData(self,query,table_name):
        if table_name == 'ventas':
            filtro = ['total']
        elif table_name == 'cambios':
            filtro = ['total_entrada','total_salida']
        elif table_name == 'encargos':
            filtro = ['fecha_encargo']
        else:
            filtro = []
        self.show_data = ShowData(main_window=self,
                                  table_name=table_name,
                                  ip=self.ip,
                                  query=query,
                                  add_row=False,
                                  filtro=filtro,
                                  operation = 'informe',
                                  from_client=True)
        return self.show_data.table
    
    def define_querys(self):
        self.ventas_query = f''' SELECT ventas.id, ventas.fecha AS fecha,
        ventas.total,ventas.metodo_pago,ventas.observaciones 
        FROM ventas JOIN clientes
        ON ventas.id_cliente = clientes.id
          WHERE clientes.id = {self.client_id} ORDER BY id DESC;'''
        self.encargos_query = f''' SELECT encargos.id,
        date_trunc('day',encargos.fecha_encargo) AS Encargado,
        date_trunc('day',encargos.fecha_entrega) AS EntregarEl,
        encargos.saldo,encargos.metodo_pago,encargos.observaciones,encargos.entregado 
        FROM encargos JOIN clientes
        ON encargos.id_cliente = clientes.id
        WHERE clientes.id = {self.client_id}
        ORDER BY id DESC;'''
        self.cambios_query = f'''SELECT cambios.id, cambios.fecha AS fecha,
        cambios.total_entrada,cambios.total_salida,cambios.finalizado,cambios.observaciones FROM cambios JOIN clientes
        ON cambios.id_cliente = clientes.id
        WHERE clientes.id = {self.client_id} ORDER BY id DESC;'''