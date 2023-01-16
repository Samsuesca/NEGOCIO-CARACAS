from PyQt5.QtWidgets import QInputDialog, QMessageBox
from Utils.QtUtils import Pestana
from Utils.util_sql import connectsql, make_query, get_id,uptade_date, delete_date

class Confeccion(Pestana):
    def __init__(self, main_window, table_name,ip):
        super().__init__(main_window, table_name,ip)
        self.ip = ip
    
    def insertData(self): 
        id_prenda, ok = QInputDialog.getInt(self,'Insertar lote en Confección','Insertar el ID de la prenda:')
        quantity, ok1 = QInputDialog.getDouble(self, 'Insertar lote en Confección', 'Ingresa la cantidad:')
        negocio, ok2 = QInputDialog.getText(self, 'Insertar lote en Confección', 'Ingresa el nombre del negocio:')
        # Si el usuario hizo clic en el botón "OK" y proporcionó un nombre válido, continuar con la inserción
        if ok and id_prenda and ok1 and quantity and ok2 and negocio:
            
            # Conectarse a la base de datos y obtener un cursor
            conn, cursor = connectsql(host=self.ip)
            # Construir la consulta para insertar una nueva fila
            query = f"INSERT INTO public.{self.table_name} (id_prenda, cantidad, negocio) VALUES ('{id_prenda}', {quantity}, '{negocio}')"
            # Ejecutar la consulta
            make_query(conn,cursor, query)
            self.openData()


    def editData(self):
        # Obtener el ID de la fila seleccionada
        row_id, ok = QInputDialog.getInt(self, 'Editar Lote', 'Ingresa el ID de la fila que deseas editar:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la edición
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                # Solicitar al usuario que ingrese los nuevos valores para cada columna
                id_prenda, ok = QInputDialog.getInt(self,'Editar lote en Confección','Ingresa el nuevo ID de la prenda:')
                quantity, ok1 = QInputDialog.getDouble(self, 'Editar lote en Confección', 'Ingresa la nueva cantidad:')
                negocio, ok2 = QInputDialog.getText(self, 'Editar lote en Confección', 'Ingresa el nuevo nombre del negocio:')
                
                uptade_date(self,ok,id_prenda,row_id,'id_prenda',self.ip)
                uptade_date(self,ok1,quantity,row_id,'cantidad',self.ip)
                uptade_date(self,ok2,negocio,row_id,'negocio',self.ip)            

    def deleteData(self):
        # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Lote de Confección', 'Ingresa el ID  que deseas eliminar:')
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id,self.ip)
        

    

        
