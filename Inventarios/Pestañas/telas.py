from PyQt5.QtWidgets import QInputDialog, QMessageBox
from Utils.QtUtils import Pestana
from Utils.util_sql import connectsql,make_query, uptade_date, delete_date, get_id

class Telas(Pestana):
    def __init__(self, main_window, table_name,ip):
        super().__init__(main_window, table_name,ip)
        self.ip
    def insertData(self): 
        name, ok1 = QInputDialog.getText(self, 'Insertar Tela', 'Ingresa el nombre de la tela:')
        price, ok2 = QInputDialog.getDouble(self, 'Insertar Tela', 'Ingresa el precio por metro:')
        quantity, ok = QInputDialog.getDouble(self, 'Insertar Tela', 'Ingresa la cantidad:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un nombre válido, continuar con la inserción
        if ok1 and name and ok2 and price and ok and quantity:
            
            # Conectarse a la base de datos y obtener un cursor
            conn, cursor = connectsql(host=self.ip)
            # Construir la consulta para insertar una nueva fila
            query = f"INSERT INTO public.{self.table_name} (name, precio_mt, cant_metros) VALUES ('{name}', {price}, {quantity})"
            # Ejecutar la consulta
            make_query(conn,cursor, query)
            self.openData()

    def editData(self):
        # Obtener el ID de la fila seleccionada
        row_id, ok = QInputDialog.getInt(self, 'Editar Tela', 'Ingresa el ID de la fila que deseas editar:')

        # Si el usuario hizo clic en el botón "OK" y proporcionó un ID válido, continuar con la edición
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                # Solicitar al usuario que ingrese los nuevos valores para cada columna
                name, ok1 = QInputDialog.getText(self, 'Editar Tela', 'Ingresa el nuevo nombre de la tela:')
                price, ok2 = QInputDialog.getDouble(self, 'Editar Tela', 'Ingresa el nuevo precio de la tela:')
                quantity, ok3 = QInputDialog.getDouble(self, 'Editar Tela', 'Ingresa la nueva cantidad de la tela:')
                
                uptade_date(self,ok1,name,row_id,'name',self.ip)
                uptade_date(self,ok2,price,row_id,'precio_mt',self.ip)
                uptade_date(self,ok3,quantity,row_id,'cant_metros',self.ip)            

    def deleteData(self):
        # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Tela', 'Ingresa el ID que deseas eliminar:')
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id,self.ip)
        

    

        

    

        
 

