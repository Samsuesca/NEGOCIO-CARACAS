#Modulos de Terceros
from PyQt5.QtWidgets import (QMainWindow,QWidget,QLineEdit,QInputDialog,
                             QGridLayout,QHBoxLayout,QVBoxLayout,QSpinBox,
                             QFormLayout,QMessageBox,QLabel,QComboBox,
                             QPushButton,QDialog)
from PyQt5.QtCore import Qt
#Modulos Internos
from Utils.style import PushButton,adj_sup_center
from Utils.util_sql import delete_date,connectsql,make_query,get_id_prenda


###PRUEBA 22222 
#3ofsdopfsd


class DetallesVenta(QMainWindow):
    def __init__(self,main_window,id_venta,title='Venta',ip='',info=False) -> None:
        super().__init__() 
        self.main_window = main_window
        self.id_venta = id_venta
        self.ti = title
        self.ip = ip
        self.table_name= self.ti.split()[0].lower() + 's'
        if info==False:
            self.initUI()
            self.show()
        else: 
            pass
   
        
    def initUI(self):
       
        label = QLabel(self.ti)
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
        hbox = QHBoxLayout()
        hbox.addWidget(label,alignment=Qt.AlignCenter) 
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
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(grid_layout)

        # Agregar el widget al layout principal de la ventana
        widget = QWidget(self)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def openCamisetas(self):
        self.detalles_venta('camisetas')

    def openChompaAzul(self):
        self.detalles_venta('chazul')
        
    def openChompaGris(self):
        self.detalles_venta('chgris')
        
    def openSudaderas(self):
        self.detalles_venta('sudaderas')
        
    def openJeans(self):
        self.detalles_venta('jeans')
    
    def openBlusas(self): 
        self.detalles_venta('blusas')

    def openMedias(self):
        self.detalles_venta('Medias')
    
    def openOtros(self): ### CONECTAR A ENCARGO
        self.detalles_venta('otros')

    def openFinalizar(self):
        self.informe_venta()

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()

    def detalles_venta(self,table_name):
        self.table_name=table_name
        try:
            talla, ok = QInputDialog.getItem(self,'¿Qué talla se Necesita?','Ingrese la talla',self.sizes())
        except TypeError:
            QMessageBox.about(self, "Error", "Intentalo de nuevo. Algo salió mal")
        if talla.upper() in self.sizes():
        
            if talla and ok:
                id_prenda = get_id_prenda(talla,self.table_name,self.ip)
                #Obtener la cantidad
                quantity, ok1 = QInputDialog.getInt(self,'¿Qué cantidad va a llevar?','Ingrese la cantidad')
                if quantity and ok1:
                    #Obtener la cantidad del inventario
                    conn, cursor = connectsql(host=self.ip)
                    query = f"SELECT cantidad FROM inventario WHERE id_prenda = {id_prenda[0]}"
                    cursor.execute(query)
                    cantidad_inventario = cursor.fetchone()
                    conn.commit()
                    cursor.close()
                    conn.close()

                    if cantidad_inventario[0] >= quantity:
                        conn, cursor = connectsql(host=self.ip)
                        query = f'''INSERT INTO public.detalle_venta (id_venta,id_prenda,cantidad)
                        VALUES ({self.id_venta},{id_prenda[0]},{quantity});'''
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        conn.close()   
                        self.initUI()
                    else:
                        QMessageBox.about(self, "Error", "No hay inventario")
        else:
            QMessageBox.about(self, "Error", "La talla que has seleccionado no existe")

    def sizes(self):
        if self.table_name == 'jeans':
            X = ['6','8','10','12','14','16','28','30','32','34']
        elif self.table_name == 'camisetas':
            X = ['6','8','10','12','14','16','S','M','L','XL','XXL']
        elif self.table_name == 'yomber' or self.table_name == 'blusas':
            X = ['6','8','10','12','14','16','S','M','L','XL']
        elif self.table_name == 'Medias':
            X = ['4-6','6-8','8-10','9-11','CANILLERA P','CANILLERA G']
        elif self.table_name == 'otros':
            X = ['TOP','CAMISILLAS','BICICLETERO','CORREA']
        elif self.table_name == 'sudaderas' or self.table_name == 'chazul' or self.table_name == 'chgris':
            X = ['4', '6', '8', '10', '12', '14', '16', 'S', 'M', 'L', 'XL']
        else:
            X = ''
        return X

    def informe_venta(self,mode='normal'):
        result = self.query_venta_detalle()
        self.result = result
        self.informe = QDialog()
        self.informe.setWindowTitle(f'Informe de venta {self.id_venta} I.E CARACAS')
        self.informe.setGeometry(0,0,550,400)
        self.names = [row[3] for row in result]
        self.sizes = [row[4] for row in result]
        self.prices = [row[5] for row in result]
        self.quant = [row[6] for row in result]
        self.parcial = [row[7] for row in result]
        self.id_det = [row[9] for row in result]
        # Crear los labels para mostrar los datos
        try:
            label_title = QLabel(f'Uniformes Consuelo Rios')
            label_cliente = QLabel(f'Nombre del cliente: {result[0][0]} | ID_VENTA: ({result[0][1]})')
            label_fecha = QLabel(f'Fecha: {result[0][2]}')
            grid = QGridLayout()
            ti_name = QLabel("Prenda") 
            ti_size = QLabel("Talla")
            ti_price = QLabel("Precio")
            ti_quant = QLabel("Cantidad")
            ti_parcial = QLabel("Subtotal")
            ti_spa = [QLabel("|") for i in range(4)]
            grid.addWidget(ti_name,0,0,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[0],0,1,alignment=Qt.AlignCenter)
            grid.addWidget(ti_size,0,2,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[1],0,3,alignment=Qt.AlignCenter)
            grid.addWidget(ti_price,0,4,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[2],0,5,alignment=Qt.AlignCenter)
            grid.addWidget(ti_quant,0,6,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[3],0,7,alignment=Qt.AlignCenter)
            grid.addWidget(ti_parcial,0,8,alignment=Qt.AlignCenter)
            for i in range(len(self.names)):
                label_name= QLabel(f'{self.names[i]}')
                label_size= QLabel(f'{self.sizes[i]}')
                label_prices= QLabel(f'{self.prices[i]}')
                label_quant= QSpinBox()
                label_quant.setMinimum(0)
                label_quant.setValue(self.quant[i])
                self.id_detalle = self.id_det[i]
                label_quant.valueChanged.connect(self.actualizar_cantidad)
                label_parcial= QLabel(f'{self.parcial[i]}')
                grid.addWidget(label_name,i+1,0,alignment=Qt.AlignCenter)
                grid.addWidget(label_size,i+1,2,alignment=Qt.AlignCenter)
                grid.addWidget(label_prices,i+1,4,alignment=Qt.AlignCenter)
                grid.addWidget(label_quant,i+1,6,alignment=Qt.AlignCenter)
                grid.addWidget(label_parcial,i+1,8,alignment=Qt.AlignCenter)
            grid2 = QGridLayout()
            label_total_venta = QLabel(f'Total de la venta: {result[0][8]}')
            grid2.addWidget(label_total_venta,0,0,alignment=Qt.AlignCenter)

            # Define el ancho de las columnas
            grid.setColumnStretch(0, 2)
            grid.setColumnStretch(1, 0.2)
            grid.setColumnStretch(2, 1)
            grid.setColumnStretch(3, 0.2)
            grid.setColumnStretch(4, 2)
            grid.setColumnStretch(5, 0.2)
            grid.setColumnStretch(6, 1)
            grid.setColumnStretch(7, 0.2)
            grid.setColumnStretch(8, 2)
            

            #si el modo del informe son observaciones
            if mode == 'normal':
                hbox = QHBoxLayout()
                save = PushButton("GUARDAR VENTA")
                save.clicked.connect(self.save_venta)
                hbox.addWidget(save)

            # Crear un layout para organizar los labels
            layout = QVBoxLayout()
            layout.addWidget(label_title,alignment=Qt.AlignCenter)
            layout.addWidget(label_cliente)
            layout.addWidget(label_fecha)
            layout.addLayout(grid)
            layout.addLayout(grid2)
            #si el modo del informe son observaciones
            if mode == 'normal':
                layout.addLayout(hbox)

            #Agregar el widget al layout principal de la ventana
            self.informe.setLayout(layout)
            adj_sup_center(self.informe)
            self.informe.exec_()

        except IndexError:
            QMessageBox.about(self,"Error", "No se han añadido prendas a la venta")

    def actualizar_cantidad(self,value):
        conn,cur = connectsql(host=self.ip)
        # Actualizar la cantidad en la tabla detalle_venta.
        query = f'''UPDATE detalle_venta SET cantidad={value} WHERE id={self.id_detalle}'''
        make_query(conn,cur,query)

        self.informe.accept()
        self.informe_venta()


    def save_venta(self):
        
        obs,ok1 = QInputDialog.getText(self,'Observaciones','¿Deseas agregar observaciones?',QLineEdit.Normal, "Sin obs")
        if obs and ok1:
            conn,cur = connectsql(host=self.ip)
            query = f'''UPDATE public.ventas SET observaciones='{obs}' WHERE id = {self.id_venta}'''
            make_query(conn,cur,query)
        else:
            self.informe.accept()
            self.up.close()    

        metodo,ok = QInputDialog.getItem(self,'Método de Pago','Selecciona el método de pago',['Efectivo','Transferencia'])
        if metodo and ok:
            conn,cur = connectsql(host=self.ip)
            query = f'''UPDATE public.ventas SET finalizada=true,metodo_pago='{metodo}' WHERE id = {self.id_venta}'''
            make_query(conn,cur,query)
            self.informe.accept()
            self.close()   
        else:
            QMessageBox.about(self,"Error", "Debes seleccionar un método de pago")
            self.informe.accept()
            self.up.close()    

    def query_venta_detalle(self):  
        conn, cursor = connectsql(host=self.ip)
        query = f''' SELECT clientes.nombre AS "Nombre del cliente",
                        ventas.id AS "ID",
                        ventas.fecha AS "Fecha",
                        tipo_prendas.name AS "Nombre de la prenda",
                        prendas.talla AS "Talla",
                        prendas.precio AS "Precio",
                        detalle_venta.cantidad AS "Cantidad",
                        (prendas.precio * detalle_venta.cantidad) AS "Total parcial por prenda",
                        ventas.total AS "Total de la Venta",
                        detalle_venta.id AS "ID_DETALLE"
                        FROM clientes
                        JOIN ventas ON clientes.id = ventas.id_cliente
                        JOIN detalle_venta ON ventas.id = detalle_venta.id_venta
                        JOIN prendas ON detalle_venta.id_prenda = prendas.id
                        JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
                        WHERE ventas.id = {self.id_venta}
                        ORDER BY detalle_venta.id'''
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close() 
        return result   

    
    
