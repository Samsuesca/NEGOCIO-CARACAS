from Utils.util_sql import connect, execute_query
from Utils.style import PushButton, adj_left, adj_right,adj_sup_center,adj_middle
from datetime import datetime
from PyQt5.QtWidgets import QDialog,QSplashScreen,QTableWidget,QTableWidgetItem,QGridLayout, QMainWindow, QMessageBox, QHeaderView,QLabel, QVBoxLayout, QWidget, QInputDialog,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QImage 
import time
import io
import os
import json
from PIL import Image



def show_beg(app,welcome_window):
        # Abre la imagen con "pillow"
    pil_image = Image.open("icon.png").convert("RGB")

    # Convierte la imagen a formato JPEG y a una cadena de bytes
    bytes_io = io.BytesIO()
    pil_image.save(bytes_io, "JPEG")
    bytes_io.seek(0)
    img_data = bytes_io.read()


    # Convierte la imagen a formato Qt
    qt_image = QImage.fromData(img_data)
    # Crea un pixmap a partir de la imagen
    splash_pix = QPixmap.fromImage(qt_image)
    # splash_pix = QPixmap(str(path))
    splash = QSplashScreen(
        splash_pix,
        Qt.WindowStaysOnTopHint
    )
    splash.setEnabled(False)
    splash.show()
    splash.setGeometry(100,100,500,500)
    adj_middle(splash)
 
    # Esto es un simple contador/temporizador para mostrar en pantalla
    # el splash screen. En el futuro haremos que esto sea más útil.
    for i in range(0, 3): 
        msg = ( 
            '<h1><font color="black">' 
             f'Iniciando en {3-i}s' 
             '</font></h1>' 
        ) 
        splash.showMessage( 
            msg, 
            int(Qt.AlignBottom) | int(Qt.AlignHCenter),  
            Qt.black  
        ) 
        time.sleep(1) 
        app.processEvents() 

    splash.finish(welcome_window)


class ShowData(QMainWindow):

    def __init__(self,main_window, table_name) -> None:
        super().__init__()
        self.table_name = table_name
        self.main_window = main_window
        self.initUI()
        self.setWindowTitle(f"Visualización de {self.table_name.title()}")
        self.setMinimumSize(400, 250)

    def initUI(self):
        try:    
            # Obtener los datos de la tabla "telas"
            results, column_names = self.get_table_data(self.table_name)
            # Crear la tabla y establecer los encabezados de las columnas
            table = QTableWidget()
            table.setRowCount(len(results))
            table.setColumnCount(len(results[0]))
            table.setHorizontalHeaderLabels(column_names)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


            # Agregar los datos a la tabla
            for i, row in enumerate(results):
                table.setRowCount(i+1)
                for j, col in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(col)))
            
           
            # Ajustar el tamaño de la ventana al tamaño mínimo necesario para mostrar todos sus widgets
            table_width = table.sizeHint().width()
            table_height = table.sizeHint().height()
            
            # Mostrar la tabla en la ventana
            self.setCentralWidget(table)
            self.setGeometry(0,0,table_width, table_height)

            
        except IndexError:
            QMessageBox.warning(self.main_window, 'Error', 'Parece que la tabla que tratas de ver esta vacia')


    def get_table_data(self,table_name):
        conn, cursor = connect()
        results = execute_query(conn,cursor, f'SELECT * FROM {table_name}')
        column_names = [column[0] for column in cursor.description]
        return results, column_names

class Pestana(QMainWindow):
    def __init__(self, main_window, table_name):
        self.main_window = main_window
        self.table_name = table_name
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel(f"Este es el Inventario de {self.table_name.title()}", self)
        label.setAlignment(Qt.AlignCenter)

        # Agregar un botón para mostrar datos
        show = PushButton("Mostrar Datos", self)
        show.clicked.connect(self.openData)

        # # Agregar un botón para editar datos
        edit = PushButton("Editar Datos", self)
        edit.clicked.connect(self.editData)

        # Agregar un botón para insertar datos
        insert = PushButton("Insertar Datos", self)
        insert.clicked.connect(self.insertData)

        # # Agregar un botón para eliminar datos
        delete = PushButton("Eliminar Datos", self)
        delete.clicked.connect(self.deleteData)

        # Agregar los botones al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        layout.addWidget(insert, alignment=Qt.AlignCenter)
        layout.addWidget(delete, alignment=Qt.AlignCenter)
        layout.addWidget(edit, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def openData(self):
        self.show_data = ShowData(self.main_window,self.table_name)
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)


