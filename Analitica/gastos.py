from PyQt5.QtWidgets import (QInputDialog, QMessageBox,
                            QLineEdit,QMainWindow)
from Utils.QtUtils import ShowData
from Utils.util_sql import connectsql, make_query

class Gastos(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.query = f''' SELECT * FROM gastos ORDER BY id DESC;'''
        self.up = main_window
        self.table_name = 'gastos'
        self.filtro = ['fecha']
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
        category,ok = QInputDialog.getItem(self,'Ingresar Gasto','Tipo de Gasto',
        ['Telas','Bordados','Confección','Insumos','Compras','Alquiler','Servicios','Trabajo','Transporte'])
        print(type(category))
        if category and ok:
            description,ok4 =QInputDialog.getText(self,'Ingresar Gasto','Ingresa la Descripción',QLineEdit.Normal, "No aplica")
            if description and ok4:
                try:
                    monto, ok1 = QInputDialog.getText(self,'Ingresar Gasto','Ingresa el Monto',QLineEdit.Normal, "0000")
                except ValueError:
                    error = QMessageBox
                    error.warning(self,'Error',''' El monto debe ser un valor numérico''')
                    monto, ok1 = QInputDialog.getText(self,'Ingresar Gasto','Ingresa el Monto',QLineEdit.Normal, "00.00")
                if monto and ok1:
                    details,ok2 = QInputDialog.getText(self,'Ingresar Gasto','Ingresa los Detalles',QLineEdit.Normal, "No aplica")
                    if details and ok2:
                        dest_ori,ok3 =  QInputDialog.getItem(self,'Ingresar Gasto','Agrega el origen',['Efectivo','Bancolombia'])
                        if  dest_ori and ok3 :
                            conn, cursor = connectsql(host=self.up.ip)
                            # Construir la consulta para insertar una nueva fila
                            query = f'''INSERT INTO public.gastos(descripcion, monto, categoria, detalles, metodo_pago)
                            VALUES ('{description}',{int(monto)},'{category}','{details}','{dest_ori}');'''
                            # Ejecutar la consulta
                            make_query(conn,cursor, query)

