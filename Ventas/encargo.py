from PyQt5.QtWidgets import QInputDialog, QMessageBox
from Utils.QtUtils import Ventana
from Utils.util_sql import connect, make_query, uptade_date, delete_date, get_id

class Encargo(Ventana):
    def __init__(self, main_window, table_name):
        super().__init__(main_window, table_name)


    def insertData(self):
        pass
   
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
        