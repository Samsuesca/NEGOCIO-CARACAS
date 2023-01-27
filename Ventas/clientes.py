from PyQt5.QtWidgets import (QInputDialog,QLineEdit,QMessageBox,
                            QMainWindow,QListWidget,QVBoxLayout,
                            QPushButton,QListWidgetItem,QLabel,
                            QWidget,QFormLayout)
from Utils.util_sql import connectsql, make_query, execute_query
from fuzzywuzzy import fuzz
from Ventas.detalles import DetallesCambio,DetallesEncargo,DetallesVenta
from Utils.QtUtils import ShowData

class Client(QMainWindow):
    def openData(self):
        self.show_data = ShowData(main_window=self.up,
                                  table_name=self.table_name,
                                  ip=self.ip,
                                  query=self.show_query,
                                  add_row=self.add_row_bool,
                                  filtro=self.filtro,
                                  operation=self.operation)
        return self.show_data    
    
    def insertData(self):
            self.client_window = QWidget()
            self.client_window.setWindowTitle("Cliente")  
            label = QLabel(f'Realizar {self.table_name.title()}')
            layout = QFormLayout() 
            self.name_line = QLineEdit("")
            self.phone_line = QLineEdit("3000000000")
            layout.addRow(label)
            layout.addRow('Inserta el nombre del cliente',self.name_line) 
            layout.addRow('Inserta el telefono del cliente',self.phone_line) 
            insert_button = QPushButton("Iniciar")
            insert_button.clicked.connect(self.openLogic)
            layout.addRow(insert_button)
            self.client_window.setLayout(layout)
            self.client_window.show()

    def detalles(self):
        print(self.bool)
        if self.bool:
            self.create_operation()   
            if self.table_name == 'ventas':
                self.show_detalle = DetallesVenta(self,self.id_operation,f'Venta #{self.id_operation}',self.ip)
            elif self.table_name == 'cambios':
                self.show_detalle = DetallesCambio(self,self.id_operation)
            elif self.table_name == 'encargos':
                self.show_detalle = DetallesEncargo(self,self.id_operation)
            else:
                return None
        else:
            pass


    def openLogic(self):
        self.phone = self.phone_line.text()
        self.name = self.name_line.text()
        if self.phone.isdigit() and len(self.phone) == 10:
            # Obtener los clientes existentes
            query1 = "SELECT id, nombre, telefono FROM clientes"
            self.all_clients = execute_query(query1,self.ip)
            print(self.all_clients)
            self.similar_clients = self.get_similar_clients()

            if len(self.similar_clients) == 0 or self.phone == "3000000000":
                conn1, cursor1 = connectsql(host=self.ip)
                # Si el cliente no existe, insertar uno nuevo
                query = f"INSERT INTO public.clientes (nombre, telefono) VALUES ('{self.name}', {int(self.phone)}) RETURNING id"
                cursor1.execute(query)
                result = cursor1.fetchone()
                conn1.commit()
                cursor1.close()
                conn1.close()
                self.cliente = result[0]
                self.bool = True
                self.client_window.close()
                self.detail_window=self.detalles()
            else:
                self.client_window.close()
                self.choose_client()
        else:
            # El número de teléfono no es válido, muestra un mensaje de error y vuelve a mostrar el cuadro de diálogo
            QMessageBox.warning(self, 'Error', 'El número de teléfono debe tener 10 dígitos')
            self.bool = False
            self.cliente = None
        
        
    def choose_client(self):
        self.choose_window = QWidget()
        self.choose_window.setWindowTitle("Clientes Similares")
        # Crear layout principal
        vbox = QVBoxLayout()
        # Crear una lista para mostrar los clientes similares
        self.client_list = QListWidget()
        for client in self.similar_clients:
            item = QListWidgetItem(f"{client[1]} - Tel: {client[2]}")
            self.client_list.addItem(item)
        # Crear un botón para seleccionar un cliente
        self.select_button = QPushButton("Seleccionar")
        self.select_button.clicked.connect(self.select_client)
        # Añadir widgets al layout principal
        vbox.addWidget(QLabel("Se encontraron estos clientes similares en la base de datos, deseas seleccionar alguno?"))
        vbox.addWidget(self.client_list)
        vbox.addWidget(self.select_button)
        # Crear un widget para mostrar el layout principal
       
        self.choose_window.setLayout(vbox)
        self.choose_window.show()
        
    def select_client(self):
        selected_client = self.client_list.currentItem()
        self.cliente = self.similar_clients[self.client_list.row(selected_client)][0]
        self.bool = True
        self.choose_window.close()
        self.detail_window = self.detalles()        
    
    def get_similar_clients(self,st=80):
        similar_clients = []
        for client in self.all_clients:
            id, nombre, telefono = client
            name_similarity = fuzz.token_set_ratio(nombre, self.name)
            phone_similarity = fuzz.token_set_ratio(str(telefono), self.phone)
            if name_similarity > st or phone_similarity > st:
                similar_clients.append((id, nombre, telefono))
        return similar_clients
                
    def create_operation(self):
        self.insert_query = f'''INSERT INTO public.{self.table_name} (id_cliente)
        VALUES ({self.cliente});'''
        conn2, cursor2 = connectsql(host=self.ip)
        make_query(conn2,cursor2,self.insert_query)

        #OBTENER id_encargo:
        conn3, cursor3 = connectsql(host=self.ip)
        query3 = f'''SELECT Max(id) FROM {self.table_name} WHERE id_cliente = {self.cliente}'''
        cursor3.execute(query3)
        self.id_operation= cursor3.fetchone()[0]

        conn3.commit()
        cursor3.close()
        conn3.close()

    def return_window(self):
        return self.detail_window