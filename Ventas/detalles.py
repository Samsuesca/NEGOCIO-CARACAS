#Modulos de Terceros
from PyQt5.QtWidgets import QMainWindow,QWidget,QLineEdit,QInputDialog,QGridLayout,QFormLayout,QMessageBox

#Modulos Internos
from Utils.style import PushButton
from Utils.QtUtils import INFO
from Utils.util_sql import delete_date,connectsql,make_query

def get_id_prenda(talla,table,ip):
     # Conectarse a la base de datos y obtener un cursor
    conn, cursor = connectsql(host=ip)
    query = f"SELECT id FROM {table} WHERE talla = '{talla.upper()}'"
    cursor.execute(query)
    id_prenda = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return id_prenda

def update_metodo_pago(metodo,id_encargo,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''UPDATE encargos SET metodo_pago = '{metodo}' WHERE id = {id_encargo};'''
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()   

def make_detail_encargo(cantidad,id_encargo,id_prenda,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''INSERT INTO detalle_encargo (id_encargo,id_prenda,cantidad)
    VALUES ({id_encargo},{id_prenda[0]},{cantidad});'''
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()   

def update_abono(abono,id_encargo,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''UPDATE encargos SET abono = {abono} WHERE id = {id_encargo};'''
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()   




class Detalles(QMainWindow):
    def __init__(self, main_window, id_venta,title,ip) -> None:
        super().__init__() 
        self.main_window = main_window
        self.id_venta = id_venta
        self.ti = title
        self.table_name= self.ti.split()[0].lower() + 's'
        self.setWindowTitle(self.ti)
        self.initUI()
        self.ip = ip
        
    def initUI(self):
       
        # Crear los botones
        button1 = PushButton("CAMISETAS")
        button1.clicked.connect(self.openCamisetas)
        button2 = PushButton("SUDADERAS")
        button2.clicked.connect(self.openSudaderas)
        button3 = PushButton("CHOMPA AZÚL")
        button3.clicked.connect(self.openChompaAzul)
        button4 = PushButton("CHOMPA GRIS")
        button4.clicked.connect(self.openChompaGris)
        button5 = PushButton("JEANS")
        button5.clicked.connect(self.openJeans)
        button6 = PushButton("BLUSAS")
        button6.clicked.connect(self.openBlusas)
        button7 = PushButton("MEDIAS")
        button7.clicked.connect(self.openMedias)
        button8 = PushButton("OTROS")
        button8.clicked.connect(self.openOtros)
        print(type(self.ti))
        button9 = PushButton(f"VER {self.ti.split()[0].upper()}",self)
        button9.clicked.connect(self.openFinalizar)
        button10 = PushButton("CANCELAR")
        button10.clicked.connect(self.cancelar)
    
        # # Crear el layout de la cuadrícula y agregar los botones
        grid_layout = QGridLayout()
        grid_layout.addWidget(button1, 0, 0)
        grid_layout.addWidget(button2, 0, 1)
        grid_layout.addWidget(button3, 1, 0)
        grid_layout.addWidget(button4, 1, 1)
        grid_layout.addWidget(button5, 2, 0)
        grid_layout.addWidget(button6, 2, 1)
        grid_layout.addWidget(button7, 3, 0)
        grid_layout.addWidget(button8, 3, 1)
        grid_layout.addWidget(button9, 4, 0)
        grid_layout.addWidget(button10, 4, 1)

        # Agregar el widget al layout principal de la ventana
        widget = QWidget(self)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)

    def openCamisetas(self):
        INFO(self).detalles_venta('camisetas')

    def openChompaAzul(self):
        INFO(self).detalles_venta('chazul')
        
    def openChompaGris(self):
        INFO(self).detalles_venta('chgris')
        
    def openSudaderas(self):
        INFO(self).detalles_venta('sudaderas')
        
    def openJeans(self):
        INFO(self).detalles_venta('jeans')
    
    def openBlusas(self): 
        INFO(self).detalles_venta('blusas')

    def openMedias(self):
        INFO(self).detalles_venta('Medias')
    
    def openOtros(self): ### CONECTAR A ENCARGO
        INFO(self).detalles_venta('otros')

    def openFinalizar(self):
        INFO(self).informe_venta()

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()
    
    
class DetallesEncargo():
    def __init__(self, main_window, id_encargo,title,ip) -> None:
        super().__init__() 
        self.main_window = main_window
        self.id_encargo = id_encargo
        self.ti = title
        self.table_name = self.ti.split()[0].lower() + 's'
        self.ip = ip
        self.initUI()
        

    def initUI(self):
        self.prenda, ok = QInputDialog.getItem(self.main_window,'Title','Selecciona el tipo de prenda',
        ['Yomber','Zapatos','Chompa Azul','Chompa Gris','Sudadera',
        'Camiseta','Blusas','Jeans','Medias','Otros'])

        if self.prenda and ok:
            self.logic()
        else:
            self.cancelar
        

    def logic(self):
        ##YOMBER
        if self.prenda == 'Yomber':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    id_prenda = get_id_prenda(talla,'yomber',self.ip)
                    print(id_prenda)
                    print(type(id_prenda))
                    make_detail_encargo(1,self.id_encargo,id_prenda,self.ip)
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        update_abono(abono,self.id_encargo,self.ip)
                        self.openYomber()
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        
        ##ZAPATOS        
        elif self.prenda == 'Zapatos':
            self.tipo,ok2= QInputDialog.getItem(self.main_window,'Tipo Zapato',
                'Selecciona el tipo de Zapato',['Blanco','Negro','Goma'])
            if self.tipo and ok2:
                self.talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
                if self.talla.upper() in self.sizes():
                    if self.talla and ok:
                        self.abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                        if self.abono and ok1:
                            self.openZapatos()
                else:
                    QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        
        ##CHOMPA AZUL
        elif self.prenda == 'Chompa Azul':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openChompaAzul
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        elif self.prenda == 'Chompa Gris':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openChompaGris
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        elif self.prenda == 'Sudadera':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openSudaderas
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        elif self.prenda == 'Camiseta':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openCamisetas
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        elif self.prenda == 'Blusas':          
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openBlusas
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        elif self.prenda == 'Medias':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openMedias
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        elif self.prenda == 'Jeans':
            talla, ok = QInputDialog.getText(self.main_window,'¿Qué talla se Necesita?','Ingrese la talla')
            if talla.upper() in self.sizes():
                if talla and ok:
                    abono,ok1=QInputDialog.getText(self.main_window,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        self.openJeans
            else:
                QMessageBox.about(self.main_window, "Error", "La talla que has seleccionado no existe")
        else:
            QMessageBox.warning(self,'Elección Incorrecta',
            'Debes seleccionar un tipo de prenda válido')
   
    def openZapatos(self):
        def conditional_size(x1,x2,x3):
            if int(self.talla) >= 25 and int(self.talla) <= 32:
                return x1
            elif int(self.talla) >= 33 and int(self.talla) <= 38:
                return x2
            else:
                return x3        
            
        if self.tipo == 'Blanco':
            id_prenda = conditional_size(71,72,73)
            make_detail_encargo(1,self.id_encargo,[id_prenda,0],self.ip)
        elif self.tipo == 'Negro':
            id_prenda = conditional_size(68,69,70)
            make_detail_encargo(1,self.id_encargo,[id_prenda,0],self.ip)
        elif self.tipo == 'Goma':
            id_prenda = conditional_size(74,75,76)
            make_detail_encargo(1,self.id_encargo,[id_prenda,0],self.ip)
        else:
            pass
        update_abono(self.abono,self.id_encargo,self.ip)
    def openCamisetas(self):
        pass
        

    def openChompaAzul(self):
        pass
        
    def openChompaGris(self):
        pass
        
    def openSudaderas(self):
        pass
        
        
    def openJeans(self):
        pass
    
    def openBlusas(self):
        pass 

    def openMedias(self):
        pass

    def openOtros(self):
        pass
    
    def openOtros(self):
        pass ### CONECTAR A ENCARG

    def openFinalizar(self):
        INFO(self).informe_venta()

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()

    def sizes(self):
        if self.prenda == 'Jeans':
            X = ['6','8','10','12','14','16','28','30','32','34']
        elif self.prenda == 'Camisetas':
            X = ['6','8','10','12','14','16','S','M','L','XL','XXL']
        elif self.prenda == 'Yomber' or self.prenda == 'Blusas':
            X = ['6','8','10','12','14','16','S','M','L','XL']
        elif self.prenda == 'Medias':
            X = ['6-8','8-10','9-11']
        elif self.prenda == 'Zapatos':
            X = ['26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44']
        elif self.prenda == 'Otros':
            X = ['TOP','MEDIAS']
        elif self.prenda == 'Sudaderas' or self.prenda == 'Chompa Azul' or self.prenda == 'Chompa Gris':
            X = ['4', '6', '8', '10', '12', '14', '16', 'S', 'M', 'L', 'XL']
        else:
            X = ''
        return X
    
    def openYomber(self):

        self.yomber_window = QWidget()
        self.yomber_window.setWindowTitle("Medidas del Yomber")
        layout = QFormLayout()
        
        self.delantero = QLineEdit()
        self.trasero = QLineEdit()
        self.espalda = QLineEdit()
        self.cintura = QLineEdit()
        self.largo = QLineEdit()
        self.nombre_nina = QLineEdit()
        
        layout.addRow("Nombre de la Niña:", self.nombre_nina)
        layout.addRow("Delantero:", self.delantero)
        layout.addRow("Trasero:", self.trasero)
        layout.addRow("Espalda:", self.espalda)
        layout.addRow("Cintura:", self.cintura)
        layout.addRow("Largo:", self.largo)
        
        
        insert_button = PushButton("Insertar")
        insert_button.clicked.connect(self.insert_yomber)
        
        layout.addRow(insert_button)
        
        self.yomber_window.setLayout(layout)
        self.yomber_window.show()

    
    def insert_yomber(self):
    # Aqui iria el codigo para insertar los datos en la tabla correspondiente
        conn, cursor = connectsql(host=self.ip)
        query = f'''INSERT INTO public.yombers 
        (id_encargo, delantero, trasero, espalda, cintura, largo, nombre_nina)
        VALUES ({self.id_encargo}, {self.delantero.text()}, {self.trasero.text()},
        {self.espalda.text()}, {self.cintura.text()}, {self.largo.text()}, 
        '{self.nombre_nina.text()}')'''
        make_query(conn, cursor, query)
        self.metodo_pago,ok=QInputDialog.getItem(self.yomber_window,'Método de Pago','Selecciona el método de pago',['Efectivo','Transferencia'])
        update_metodo_pago(self.metodo_pago,self.id_encargo,self.ip)
        self.yomber_window.close()
    