#Modulos de Terceros
from PyQt5.QtWidgets import (QMainWindow,QWidget,QLineEdit,QInputDialog,
                             QGridLayout,QHBoxLayout,QVBoxLayout,QSpinBox,
                             QFormLayout,QMessageBox,QLabel,QComboBox,
                             QPushButton)
from PyQt5.QtCore import Qt
#Modulos Internos
from Utils.style import PushButton
from Utils.QtUtils import INFO
from Utils.util_sql import delete_date,connectsql,make_query,get_id_prenda


def update_metodo_pago(metodo,id_encargo,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''UPDATE encargos SET metodo_pago = '{metodo}' WHERE id = {id_encargo};'''
    make_query(conn,cursor,query) 

def update_obs(obs,id_encargo,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''UPDATE encargos SET observaciones = '{obs}' WHERE id = {id_encargo};'''
    make_query(conn,cursor,query)

def make_detail_encargo(cantidad,id_encargo,id_prenda,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''INSERT INTO detalle_encargo (id_encargo,id_prenda,cantidad)
    VALUES ({id_encargo},{id_prenda},{cantidad});'''
    make_query(conn,cursor,query) 

def update_abono(abono,id_encargo,ip):
    conn, cursor = connectsql(host=ip)
    query = f'''UPDATE encargos SET abono = {abono} WHERE id = {id_encargo};'''
    make_query(conn,cursor,query)




class DetallesVenta(QMainWindow):
    def __init__(self,main_window,id_venta,title,ip) -> None:
        super().__init__() 
        self.main_window = main_window
        self.id_venta = id_venta
        self.ti = title
        self.table_name= self.ti.split()[0].lower() + 's'
        self.initUI()
        self.ip = ip
        
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
    
    
class DetallesEncargo(QMainWindow):
    def __init__(self, main_window, id_encargo) -> None:
        super().__init__() 
        self.up = main_window
        self.id_encargo = id_encargo
        self.ip = self.up.ip
        self.prendas = ['Yomber','Zapatos B','Zapatos N','Zapatos G','Chompa Azul','Chompa Gris','Sudaderas',
        'Camisetas','Blusas','Jeans','Medias','Otros']
        self.initUI()
        

    def initUI(self):
        self.prenda, ok = QInputDialog.getItem(self.up,'Title',
        'Selecciona el tipo de prenda',self.prendas)

        if self.prenda and ok:
            self.logic()
        else:
            self.cancelar
        
    def logic(self):
        ##YOMBER
        if self.prenda == 'Yomber':
            self.talla, ok = QInputDialog.getText(self.up,'¿Qué talla se Necesita?',
                                             'Ingrese la talla')
            if ok:
                if self.talla.upper() in self.sizes():
                    id_prenda = get_id_prenda(self.talla,'yomber',self.ip)
                    make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
                    abono,ok1=QInputDialog.getText(self.up,'Abono','¿Cuánto va a abonar?')
                    if abono and ok1:
                        update_abono(abono,self.id_encargo,self.ip)
                        self.openYomber()
                else:
                    QMessageBox.about(self.up, "Error", "La talla que has seleccionado no existe")
        
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
            self.talla,self.abono=self.get_size_and_abono(self.openCamisetas)
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


    

    def openZapatoBlanco(self):
        id_prenda = get_id_prenda(self.talla,'zapatoblanco',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()

    def openZapatoNegro(self):
        id_prenda = get_id_prenda(self.talla,'zapatonegro',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()
    
    def openZapatoGoma(self):
        id_prenda = get_id_prenda(self.talla,'zapatogoma',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()
    
    def openChompaAzul(self):
        id_prenda = get_id_prenda(self.talla,'chazul',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()
        
    def openChompaGris(self):
        id_prenda = get_id_prenda(self.talla,'chgris',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()
        
    def openSudaderas(self):
        id_prenda = get_id_prenda(self.talla,'sudaderas',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()
        
        
    def openJeans(self):
        id_prenda = get_id_prenda(self.talla,'jeans',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()
    
    def openBlusas(self):
        id_prenda = get_id_prenda(self.talla,'blusas',self.ip) 
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()

    def openMedias(self):
        id_prenda = get_id_prenda(self.talla,'medias',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()

    def openOtros(self):
        id_prenda = get_id_prenda(self.talla,'otros',self.ip)
        make_detail_encargo(1,self.id_encargo,id_prenda[0],self.ip)
        self.get_metodo_pago()
        update_abono(self.abono,self.id_encargo,self.ip)
        self.get_obs()

    def update_obs(self,obs):
        conn, cursor = connectsql(host=self.ip)
        query = f'''UPDATE encargos SET observaciones = '{obs}' WHERE id = {self.id_encargo};'''
        make_query(conn,cursor,query)
    
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
        update_obs(self.obs,self.id_encargo,self.ip)
        
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
            update_metodo_pago(self.metodo_pago,self.id_encargo,self.ip)
            self.yomber_window.close()
        else:
            QMessageBox.about(self.up,"Error", "Debes seleccionar un método de pago")

    
    def sizes(self):
        if self.prenda == 'Jeans':
            X = ['6','8','10','12','14','16','28','30','32','34']
        elif self.prenda == 'Camisetas':
            X = ['6','8','10','12','14','16','S','M','L','XL','XXL']
        elif self.prenda == 'Yomber' or self.prenda == 'Blusas':
            X = ['6','8','10','12','14','16','S','M','L','XL']
        elif self.prenda == 'Medias':
            X = ['6-8','8-10','9-11']
        elif self.prenda == 'Zapatos B':
            X = ['B26','B27','B28','B29','B30','B31','B32','B33','B34','B35',
                 'B36','B37','B38','B39','B40','B41','B42','B43','B44']
        elif self.prenda == 'Zapatos N':
            X = ['N26','N27','N28','N29','N30','N31','N32','N33','N34','N35',
                 'N36','N37','N38','N39','N40','N41','N42','N43','N44']
        elif self.prenda == 'Zapatos G':
            X = ['G26','G27','G28','G29','G30','G31','G32','G33','G34','G35',
                 'G36','G37','G38','G39','G40','G41','G42','G43','G44']
        elif self.prenda == 'Otros':
            X = ['TOP','MEDIAS']
        elif self.prenda == 'Sudaderas' or self.prenda == 'Chompa Azul' or self.prenda == 'Chompa Gris':
            X = ['4', '6', '8', '10', '12', '14', '16', 'S', 'M', 'L', 'XL']
        else:
            X = ''
        return X
    
    def openFinalizar(self):
        INFO(self).informe_venta()

    def cancelar(self):
        delete_date(self,ok=True,id=self.id_venta,ip=self.ip)
        self.close()
      
    def get_size_and_abono(self,metodo):
        print(self.prenda)
        self.talla, ok = QInputDialog.getText(self.up,'¿Qué talla se Necesita?',
                                                'Ingrese la talla')
        print(self.talla)
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
            update_metodo_pago(self.metodo_pago,self.id_encargo,self.ip)
        else:
            QMessageBox.about(self.up,"Error", "Debes seleccionar un método de pago")

    def get_obs(self):
        self.obs,ok=QInputDialog.getText(self,'Observaciones',
                                                '¿Deseas agregar observaciones?')
        if self.metodo_pago and ok:
            self.update_obs(self.obs)
            
class DetallesCambio(QMainWindow):
    def __init__(self, main_window, id_cambio) -> None:
        super().__init__() 
        self.up = main_window
        self.id_cambio = id_cambio
        self.ip = self.up.ip
        self.prendas = ['Zapatos B','Zapatos N','Zapatos G','Chompa Azul','Chompa Gris','Sudaderas',
        'Camisetas','Blusas','Jeans','Medias','Otros']
        self.title = f'Cambio #{self.id_cambio}'
        self.initUI()
        

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
        query = f'''INSERT INTO public.detalle_cambio(
	    id_cambio, id_prenda_entrante, id_prenda_saliente, cantidad_entrante, cantidad_saliente)
	    VALUES ({self.id_cambio}, {self.id_prenda_entrante[0]}, {self.id_prenda_saliente[0]},
        {self.cantidad_entrante_spinbox.value()}, {self.cantidad_saliente_spinbox.value()});'''
        try:
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
            update_obs(self.obs)        
           

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

