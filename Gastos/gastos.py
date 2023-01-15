from PyQt5.QtWidgets import QInputDialog,QLineEdit,QMessageBox
from Utils.QtUtils import Ventana
from Utils.util_sql import connectsql, make_query,get_id,delete_date

class MenuGastos(Ventana):
    def __init__(self, selfis):
        super().__init__(selfis,'Gastos',selfis.ip,True)
        self.up = selfis
        self.initUI()

    def insertData(self):
        category,ok = QInputDialog.getItem(self,'Ingresar Gasto','Tipo de Gasto',
        ['Telas','Bordados','Confección','Insumos','Compras','Alquiler','Servicios','Trabajo','Transporte'])
        if category and ok:
            description,ok =QInputDialog.getText(self,'Ingresar Gasto','Ingresa la Descripción',QLineEdit.Normal, "")
            monto, ok1 = QInputDialog.getText(self,'Ingresar Gasto','Ingresa el Monto',QLineEdit.Normal, "00")
            details,ok2 = QInputDialog.getText(self,'Ingresar Gasto','Ingresa los Detalles',QLineEdit.Normal, "")
            dest_ori =  QInputDialog.getItem(self,'Ingresar Gasto','Agrega el origen',['Efectivo','Bancolombia'])
            if description and ok and monto and ok1 and details and ok2:
                conn, cursor = connectsql(host=self.up.ip)
                # Construir la consulta para insertar una nueva fila
                query = f"INSERT INTO public.gastos (descripcion, monto, categoria,detalles,metodo_pago) VALUES ('{description}',{int(monto)},'{category}','{details}','{dest_ori}')"
                # Ejecutar la consulta
                make_query(conn,cursor, query)

    def editData(self): ##COMPLETAR
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
        