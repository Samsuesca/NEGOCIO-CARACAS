from PyQt5.QtWidgets import QInputDialog, QMessageBox
from Utils.QtUtils import Pestana
from Utils.util_sql import connectsql, make_query, uptade_date, delete_date, get_id

class Corte(Pestana):
    def __init__(self, main_window, table_name,ip):
        super().__init__(main_window, table_name,ip)
        self.ip = ip
    def insertData(self): 
        id_prenda, ok = QInputDialog.getInt(self,'Insertar lote en Corte','Insertar el ID de la prenda:')
        quantity, ok1 = QInputDialog.getDouble(self, 'Insertar lote en Corte', 'Ingresa la cantidad:')
        

        # Si el usuario hizo clic en el botón "OK" y proporcionó un nombre válido, continuar con la inserción
        if ok and id_prenda and ok1 and quantity:
            
            # Conectarse a la base de datos y obtener un cursor
            conn, cursor = connectsql(self.ip)
            # Construir la consulta para insertar una nueva fila
            query = f"INSERT INTO public.{self.table_name}(id_prenda, cantidad) VALUES ('{id_prenda}', {quantity})"
            # Ejecutar la consulta
            make_query(conn,cursor, query)
            self.openData()

    def editData(self):
        # Obtener el ID de la fila seleccionada
        row_id, ok = QInputDialog.getInt(self, 'Editar Lote en Corte', 'Ingresa el ID de la fila que deseas editar:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la edición
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                # Solicitar al usuario que ingrese los nuevos valores para cada columna
                id_prenda, ok = QInputDialog.getInt(self,'Editar lote en Corte','Ingresa el nuevo ID de la prenda:')
                quantity, ok1 = QInputDialog.getDouble(self, 'Editar lote en Corte', 'Ingresa la nueva cantidad:')
                uptade_date(self,ok,id_prenda,row_id,'id_prenda',self.ip)
                uptade_date(self,ok1,quantity,row_id,'cantidad',self.ip)
             

    def deleteData(self):
        # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Lote en Corte', 'Ingresa el ID que deseas eliminar:')
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id,self.ip)
        

    

        

        