class Ventana(QMainWindow):
    def __init__(self, main_window, table_name):
        self.main_window = main_window
        self.table_name = table_name
        
        super().__init__()
        self.initUI()
        self.setWindowTitle(f'Estás en: {table_name.title()}')
    def initUI(self):
        # Agregar un mensaje de bienvenida 
        label = QLabel(f"Este es tu menú para {self.table_name.title()}", self)
        label.setAlignment(Qt.AlignCenter)

        # Agregar un botón para mostrar datos
        show = PushButton(f"Mostrar {self.table_name}", self)
        show.clicked.connect(self.openData)

        # # Agregar un botón para editar 
        edit = PushButton(f"Editar {self.table_name}", self)
        edit.clicked.connect(self.editData)

        # Agregar un botón para insertar 
        insert = PushButton(f"Realizar {self.table_name}", self)
        insert.clicked.connect(self.insertData)

        # # Agregar un botón para eliminar 
        delete = PushButton(f"Eliminar {self.table_name}", self)
        delete.clicked.connect(self.deleteData)

        # # Agregar un botón para volver
        volver = PushButton("Volver", self)
        volver.clicked.connect(self.returnback)

        # Agregar los botones al layout principal de la ventana
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(show, alignment=Qt.AlignCenter)
        layout.addWidget(insert, alignment=Qt.AlignCenter)
        layout.addWidget(delete, alignment=Qt.AlignCenter)
        layout.addWidget(edit, alignment=Qt.AlignCenter)
        layout.addWidget(volver, alignment=Qt.AlignCenter)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def openData(self):
        self.show_data = ShowData(self.main_window,self.table_name)
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)
    
    def returnback(self):
        # Mostrar la ventana del menú principal y cerrar la ventana actual
        self.main_window.show()
        self.close()