class DetallesEncargo(QMainWindow):
    def __init__(self, main_window, id_encargo,info=False) -> None:
        super().__init__() 
        self.up = main_window
        self.id_encargo = id_encargo
        self.ip = self.up.ip
        self.prendas = ['Yomber','Zapatos B','Zapatos N','Zapatos G','Chompa Azul','Chompa Gris','Sudaderas',
        'Camisetas','Blusas','Jeans','Medias','Otros']
        if info:
            pass
        else:
            self.initUI()
            self.show()
        

    def initUI(self):
        self.plazo,ok1 =  QInputDialog.getText(self, 'Realizar Encargo',
                                                       'Inserta el plazo del encargo',
                                                         QLineEdit.Normal, "10")
        if self.plazo and ok1:   
            self.prenda, ok = QInputDialog.getItem(self.up,'Title',
            'Selecciona el tipo de prenda',self.prendas)

            if self.prenda and ok:
                self.logic()
            else:
                self.cancelar
        else: 
            QMessageBox.about(self.up, "Error", "Intentalo de nuevo")
            
    def logic(self):
        ##YOMBER
        if self.prenda == 'Yomber':
            self.talla, ok = QInputDialog.getItem(self,'¿Qué talla se Necesita?','Ingrese la talla',self.sizes())
    
            if ok:
                if self.talla.upper() in self.sizes():
                    self.id_prenda = get_id_prenda(self.talla,'yomber',self.ip)
                    self.make_detail_encargo()
                    self.abono,ok1=QInputDialog.getText(self.up,'Abono','¿Cuánto va a abonar?')
                    if self.abono and ok1:
                        self.update_abono()
                        self.openYomber()
                else:
                    QMessageBox.about(self.up, "Error", "La talla que has seleccionado no existe, intentalo de nuevo")

        ##ZAPATOS        
        elif self.prenda == 'Zapatos B':
            self.talla,self.abono=self.get_size_and_abono(self.openZapatoBlanco)
        elif self.prenda == 'Zapatos N':
            self.talla,self.abono=self.get_size_and_abono(self.openZapatoNegro)
        elif self.prenda == 'Zapatos G':
            self.talla,self.abono=self.get_size_and_abono(self.openZapatoGoma)
        
        ##CHOMPA AZUL
        elif self.prenda == 'Chompa Azul':
            self.talla,self.abono=self.get_size_and_abono(self.openChompaAzul)
        ##CHOMPA GRIS        
        elif self.prenda == 'Chompa Gris':
            self.talla,self.abono=self.get_size_and_abono(self.openChompaGris)  
        ##SUDADERA        
        elif self.prenda == 'Sudaderas':
            self.talla,self.abono=self.get_size_and_abono(self.openSudaderas)
        ##CAMISETA        
        elif self.prenda == 'Camisetas':
            self.talla,self.abono=self.get_size_and_abono(self.openCamiseta)
        ##BLUSAS
        elif self.prenda == 'Blusas':          
            self.talla,self.abono=self.get_size_and_abono(self.openBlusas)
        ##MEDIAS        
        elif self.prenda == 'Medias':
            self.talla,self.abono=self.get_size_and_abono(self.openMedias)
                    
        ##JEANS        
        elif self.prenda == 'Jeans':
            self.talla,self.abono=self.get_size_and_abono(self.openJeans)
            
        else:
            QMessageBox.warning(self,'Elección Incorrecta',
            'Debes seleccionar un tipo de prenda válido')
            self.initUI()

    def make_detail_encargo(self):
        conn, cursor = connectsql(host=self.ip)
        query = f'''INSERT INTO detalle_encargo (id_encargo,id_prenda,cantidad)
        VALUES ({self.id_encargo},{self.id_prenda[0]},{1});'''
        make_query(conn,cursor,query) 

    def update_abono(self):
        conn, cursor = connectsql(host=self.ip)
        query = f'''UPDATE encargos SET abono = {self.abono},dias_entrega = {self.plazo} WHERE id = {self.id_encargo};'''
        make_query(conn,cursor,query)

    def openCamiseta(self):
        self.id_prenda = get_id_prenda(self.talla,'camisetas',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()

    def openZapatoBlanco(self):
        self.id_prenda = get_id_prenda(self.talla,'zapatoblanco',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()

    def openZapatoNegro(self):
        self.id_prenda = get_id_prenda(self.talla,'zapatonegro',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
    
    def openZapatoGoma(self):
        self.id_prenda = get_id_prenda(self.talla,'zapatogoma',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
    
    def openChompaAzul(self):
        self.id_prenda = get_id_prenda(self.talla,'chazul',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
        
    def openChompaGris(self):
        self.id_prenda = get_id_prenda(self.talla,'chgris',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
        
    def openSudaderas(self):
        self.id_prenda = get_id_prenda(self.talla,'sudaderas',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
        
        
    def openJeans(self):
        self.id_prenda = get_id_prenda(self.talla,'jeans',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
    
    def openBlusas(self):
        self.id_prenda = get_id_prenda(self.talla,'blusas',self.ip) 
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()

    def openMedias(self):
        self.id_prenda = get_id_prenda(self.talla,'medias',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()

    def openOtros(self):
        self.id_prenda = get_id_prenda(self.talla,'otros',self.ip)
        self.make_detail_encargo()
        self.get_metodo_pago()
        self.update_abono()
        self.get_obs()
        self.informe_encargo()
    
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
        self.obs = QLineEdit()
        
        layout.addRow("Nombre de la Niña:", self.nombre_nina)
        layout.addRow("Delantero:", self.delantero)
        layout.addRow("Trasero:", self.trasero)
        layout.addRow("Espalda:", self.espalda)
        layout.addRow("Cintura:", self.cintura)
        layout.addRow("Largo:", self.largo)
        layout.addRow("Observaciones:", self.obs)
        self.update_obs()
        
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
        self.metodo_pago,ok=QInputDialog.getItem(self.yomber_window,'Método de Pago',
                                                'Selecciona el método de pago',
                                                ['Efectivo','Transferencia'])
        if self.metodo_pago and ok:
            self.update_metodo_pago()
            self.informe_encargo()
            self.yomber_window.close()
        else:
            QMessageBox.about(self.up,"Error", "Debes seleccionar un método de pago")

    
    def sizes(self):
        if self.prenda == 'Jeans':
            self.tallas = ['6','8','10','12','14','16','28','30','32','34']
        elif self.prenda == 'Camisetas':
            self.tallas = ['6','8','10','12','14','16','S','M','L','XL','XXL']
        elif self.prenda == 'Yomber' or self.prenda == 'Blusas':
            self.tallas = ['6','8','10','12','14','16','S','M','L','XL']
        elif self.prenda == 'Medias':
            self.tallas = ['6-8','8-10','9-11']
        elif self.prenda == 'Zapatos B':
            self.tallas = ['B26','B27','B28','B29','B30','B31','B32','B33','B34','B35',
                 'B36','B37','B38','B39','B40','B41','B42','B43','B44']
        elif self.prenda == 'Zapatos N':
            self.tallas = ['N26','N27','N28','N29','N30','N31','N32','N33','N34','N35',
                 'N36','N37','N38','N39','N40','N41','N42','N43','N44']
        elif self.prenda == 'Zapatos G':
            self.tallas = ['G26','G27','G28','G29','G30','G31','G32','G33','G34','G35',
                 'G36','G37','G38','G39','G40','G41','G42','G43','G44']
        elif self.prenda == 'Otros':
            self.tallas = ['TOP','MEDIAS']
        elif self.prenda == 'Sudaderas' or self.prenda == 'Chompa Azul' or self.prenda == 'Chompa Gris':
            self.tallas = ['4', '6', '8', '10', '12', '14', '16', 'S', 'M', 'L', 'XL']
        else:
            self.tallas = ''
        return self.tallas

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()
      
    def get_size_and_abono(self,metodo):
        self.talla, ok = QInputDialog.getItem(self,'¿Qué talla se Necesita?','Ingrese la talla',self.sizes())

        if ok:
            if self.talla.upper() in self.sizes():
                    self.abono,ok1=QInputDialog.getText(self.up,'Abono',
                                                    '¿Cuánto va a abonar?')
                    if self.abono and ok1:
                        metodo()
            else:
                QMessageBox.about(self.up, "Error", "La talla que has seleccionado no existe")
                self.abono = None
            return self.talla, self.abono
        
    def get_metodo_pago(self):
        self.metodo_pago,ok=QInputDialog.getItem(self,'Método de Pago',
                                                'Selecciona el método de pago',
                                                ['Efectivo','Transferencia'])
        if self.metodo_pago and ok:
            self.update_metodo_pago()
        else:
            QMessageBox.about(self.up,"Error", "Debes seleccionar un método de pago")

    def update_metodo_pago(self):
        conn, cursor = connectsql(host=self.ip)
        query = f'''UPDATE encargos SET metodo_pago = '{self.metodo_pago}' WHERE id = {self.id_encargo};'''
        make_query(conn,cursor,query) 

    def get_obs(self):
        self.obs,ok=QInputDialog.getText(self,'Observaciones',
                                                '¿Deseas agregar observaciones?')
        if self.obs and ok:
            self.update_obs()

    def update_obs(self):
        conn, cursor = connectsql(host=self.ip)
        query = f'''UPDATE encargos SET observaciones = '{self.obs}' WHERE id = {self.id_encargo};'''
        make_query(conn,cursor,query)

    def query_encargo_detalle(self):  
        conn, cursor = connectsql(host=self.ip)
        query = f''' SELECT clientes.nombre AS "Nombre del cliente",
                        encargos.id AS "ID",
                        encargos.fecha_encargo AS "Encargado el:",
                        encargos.fecha_entrega AS "Para Entregar el:",
                        encargos.entregado,
                        tipo_prendas.name AS "Nombre de la prenda",
                        prendas.talla AS "Talla",
                        prendas.precio AS "Precio",
                        detalle_encargo.cantidad AS "Cantidad",
                        (prendas.precio * detalle_encargo.cantidad) AS "Total Parcial",
                        encargos.total AS "Total del Encargo",
                        detalle_encargo.id AS "ID_ENCARGO",
                        encargos.abono,
                        encargos.saldo,
                        encargos.observaciones
                        FROM clientes
                        JOIN encargos ON clientes.id = encargos.id_cliente
                        JOIN detalle_encargo ON encargos.id = detalle_encargo.id_encargo
                        JOIN prendas ON detalle_encargo.id_prenda = prendas.id
                        JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
                        WHERE encargos.id = {self.id_encargo}
                        ORDER BY detalle_encargo.id'''
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close() 
        return result   

    def informe_encargo(self,mode='normal'):
        try:
            result = self.query_encargo_detalle()
            print(result)
            print(len(result))
            self.result = result
            self.informe = QDialog()
            self.informe.setWindowTitle(f'Informe de Encargo {self.id_encargo} I.E CARACAS')
            self.informe.setGeometry(0,0,550,400)
            # Crear los labels para mostrar los datos
            self.names = [row[5] for row in result]
            self.tallas = [row[6] for row in result]
            self.prices = [row[7] for row in result]
            self.quant = [row[8] for row in result]
            self.parcial = [row[9] for row in result]
            self.id_det = [row[11] for row in result]
            label_title = QLabel(f'Uniformes Consuelo Rios')
            label_cliente = QLabel(f'Nombre del cliente: {result[0][0]} | ID_ENCARGO: ({result[0][1]})')
            label_fecha_enc = QLabel(f'Fecha Encargo: {result[0][2]}')
            label_fecha_ent = QLabel(f'Fecha Encargo: {result[0][3]}')
            label_entregado = QLabel(f'Entregado: {result[0][4]}')
            grid = QGridLayout()
            ti_name = QLabel("Prenda") 
            ti_size = QLabel("Talla")
            ti_price = QLabel("Precio")
            ti_quant = QLabel("Cantidad")
            ti_total = QLabel("Subtotal")
            ti_spa = [QLabel("|") for i in range(5)]
            grid.addWidget(ti_name,0,0,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[0],0,1,alignment=Qt.AlignCenter)
            grid.addWidget(ti_size,0,2,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[1],0,3,alignment=Qt.AlignCenter)
            grid.addWidget(ti_price,0,4,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[2],0,5,alignment=Qt.AlignCenter)
            grid.addWidget(ti_quant,0,6,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[3],0,7,alignment=Qt.AlignCenter)
            grid.addWidget(ti_total,0,8,alignment=Qt.AlignCenter)
            for i in range(len(self.names)):
                label_name= QLabel(f'{self.names[i]}')
                label_size= QLabel(f'{self.tallas[i]}')
                label_prices= QLabel(f'{self.prices[i]}')
                label_quant= QSpinBox()
                label_quant.setMinimum(0)
                label_quant.setValue(self.quant[i])
                self.id_detalle = self.id_det[i]
                label_parcial= QLabel(f'{self.parcial[i]}')
                grid.addWidget(label_name,i+1,0,alignment=Qt.AlignCenter)
                grid.addWidget(label_size,i+1,2,alignment=Qt.AlignCenter)
                grid.addWidget(label_prices,i+1,4,alignment=Qt.AlignCenter)
                grid.addWidget(label_quant,i+1,6,alignment=Qt.AlignCenter)
                grid.addWidget(label_parcial,i+1,8,alignment=Qt.AlignCenter)
            grid2 = QGridLayout()
            label_total_encargo = QLabel(f'Total del Encargo: {result[0][10]}')
            label_abono_encargo = QLabel(f'Abono: {result[0][12]}')
            label_saldo_encargo = QLabel(f'Saldo: {result[0][13]}')
            label_obs = QLabel(f'Observaciones: {result[0][14]}')
            grid2.addWidget(label_total_encargo,0,0,alignment=Qt.AlignCenter)
            grid2.addWidget(label_abono_encargo,1,0,alignment=Qt.AlignCenter)
            grid2.addWidget(label_saldo_encargo,1,1,alignment=Qt.AlignCenter)
            grid2.addWidget(label_total_encargo,2,0,alignment=Qt.AlignCenter)

            # Define el ancho de las columnas
            grid.setColumnStretch(0, 2)
            grid.setColumnStretch(1, 0.2)
            grid.setColumnStretch(2, 1)
            grid.setColumnStretch(3, 0.2)
            grid.setColumnStretch(4, 2)
            grid.setColumnStretch(5, 0.2)
            grid.setColumnStretch(6, 1)
            grid.setColumnStretch(7, 0.2)
            grid.setColumnStretch(8, 2)
            

            #si el modo del informe son observaciones
            if mode == 'normal':
                hbox = QHBoxLayout()
                save = PushButton("GUARDAR ENCARGO")
                save.clicked.connect(self.save_encargo)
                edit = PushButton("AGREGAR PRODUCTOS")
                edit.clicked.connect(self.agregar_productos)
                hbox.addWidget(save)
                hbox.addWidget(edit)

            # Crear un layout para organizar los labels
            layout = QVBoxLayout()
            layout.addWidget(label_title,alignment=Qt.AlignCenter)
            layout.addWidget(label_cliente)
            layout.addWidget(label_fecha_enc)
            layout.addWidget(label_fecha_ent)
            layout.addWidget(label_entregado)
            layout.addLayout(grid)
            layout.addLayout(grid2)
            layout.addWidget(label_obs)
            #si el modo del informe son observaciones
            if mode == 'normal':
                layout.addLayout(hbox)

            #Agregar el widget al layout principal de la ventana
            self.informe.setLayout(layout)
            adj_sup_center(self.informe)
            self.informe.exec_()

        except IndexError:
            QMessageBox.about(self.up,"Error", "No hay información para ver")

    def agregar_productos(self):
        pass
    def save_encargo(self):
        self.informe.accept()

class DetallesCambio(QMainWindow):
    def __init__(self, main_window, id_cambio,info=False) -> None:
        super().__init__() 
        self.up = main_window
        self.id_cambio = id_cambio
        self.ip = self.up.ip
        self.prendas = ['Zapatos B','Zapatos N','Zapatos G','Chompa Azul','Chompa Gris','Sudaderas',
        'Camisetas','Blusas','Jeans','Medias','Otros']
        self.title = f'Cambio #{self.id_cambio}'
        if info:
            pass
        else:
            self.initUI()
            self.show()
        

    def initUI(self):
        print('1')
        self.setWindowTitle(self.title)
        # Crear el layout principal
        vbox = QVBoxLayout()  
        layout = QHBoxLayout()
        principal_label = QLabel('Cambio')
        # Crear el layout para las prendas entrantes
        entrante_layout = QFormLayout()
        
        # Crear los widgets para seleccionar el tipo y la talla de la prenda entrante
        self.prenda_entrante_label = QLabel("Prenda entrante:")
        self.prenda_entrante_combo = QComboBox()
        self.prenda_entrante_combo.addItems(self.prendas)
        self.prenda_entrante_combo.activated.connect(lambda: self.talla_entrante_combo.clear() or 
                                                    self.talla_entrante_combo.addItems(
                                                    self.sizes(
                                                    self.prenda_entrante_combo.currentText())))
        self.talla_entrante_label = QLabel("Talla entrante:")
        self.talla_entrante_combo = QComboBox()
        #Crear los widgets para seleccionar la cantidad de prendas entrantes y salientes
        self.cantidad_entrante_label = QLabel("Cantidad entrante:", self)
        self.cantidad_entrante_spinbox = QSpinBox(self)
        self.cantidad_entrante_spinbox.setMinimum(0)
        entrante_layout.addRow(self.prenda_entrante_label,self.prenda_entrante_combo)
        entrante_layout.addRow(self.talla_entrante_label,self.talla_entrante_combo)
        entrante_layout.addRow(self.cantidad_entrante_label,self.cantidad_entrante_spinbox)

        saliente_layout = QFormLayout()
         # Crear los widgets para seleccionar el tipo y la talla de la prenda entrante
        self.prenda_saliente_label = QLabel("Prenda saliente:")
        self.prenda_saliente_combo = QComboBox()
        self.prenda_saliente_combo.addItems(self.prendas)
        self.prenda_saliente_combo.activated.connect(lambda: self.talla_saliente_combo.clear() or
                                                    self.talla_saliente_combo.addItems(
                                                    self.sizes(
                                                    self.prenda_saliente_combo.currentText())))
        self.talla_saliente_label = QLabel("Talla saliente:")
        self.talla_saliente_combo = QComboBox()
        # Crear los widgets para seleccionar la cantidad de prendas salientes y salientes
        self.cantidad_saliente_label = QLabel("Cantidad saliente:", self)
        self.cantidad_saliente_spinbox = QSpinBox(self)
        self.cantidad_saliente_spinbox.setMinimum(0)
        saliente_layout.addRow(self.prenda_saliente_label,self.prenda_saliente_combo)
        saliente_layout.addRow(self.talla_saliente_label,self.talla_saliente_combo)
        saliente_layout.addRow(self.cantidad_saliente_label,self.cantidad_saliente_spinbox)
        layout.addLayout(entrante_layout)
        layout.addLayout(saliente_layout)
        print('2')
   
        insert_button = QPushButton("Realizar Cambio")
        insert_button.clicked.connect(self.openLogic)
        vbox.addLayout(layout)
        vbox.addWidget(insert_button)

        widget = QWidget(self)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
    

    def def_tabl(self,prenda):
        if prenda == 'Jeans':
            X = 'jeans'
        elif prenda == 'Camisetas':
            X = 'camisetas'
        elif prenda == 'Blusas':
            X = 'blusas'
        elif prenda == 'Medias':
            X = 'medias'
        elif prenda == 'Zapatos B':
            X = 'zapatoblanco'
        elif prenda == 'Zapatos N':
            X = 'zapatonegro'
        elif prenda == 'Zapatos G':
            X = 'zapatogoma'
        elif prenda == 'Otros':
            X = 'otros'
        elif prenda == 'Sudaderas':
            X = 'sudaderas'
        elif prenda == 'Chompa Azul':
            X = 'chazul'
        elif prenda == 'Chompa Gris':
            X = 'chgris'
        else:
            X = ''
        return X
    def openLogic(self):
        table_entrante = self.def_tabl(self.prenda_entrante_combo.currentText())
        self.id_prenda_entrante = get_id_prenda(self.talla_entrante_combo.currentText(),
                                                table_entrante,
                                                self.ip)
    
        table_saliente = self.def_tabl(self.prenda_saliente_combo.currentText())
        self.id_prenda_saliente = get_id_prenda(self.talla_saliente_combo.currentText(),
                                            table_saliente,
                                            self.ip) 

        self.make_cambio()
        self.get_obs()
        self.close()

    def make_cambio(self):
        conn, cursor = connectsql(host=self.ip)
        try:
            query = f'''INSERT INTO public.detalle_cambio(
            id_cambio, id_prenda_entrante, id_prenda_saliente, cantidad_entrante, cantidad_saliente)
            VALUES ({self.id_cambio}, {self.id_prenda_entrante[0]}, {self.id_prenda_saliente[0]},
            {self.cantidad_entrante_spinbox.value()}, {self.cantidad_saliente_spinbox.value()});'''

            make_query(conn,cursor,query)

        except TypeError:
            QMessageBox.about(self.up, "Error", "Debes ingresar los datos para poder realizar el cambio")
            self.initUI

    def update_obs(self,obs):
        conn, cursor = connectsql(host=self.ip)
        query = f'''UPDATE cambios SET observaciones = '{obs}' WHERE id = {self.id_encargo};'''
        make_query(conn,cursor,query)  

    def get_obs(self):
        self.obs,ok=QInputDialog.getText(self,'Observaciones',
                                                '¿Deseas agregar observaciones?')
        if self.obs and ok:
            self.update_obs() 

    def update_obs(self):
        conn, cursor = connectsql(host=self.ip)
        query = f'''UPDATE cambios SET observaciones = '{self.obs}', finalizado = True WHERE id = {self.id_cambio};'''
        make_query(conn,cursor,query)       

    def sizes(self,prenda):
        if prenda == 'Jeans':
            X = ['6','8','10','12','14','16','28','30','32','34']
        elif prenda == 'Camisetas':
            X = ['6','8','10','12','14','16','S','M','L','XL','XXL']
        elif prenda == 'Blusas':
            X = ['6','8','10','12','14','16','S','M','L','XL']
        elif prenda == 'Medias':
            X = ['6-8','8-10','9-11']
        elif prenda == 'Zapatos B':
            X = ['B26','B27','B28','B29','B30','B31','B32','B33','B34','B35',
                 'B36','B37','B38','B39','B40','B41','B42','B43','B44']
        elif prenda == 'Zapatos N':
            X = ['N26','N27','N28','N29','N30','N31','N32','N33','N34','N35',
                 'N36','N37','N38','N39','N40','N41','N42','N43','N44']
        elif prenda == 'Zapatos G':
            X = ['G26','G27','G28','G29','G30','G31','G32','G33','G34','G35',
                 'G36','G37','G38','G39','G40','G41','G42','G43','G44']
        elif prenda == 'Otros':
            X = ['TOP','MEDIAS']
        elif prenda == 'Sudaderas' or prenda == 'Chompa Azul' or prenda == 'Chompa Gris':
            X = ['4', '6', '8', '10', '12', '14', '16', 'S', 'M', 'L', 'XL']
        else:
            X = ''
        return X

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()

    def query_cambio_detalle(self):  
        conn, cursor = connectsql(host=self.ip)
        query = f''' SELECT clientes.nombre AS "Nombre del cliente",
                        cambios.id AS "ID",
                        cambios.fecha,
                        tp_entrante.name AS "Prenda Entrante",
                        tp_saliente.name AS "Prenda Saliente",
                        prendas_entrantes.talla AS "Talla Entrante",
                        prendas_salientes.talla AS "Talla Saliente",
                        prendas_entrantes.precio AS "Precio Entrante",
                        prendas_salientes.precio AS "Precio Saliente",
                        detalle_cambio.cantidad_entrante,
                        detalle_cambio.cantidad_saliente,
                        cambios.total_entrada AS "Total Entrante",
                        cambios.total_salida AS "Total Saliente",
                        (cambios.total_entrada-cambios.total_salida) AS "Total",
                        detalle_cambio.id AS "ID_cambio",
                        cambios.observaciones
                        FROM clientes
                        JOIN cambios ON clientes.id = cambios.id_cliente
                        JOIN detalle_cambio ON cambios.id = detalle_cambio.id_cambio
                        JOIN prendas AS prendas_entrantes ON detalle_cambio.id_prenda_entrante = prendas_entrantes.id
                        JOIN prendas AS prendas_salientes ON detalle_cambio.id_prenda_saliente = prendas_salientes.id
                        JOIN tipo_prendas AS tp_entrante ON prendas_entrantes.id_tipo_prenda = tp_entrante.id
                        JOIN tipo_prendas AS tp_saliente ON prendas_salientes.id_tipo_prenda = tp_saliente.id
                        WHERE cambios.id = 3
                        ORDER BY detalle_cambio.id'''
        
        
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close() 
        return result   

    def informe_cambio(self,mode='normal'):
        try:
            result = self.query_cambio_detalle()
            print(result)
            print(len(result))
            self.result = result
            self.informe = QDialog()
            self.informe.setWindowTitle(f'Informe de cambio {self.id_cambio} I.E CARACAS')
            self.informe.setGeometry(0,0,550,400)
            # Crear los labels para mostrar los datos
            self.names_entrante = [row[3] for row in result]
            self.names_saliente = [row[4] for row in result]
            self.tallas_entrante = [row[5] for row in result]
            self.tallas_saliente = [row[6] for row in result]
            self.prices_entrante = [row[7] for row in result]
            self.prices_saliente = [row[8] for row in result]
            self.quant_entrante = [row[9] for row in result]
            self.quant_saliente = [row[10] for row in result]
            self.total_entrante = [row[11] for row in result]
            self.total_saliente = [row[12] for row in result]
            self.id_det = [row[14] for row in result]
            label_title = QLabel(f'Uniformes Consuelo Rios')
            label_cliente = QLabel(f'Nombre del cliente: {result[0][0]} | ID_CAMBIO: ({result[0][1]})')
            label_fecha = QLabel(f'Fecha Cambio: {result[0][2]}')
            grid = QGridLayout()
            ti_name = QLabel("Prenda E") 
            ti_size = QLabel("Talla E")
            ti_price = QLabel("Precio E")
            ti_quant = QLabel("Cantidad E")
            ti_total = QLabel("Total E")
            ti_name_sal = QLabel("Prenda S") 
            ti_size_sal = QLabel("Talla S")
            ti_price_sal = QLabel("Precio S")
            ti_quant_sal = QLabel("Cantidad S")
            ti_total_sal = QLabel("Total S")
            ti_spa = [QLabel("|") for i in range(8)]
            grid.addWidget(ti_name,0,0,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[0],0,1,alignment=Qt.AlignCenter)
            grid.addWidget(ti_size,0,2,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[1],0,3,alignment=Qt.AlignCenter)
            grid.addWidget(ti_price,0,4,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[2],0,5,alignment=Qt.AlignCenter)
            grid.addWidget(ti_quant,0,6,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[3],0,7,alignment=Qt.AlignCenter)
            grid.addWidget(ti_total,0,8,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[3],0,9,alignment=Qt.AlignCenter)
            grid.addWidget(ti_name_sal,0,10,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[0],0,11,alignment=Qt.AlignCenter)
            grid.addWidget(ti_size_sal,0,12,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[2],0,13,alignment=Qt.AlignCenter)
            grid.addWidget(ti_price_sal,0,14,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[2],0,15,alignment=Qt.AlignCenter)
            grid.addWidget(ti_quant_sal,0,16,alignment=Qt.AlignCenter)
            grid.addWidget(ti_spa[3],0,17,alignment=Qt.AlignCenter)
            grid.addWidget(ti_total_sal,0,18,alignment=Qt.AlignCenter)

            for i in range(len(self.names_entrante)):
                label_name_ent= QLabel(f'{self.names_entrante[i]}')
                label_size_ent= QLabel(f'{self.tallas_entrante[i]}')
                label_prices_ent= QLabel(f'{self.prices_entrante[i]}')
                label_quant_ent= QSpinBox()
                label_quant_ent.setMinimum(0)
                label_quant_ent.setValue(self.quant_entrante[i])
                label_parcial_ent= QLabel(f'{self.total_entrante[i]}')
                grid.addWidget(label_name_ent,i+1,0,alignment=Qt.AlignCenter)
                grid.addWidget(label_size_ent,i+1,2,alignment=Qt.AlignCenter)
                grid.addWidget(label_prices_ent,i+1,4,alignment=Qt.AlignCenter)
                grid.addWidget(label_quant_ent,i+1,6,alignment=Qt.AlignCenter)
                grid.addWidget(label_parcial_ent,i+1,8,alignment=Qt.AlignCenter)
                label_name_sal= QLabel(f'{self.names_saliente[i]}')
                label_size_sal= QLabel(f'{self.tallas_saliente[i]}')
                label_prices_sal= QLabel(f'{self.prices_saliente[i]}')
                label_quant_sal= QSpinBox()
                label_quant_sal.setMinimum(0)
                label_quant_sal.setValue(self.quant_saliente[i])
                label_parcial_sal= QLabel(f'{self.total_saliente[i]}')
                grid.addWidget(label_name_sal,i+1,10,alignment=Qt.AlignCenter)
                grid.addWidget(label_size_sal,i+1,12,alignment=Qt.AlignCenter)
                grid.addWidget(label_prices_sal,i+1,14,alignment=Qt.AlignCenter)
                grid.addWidget(label_quant_sal,i+1,16,alignment=Qt.AlignCenter)
                grid.addWidget(label_parcial_sal,i+1,18,alignment=Qt.AlignCenter)
            grid2 = QGridLayout()
            label_total_cambio = QLabel(f'Total del cambio: {result[0][13]}')
            label_obs = QLabel(f'Observaciones: {result[0][15]}')
            grid2.addWidget(label_total_cambio,0,0,alignment=Qt.AlignCenter)
            grid2.addWidget(label_total_cambio,2,0,alignment=Qt.AlignCenter)

            # Define el ancho de las columnas
            grid.setColumnStretch(0, 2)
            grid.setColumnStretch(1, 0.2)
            grid.setColumnStretch(2, 1)
            grid.setColumnStretch(3, 0.2)
            grid.setColumnStretch(4, 2)
            grid.setColumnStretch(5, 0.2)
            grid.setColumnStretch(6, 1)
            grid.setColumnStretch(7, 0.2)
            grid.setColumnStretch(8, 2)
            

            #si el modo del informe son observaciones
            if mode == 'normal':
                hbox = QHBoxLayout()
                save = PushButton("GUARDAR cambio")
                save.clicked.connect(self.save_cambio)
                edit = PushButton("AGREGAR PRODUCTOS")
                edit.clicked.connect(self.agregar_productos)
                hbox.addWidget(save)
                hbox.addWidget(edit)

            # Crear un layout para organizar los labels
            layout = QVBoxLayout()
            layout.addWidget(label_title,alignment=Qt.AlignCenter)
            layout.addWidget(label_cliente)
            layout.addWidget(label_fecha)
            layout.addLayout(grid)
            layout.addLayout(grid2)
            layout.addWidget(label_obs)
            #si el modo del informe son observaciones
            if mode == 'normal':
                layout.addLayout(hbox)

            #Agregar el widget al layout principal de la ventana
            self.informe.setLayout(layout)
            self.informe.exec_()

        except IndexError:
            QMessageBox.about(self.up,"Error", "No hay información para ver")

    def agregar_productos(self):
        pass
    def save_cambio(self):
        self.informe.accept()

