
#Librerias de terceros
from PyQt5.QtWidgets import QInputDialog, QLineEdit,QMainWindow

#Importaciones internas
from Utils.util_sql import connectsql,make_query
from Utils.QtUtils import ShowData

class Movimientos(QMainWindow):
    def __init__(self,main_window):
        super().__init__()
        self.query = f'''SELECT id,tipo,descripcion,monto,date_trunc('day',fecha) AS fecha,destino_origen
        FROM movimientos ORDER BY id DESC'''
        self.filtro = ['fecha']
        self.up = main_window
        self.table_name = 'movimientos'
        self.ip = self.up.ip
        self.add_row_bool = True

    def openData(self):
        self.show_data = ShowData(main_window=self.up,
                                  table_name=self.table_name,
                                  ip=self.ip,
                                  query=self.query,
                                  add_row=self.add_row_bool,
                                  filtro=self.filtro)
        return self.show_data 


    def insertData(self):
        category,ok = QInputDialog.getText(self,'Ingresar Movimiento','Tipo de Movimiento',QLineEdit.Normal, "")
        if category and ok:
            description,ok =QInputDialog.getText(self,'Ingresar Movimiento','Ingresa la Descripción',QLineEdit.Normal, "")
            monto, ok1 = QInputDialog.getText(self,'Ingresar Movimiento','Ingresa el Monto',QLineEdit.Normal, "00")
            dest_ori, ok2 =  QInputDialog.getItem(self,'Ingresar Movimiento','Agrega el origen',['Efectivo','Bancolombia'])
            if description and ok and monto and ok1 and dest_ori and ok2:
                conn, cursor = connectsql(host=self.up.ip)
                # Construir la consulta para insertar una nueva fila
                query = f"INSERT INTO public.movimientos (descripcion, monto, tipo,destino_origen) VALUES ('{description}',{int(monto)},'{category}','{dest_ori}')"
                # Ejecutar la consulta
                make_query(conn,cursor, query)