class INFO():
    def __init__(self,selfis) -> None:
        self.up = selfis

    def detalles_venta(self,table_name):
        talla, ok = QInputDialog.getText(self.up,'¿Qué talla se Necesita?','Ingrese la talla')
        if talla and ok:
            # Conectarse a la base de datos y obtener un cursor
            conn, cursor = connect()
            query = f"SELECT id FROM {table_name} WHERE talla = '{talla.upper()}'"
            cursor.execute(query)
            id_prenda = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            #Obtener la cantidad
            quantity, ok1 = QInputDialog.getInt(self.up,'¿Qué cantidad va a llevar?','Ingrese la cantidad')
            if quantity and ok1:
                #Obtener la cantidad del inventario
                conn, cursor = connect()
                query = f"SELECT cantidad FROM inventario WHERE id_prenda = {id_prenda[0]}"
                cursor.execute(query)
                cantidad_inventario = cursor.fetchone()
                conn.commit()
                cursor.close()
                conn.close()

                if cantidad_inventario[0] >= quantity:
                    conn, cursor = connect()
                    query = f'''INSERT INTO public.detalle_venta (id_venta,id_prenda,cantidad)
                    VALUES ({self.up.id_venta},{id_prenda[0]},{quantity});'''
                    cursor.execute(query)
                    conn.commit()
                    cursor.close()
                    conn.close()   
                    self.up.initUI()
                else:
                    QMessageBox.about(self.up, "Error", "No hay inventario")

    def informe_venta(self,id_venta):
        result = self.query_venta_detalle(id_venta)
        self.result = result
        self.informe = QDialog()
        self.informe.setWindowTitle(f'Informe de venta {id_venta}')
        self.informe.setGeometry(0,0,550,400)
        names = [row[3] for row in result]
        sizes = [row[4] for row in result]
        prices = [row[5] for row in result]
        quant = [row[6] for row in result]
        parcial = [row[7] for row in result]
        # Crear los labels para mostrar los datos
        try:
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
            for i in range(len(names)):
                label_name= QLabel(f'{names[i]}')
                label_size= QLabel(f'{sizes[i]}')
                label_prices= QLabel(f'{prices[i]}')
                label_quant= QLabel(f'{quant[i]}')
                label_parcial= QLabel(f'{parcial[i]}')
                grid.addWidget(label_name,i+1,0,alignment=Qt.AlignCenter)
                grid.addWidget(label_size,i+1,2,alignment=Qt.AlignCenter)
                grid.addWidget(label_prices,i+1,4,alignment=Qt.AlignCenter)
                grid.addWidget(label_quant,i+1,6,alignment=Qt.AlignCenter)
                grid.addWidget(label_parcial,i+1,8,alignment=Qt.AlignCenter)
            label_total_venta = QLabel(f'Total de la venta: {result[0][8]}')
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

            #botones
            hbox = QHBoxLayout()
            save = PushButton("Guardar Venta")
            save.clicked.connect(self.save_venta)
            edit = PushButton("Editar Venta")
            edit.clicked.connect(self.edit_venta)
            hbox.addWidget(save)
            hbox.addWidget(edit)

            # Crear un layout para organizar los labels
            layout = QVBoxLayout()
            layout.addWidget(label_cliente)
            layout.addWidget(label_fecha)
            layout.addLayout(grid)
            layout.addWidget(label_total_venta)
            layout.addLayout(hbox)

            #Agregar el widget al layout principal de la ventana
            self.informe.setLayout(layout)
            adj_sup_center(self.informe)
            self.informe.exec_()

        except IndexError:
            QMessageBox.about(self.up,"Error", "No se han añadido prendas a la venta")

    def save_venta(self):
        result=self.result
            # Obtiene la fecha actual en formato "YYYY-MM-DD"
        today = datetime.now().strftime("%Y-%m-%d")
        ventas = {'Ventas': []}
        # Crea el diccionario con los datos de la venta
        data = {'name':result[0][0],
                'id_cliente':result[0][1],
                'fecha':result[0][2].strftime("%Y-%m-%d %H:%M:%S"),
                'detalles':[{'prenda': result[i][3], 'talla': result[i][4],
                 'precio': str(result[i][5]), 'cantidad': result[i][6], 'subtotal': 
                 str(result[i][7])} for i in range(len(result))],
                'total':str(result[0][8])}
      #######
       
        if os.path.exists(f"registro_ventas/{today}.json"):
            # Escribe la lista de ventas con la venta actual en el archivo
            f = open(f"registro_ventas/{today}.json")
            read = json.load(f)
            with open(f"registro_ventas/{today}.json", "r+") as file:
                # Carga el contenido del archivo en formato JSON
                ventass = json.load(file)
                read['Ventas'].append(data)
                ventass.update(read)
                file.seek(0)
                json.dump(ventass, file, indent = 4)
        else:
            # Si no existe, abre el archivo en modo "w" (sobreescribir)
            with open(f"registro_ventas/{today}.json", "w") as f:
                # Escribe el diccionario en formato JSON en el archivo
                json.dump(ventas, f)
            # Escribe la lista de ventas con la venta actual en el archivo
            f = open(f"registro_ventas/{today}.json")
            read = json.load(f)
            with open(f"registro_ventas/{today}.json", "r+") as file:
                # Carga el contenido del archivo en formato JSON
                ventass = json.load(file)
                read['Ventas'].append(data)
                ventass.update(read)
                file.seek(0)
                json.dump(ventass, file, indent = 4)
        self.informe.close()
        self.up.close()       
    def edit_venta():
        pass   
    def query_venta_detalle(self,id_venta):  
        conn, cursor = connect()
        query = f''' SELECT clientes.nombre AS "Nombre del cliente",
                        ventas.id AS "ID",
                        ventas.fecha AS "Fecha",
                        tipo_prendas.name AS "Nombre de la prenda",
                        prendas.talla AS "Talla",
                        prendas.precio AS "Precio",
                        detalle_venta.cantidad AS "Cantidad",
                        (prendas.precio * detalle_venta.cantidad) AS "Total parcial por prenda",
                        ventas.total AS "Total de la Venta"
                        FROM clientes
                        JOIN ventas ON clientes.id = ventas.id_cliente
                        JOIN detalle_venta ON ventas.id = detalle_venta.id_venta
                        JOIN prendas ON detalle_venta.id_prenda = prendas.id
                        JOIN tipo_prendas ON prendas.id_tipo_prenda = tipo_prendas.id
                        WHERE ventas.id = {id_venta}'''
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close() 
        return result   

    



            
        