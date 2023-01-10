from PyQt5.QtWidgets import QInputDialog, QMessageBox, QLineEdit
from Utils.QtUtils import Ventana
from Ventas.detalles import Detalles
from Utils.style import adj_right,adj_left
from Utils.util_sql import connect, make_query, uptade_date, delete_date, get_id

class Venta(Ventana):
    def __init__(self, main_window, table_name):
        super().__init__(main_window, table_name)
        
    def insertData(self): 
        client, ok = QInputDialog.getText(self,'Realizar Venta','Inserta el nombre del cliente', QLineEdit.Normal, "")
        phone, ok1 = QInputDialog.getText(self, 'Realizar Venta', 'Inserta el teléfono del cliente', QLineEdit.Normal, "3000000000")
        if phone.isdigit() and len(phone) == 10:

            # El número de teléfono es válido
            email, ok2 = QInputDialog.getText(self,'Realizar Venta','Inserta el correo del cliente',QLineEdit.Normal, "negocio@gmail.com")

            if ok  and ok1  and ok2:
                # CREAR CLIENTE
                conn, cursor = connect()
                # Construir la consulta para insertar una nueva fila
                query = f"INSERT INTO public.clientes (nombre, telefono, correo) VALUES ('{client}',{int(phone)},'{email}')"
                # Ejecutar la consulta
                make_query(conn,cursor, query)


                #OBTENER ID_CLIENTE:
                conn1, cursor1 = connect()
                query1 = f'''SELECT Max(id) FROM clientes WHERE nombre = '{client}' '''
                cursor1.execute(query1)
                id_cliente= cursor1.fetchone()
                conn1.commit()
                cursor1.close()
                conn1.close()

                #CREAR VENTA
                conn2, cursor2 = connect()
                query2 = f'''INSERT INTO public.ventas (id_cliente)
                VALUES ({id_cliente[0]});'''
                make_query(conn2,cursor2, query2)

                #OBTENER ID_VENTA:
                conn3, cursor3 = connect()
                query3 = f'''SELECT id FROM ventas WHERE id_cliente = {id_cliente[0]}'''
                cursor3.execute(query3)
                id_venta= cursor3.fetchone()
            
                conn3.commit()
                cursor3.close()
                conn3.close()
                
                #CREAR DETALLE VENTA:
                self.detalles(id_venta[0])
        else:
            # El número de teléfono no es válido, muestra un mensaje de error y vuelve a mostrar el cuadro de diálogo
            QMessageBox.warning(self, 'Error', 'El número de teléfono debe tener 10 dígitos')
               
    
    def detalles(self,id_venta):
        self.show_detalles = Detalles(self,id_venta,f'Venta #{id_venta}')
        x,y = adj_right(self.show_detalles,1.3)
        self.show_detalles.move(x,y)
        self.show_detalles.show()
        x1,y1 = adj_left(self)
        self.move(x1,y1)


    def editData(self):
        # Obtener el ID de la fila seleccionada
        row_id, ok = QInputDialog.getInt(self, 'Editar Lote en Corte', 'Ingresa el ID de la fila que deseas editar:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la edición
        if ok and row_id:
            row = get_id(self.table_name,row_id)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                # Solicitar al usuario que ingrese los nuevos valores para cada columna
                id_prenda, ok = QInputDialog.getInt(self,'Editar lote en Corte','Ingresa el nuevo ID de la prenda:')
                quantity, ok1 = QInputDialog.getDouble(self, 'Editar lote en Corte', 'Ingresa la nueva cantidad:')
                uptade_date(self,ok,id_prenda,row_id,'id_prenda')
                uptade_date(self,ok1,quantity,row_id,'cantidad')
             

    def deleteData(self):
        # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Lote en Corte', 'Ingresa el ID que deseas eliminar:')
        if ok and row_id:
            row = get_id(self.table_name,row_id)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id)
        

    

        

        
