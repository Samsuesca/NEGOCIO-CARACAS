from PyQt5.QtWidgets import (QInputDialog, QMessageBox,
                            QLineEdit,QMainWindow)
from Utils.QtUtils import ShowData
from Ventas.detalles import Detalles
from Utils.util_sql import connectsql, make_query

class Venta(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.query = f''' SELECT ventas.id, clientes.nombre,clientes.telefono,date_trunc('day',ventas.fecha) AS fecha,
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
                                  filtro=self.filtro)
        return self.show_data    

    def insertData(self): 
        client, ok = QInputDialog.getText(self,'Realizar Venta',
                                          'Inserta el nombre del cliente',
                                           QLineEdit.Normal, "")      
        if ok:
            phone, ok1 = QInputDialog.getText(self, 'Realizar Venta',
                                            'Inserta el teléfono del cliente',
                                              QLineEdit.Normal, "3000000000")
            if ok1:
                if phone.isdigit() and len(phone) == 10:
                    # CREAR CLIENTE
                    conn, cursor = connectsql(host=self.ip)
                    # Construir la consulta para insertar una nueva fila
                    query = f'''INSERT INTO public.clientes (nombre, telefono) 
                    VALUES ('{client}',{int(phone)})'''
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
                    query2 = f'''INSERT INTO public.ventas (id_cliente)
                    VALUES ({id_cliente[0]});'''
                    make_query(conn2,cursor2, query2)

                    #OBTENER ID_VENTA:
                    conn3, cursor3 = connectsql(host=self.ip)
                    query3 = f'''SELECT id FROM ventas WHERE id_cliente = {id_cliente[0]}'''
                    cursor3.execute(query3)
                    self.id_venta= cursor3.fetchone()
                
                    conn3.commit()
                    cursor3.close()
                    conn3.close()
                    self.bool = True
                else:
                    # El número de teléfono no es válido, muestra un mensaje de error y vuelve a mostrar el cuadro de diálogo
                    QMessageBox.warning(self, 'Error', 'El número de teléfono debe tener 10 dígitos')
                    self.bool = False
            else:
                self.bool = False
        else: 
            self.bool = False     

    def detalles(self):
        if self.bool:
            self.show_detalles = Detalles(self,self.id_venta[0],f'Venta #{self.id_venta[0]}',self.ip)
            return self.show_detalles
        else:
            return None

        

    

        

        
