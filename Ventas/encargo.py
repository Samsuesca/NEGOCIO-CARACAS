from PyQt5.QtWidgets import QInputDialog, QMessageBox, QLineEdit,QLabel,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt
from Utils.QtUtils import Ventana,ShowData
from Ventas.detalles import DetallesEncargo
from Utils.style import PushButton,adj_left,adj_right
from Utils.util_sql import connectsql, make_query, delete_date, get_id

class Encargo(Ventana):
    def __init__(self, main_window, table_name):
        query = f''' SELECT clientes.nombre,clientes.telefono,date_trunc('day',encargos.fecha_encargo) AS Encargado,
        date_trunc('day',encargos.fecha_entrega) AS EntregarEl,encargos.saldo,
        encargos.metodo_pago FROM encargos JOIN clientes ON encargos.id_cliente = clientes.id ORDER BY encargos.id DESC;'''
        super().__init__(main_window, table_name,main_window.ip,query=query)
        self.up = main_window
        self.ip = self.up.ip

    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel(f"Este es tu menú para {self.table_name.title()}", self)
        label.setAlignment(Qt.AlignCenter)

        # Agregar un botón para mostrar datos
        show = PushButton(f"Mostrar {self.table_name}", self)
        show.clicked.connect(self.openData)

        # Agregar un botón para insertar 
        insert = PushButton(f"Realizar {self.table_name}", self)
        insert.clicked.connect(self.insertData)

         # # Agregar un botón para mostrar yombers 
        yomber = PushButton(f"Mostrar Yombers",self)
        yomber.clicked.connect(self.showYomber)

        # # Agregar un botón para eliminar 
        delete = PushButton(f"Eliminar {self.table_name}", self)
        delete.clicked.connect(self.deleteData)

        # # Agregar un botón para volver
        volver = PushButton("Volver", self)
        volver.clicked.connect(self.returnback)

        # Agregar los botones al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        layout.addWidget(yomber, alignment=Qt.AlignCenter)
        layout.addWidget(insert, alignment=Qt.AlignCenter)
        layout.addWidget(delete, alignment=Qt.AlignCenter)
        layout.addWidget(volver, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def showYomber(self):
        query='SELECT * FROM yombers_encargados;'
        self.show_data = ShowData(self.main_window,'yombers_encargados',self.ip,query)
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)

    def insertData(self): 
        client, ok = QInputDialog.getText(self,'Realizar Encargo','Inserta el nombre del cliente', QLineEdit.Normal, "")
        phone, ok1 = QInputDialog.getText(self, 'Realizar Encargo', 'Inserta el teléfono del cliente', QLineEdit.Normal, "3000000000")
        plazo, ok2 = QInputDialog.getText(self, 'Realizar Encargo', 'Inserta el plazo del encargo', QLineEdit.Normal, "10")
        if phone.isdigit() and len(phone) == 10:

            if  ok and phone and ok1 and plazo and ok2:
                # CREAR CLIENTE
                conn, cursor = connectsql(host=self.ip)
                # Construir la consulta para insertar una nueva fila
                query = f"INSERT INTO public.clientes (nombre, telefono) VALUES ('{client}',{int(phone)})"
                # Ejecutar la consulta
                make_query(conn,cursor, query)

                #OBTENER ID_CLIENTE:
                conn1, cursor1 = connectsql(host=self.ip)
                query1 = f'''SELECT Max(id) FROM clientes WHERE nombre = '{client}' '''
                cursor1.execute(query1)
                id_cliente= cursor1.fetchone()
                conn1.commit()
                cursor1.close()
                conn1.close()
          
                #CREAR VENTA
                conn2, cursor2 = connectsql(host=self.ip)
                query2 = f'''INSERT INTO public.encargos (id_cliente,dias_entrega)
                VALUES ({id_cliente[0]},{plazo});'''
                make_query(conn2,cursor2, query2)
             
                #OBTENER ID_VENTA:
                conn3, cursor3 = connectsql(host=self.ip)
                query3 = f'''SELECT id FROM encargos WHERE id_cliente = {id_cliente[0]}'''
                cursor3.execute(query3)
                id_encargo= cursor3.fetchone()
            
                conn3.commit()
                cursor3.close()
                conn3.close()
                
                #CREAR DETALLE encargo:
                self.detalles(id_encargo[0])
        else:
            # El número de teléfono no es válido, muestra un mensaje de error y vuelve a mostrar el cuadro de diálogo
            QMessageBox.warning(self, 'Error', 'El número de teléfono debe tener 10 dígitos')
               
    def detalles(self,id_encargo):
        self.show_detalles = DetallesEncargo(self,id_encargo,f'Encargo #{id_encargo}',self.ip)

    def deleteData(self):
        # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Encargo', 'Ingresa el ID que deseas eliminar:')
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id,self.ip)
        
