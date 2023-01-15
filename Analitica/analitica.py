from PyQt5.QtWidgets import QInputDialog, QLineEdit,QMessageBox
from Utils.QtUtils import Ventana
from Utils.util_sql import connectsql,make_query,get_id,delete_date

class MenuAnalitica(Ventana):
    def __init__(self,selfis):
        super().__init__(selfis,'movimientos',selfis.ip,True)
        self.up = selfis
        self.initUI()

    def insertData(self):
        category,ok = QInputDialog.getText(self,'Ingresar Movimiento','Tipo de Movimiento',QLineEdit.Normal, "")
        if category and ok:
            description,ok =QInputDialog.getText(self,'Ingresar Movimiento','Ingresa la Descripción',QLineEdit.Normal, "")
            monto, ok1 = QInputDialog.getText(self,'Ingresar Movimiento','Ingresa el Monto',QLineEdit.Normal, "00")
            dest_ori =  QInputDialog.getItem(self,'Ingresar Movimiento','Agrega el origen',['Efectivo','Bancolombia'])
            if description and ok and monto and ok1:
                conn, cursor = connectsql(host=self.up.ip)
                # Construir la consulta para insertar una nueva fila
                query = f"INSERT INTO public.movimientos (descripcion, monto, tipo,destino_origen) VALUES ('{description}',{int(monto)},'{category}','{dest_ori}')"
                # Ejecutar la consulta
                make_query(conn,cursor, query)

    def editData(self):
        pass

    def deleteData(self):
          # Obtener el ID de la fila que se desea eliminar
        row_id, ok = QInputDialog.getInt(self, 'Eliminar Gasto', 'Ingresa el ID que deseas eliminar:')
        if ok and row_id:
            row = get_id(self.table_name,row_id,self.up.ip)
            if row is None:
                QMessageBox.warning(self, 'Error', 'No se encontró ninguna fila con ese ID.')
            else:
                delete_date(self,ok,row_id,self.up.ip)


