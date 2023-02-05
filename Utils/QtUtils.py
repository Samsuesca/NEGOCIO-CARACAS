#Modulos Internos
from Ventas.detalles import DetallesCambio,DetallesVenta,DetallesEncargo
from Utils.util_sql import execute_query
from Utils.style import PushButton, adj_left, adj_right
#Modelos de Terceros
from fuzzywuzzy import fuzz
from PyQt5.QtWidgets import (QLayout,QComboBox,QPushButton,QTableWidget,QTableWidgetItem,
                             QLineEdit, QMainWindow,QMessageBox, QHeaderView,QLabel, QDialog,
                             QVBoxLayout, QWidget, QInputDialog,QHBoxLayout,QCalendarWidget)
from PyQt5.QtCore import Qt, QDate
from sqlalchemy import Table, MetaData, create_engine, insert,delete,update 
from sqlalchemy.exc import ProgrammingError, IntegrityError
#Modulos de Python
from datetime import datetime


#####COMENTARIO DE PRUEBA

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.showDate)
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)

    def showDate(self, date=None):
        self.selected_date = date
        self.selected_date = self.calendar.selectedDate()
        self.selected_datetime = datetime.combine(self.selected_date.toPyDate(), datetime.now().time())
        self.accept()
        

    def showCalendar(self,dict={},columname=''):
        if self.exec_() == QDialog.Accepted:
            # Insertar la fecha y hora seleccionadas en la tabla
            self.date_string = self.selected_datetime.strftime('%Y-%m-%d %H:%M:%S')
            dict[columname] = self.date_string
            return self.date_string
    

def delete_widgets(layout:QLayout):
    while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

class ShowData(QMainWindow):

    def __init__(self,main_window, table_name,ip,query='',
                 filtro=None,add_row=True,operation='general',
                 from_client = False) -> None:
        super().__init__()
        self.table_name = table_name
        self.filtro = filtro
        self.ip = ip
        self.operation = operation
        self.main_window = main_window
        self.query = query
        self.from_clients = from_client
        self.add_row_bool = add_row
        self.aditional_cols()
        self.initUI()
         # Crear un objeto de tipo Engine
        self.engine = create_engine(f'postgresql://postgres:miakhalifA07@{self.ip}:5432/negocio')
        # Crear un objeto de tipo MetaData
        metadata = MetaData(bind=self.engine)
        # Obtener el objeto de tipo Table para la tabla específica
        if operation == 'inventario':
            self.tablesql = Table('inventario', metadata, autoload=True)
        else:
            self.tablesql = Table(self.table_name, metadata, autoload=True)

    def aditional_cols(self):
        self.add_col = 2
        if self.operation == 'informe':
            self.add_col = 3

    def make_table(self,results,column_names):
            # Crear la tabla y establecer los encabezados de las columnas
            self.table = QTableWidget()
            self.table.setRowCount(len(results))
            self.table.setColumnCount(len(results[0])+self.add_col)
            self.table.setHorizontalHeaderLabels(column_names)
            self.table.horizontalHeader().setSectionsMovable(True)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.table.resizeColumnsToContents()
            self.table.setHorizontalHeaderItem(len(results[0]), QTableWidgetItem("⟳"))
            self.table.setHorizontalHeaderItem(len(results[0])+1, QTableWidgetItem("X"))
            self.table.setHorizontalHeaderItem(len(results[0])+2, QTableWidgetItem("Info"))

            # Agregar los datos a la tabla
            for i, row in enumerate(results):
                self.table.setRowCount(i+1)
                for j, col in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(col)))
                update_button = QPushButton("⟳")
                update_button.clicked.connect(self.update_row)
                delete_button = QPushButton("X")
                delete_button.clicked.connect(self.delete_row)
                self.table.setColumnWidth(len(results[0]), 20)
                self.table.setColumnWidth(len(results[0])+1, 20)
                self.table.setCellWidget(i, len(results[0]), update_button)
                self.table.setCellWidget(i, len(results[0])+1, delete_button)
                if self.operation == 'informe':
                    info_button = QPushButton("¡")
                    info_button.clicked.connect(self.info_row)
                    self.table.setCellWidget(i, len(results[0])+2, info_button)

            if self.table.horizontalHeaderItem(0).text() == 'id' and not self.from_clients:
                self.table.hideColumn(0)



    def initUI(self):
        try:    
            self.title = QLabel(f"Visualización de {self.table_name.title()}")
            
            # Añadir el seleccionador de columna para 
            self.filter_col = QComboBox()
            # Crear el botón de actualizar
            self.refresh_button = QPushButton("Actualizar", self)
            self.refresh_button.clicked.connect(self.refresh_window)

            if self.query == '':
                results, column_names = self.get_table_data()
            else:
                print(self.query)
                results, column_names = self.get_table_data(self.query)
                
            self.make_table(results,column_names)
            # Agregar las columnas al seleccionador
            self.filter_col.addItems(column_names)
            self.filter_col.currentIndexChanged.connect(self.filter_table)
            self.search_bar = QLineEdit()
            self.search_bar.textChanged.connect(self.filter_table)

            add_button = QPushButton("+")
            add_button.clicked.connect(self.add_row)
            
            self.layout = QVBoxLayout()
            hbox1 = QHBoxLayout()
            hbox1.addWidget(self.title)
            hbox1.addWidget(self.refresh_button)
            hbox = QHBoxLayout()
            hbox.addWidget(self.filter_col)
            hbox.addWidget(self.search_bar)
            self.layout.addLayout(hbox1)
            self.layout.addLayout(hbox)
            self.layout.addWidget(self.table)
            if self.add_row_bool == True:
                self.layout.addWidget(add_button)
            widget = QWidget(self)
            widget.setLayout(self.layout)
            self.setCentralWidget(widget)

            
            # Ajustar el tamaño de la ventana al tamaño mínimo necesario para mostrar todos sus widgets
            table_width = self.table.sizeHint().width()
            table_height = self.table.sizeHint().height()
        
            self.setGeometry(0,0,table_width, table_height)
            
        except IndexError:
            QMessageBox.warning(self.main_window, 'Error', 'Parece que la tabla que tratas de ver esta vacia')

    def info_row(self):
        # Obtener la fila seleccionada
        current_row = self.table.currentRow()
        # Obtener el id de la fila seleccionada
        id_value = self.table.item(current_row, 0).text()
        if self.table_name == 'ventas':
            venta = DetallesVenta(self,id_venta=id_value,ip=self.ip,info=True)
            venta.informe_venta(mode=self.table_name)
        elif self.table_name == 'encargos':
            encargo = DetallesEncargo(self,id_encargo=id_value,info=True)
            encargo.informe_encargo(mode=self.table_name)
        elif self.table_name == 'cambios':
            cambio = DetallesCambio(self,id_cambio=id_value,info=True)
            cambio.informe_cambio(mode=self.table_name)

    def update_row(self):
        # Obtener la fila seleccionada
        current_row = self.table.currentRow()
        # Obtener el id de la fila seleccionada
        id_value = self.table.item(current_row, 0).text()
        # Obtener los nombres de las columnas de la tabla
        if self.operation == 'informe':
            column_names = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount()-3)]
            indices = {self.table.horizontalHeaderItem(i).text(): i for i in range(self.table.columnCount()-3)}
        else:
            column_names = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount()-2)]
            indices = {self.table.horizontalHeaderItem(i).text(): i for i in range(self.table.columnCount()-2)}
        # Eliminar la columna 'id' de la lista de nombres de columnas
        
        column_names.remove('id')

        if self.filtro is not None and len(self.filtro)>0:
            for _ in self.filtro:
                column_names.remove(_)
        # Crear un diccionario vacío para almacenar los nuevos valores de las columnas
        new_values = {}
        
        # Iterar sobre los nombres de las columnas
        for column_name in column_names:
            print(column_name)
            current_value = self.table.item(current_row,indices[column_name]).text()
            # Pedir al usuario que ingrese un nuevo valor para la columna actual
             # Pedir al usuario que ingrese un nuevo valor para la columna actual
            if column_name == 'fecha' or column_name == 'entregarel' or column_name == 'encargado':
                # Mostrar el QCalendarWidget
                calendar = CalendarDialog(self.main_window)
                calendar.showCalendar(new_values,column_name)
            else:
                value,ok = QInputDialog.getText(self,'Actualizar Fila',f"Ingresa un nuevo valor para la columna {column_name}: ",
                                            QLineEdit.Normal,current_value)
                if value == 'Si' or value == 'True':
                    value = True
                elif value == 'No' or value == 'False':
                    value = False
                else:
                    pass
                # Agregar el nuevo valor al diccionario
                if value and ok:
                    new_values[column_name] = value
                else:
                    break
        try: 
                # Crear un objeto de tipo update
            if self.operation == 'inventario':
                update_stmt = update(self.tablesql).where(self.tablesql.columns.id_prenda == id_value).values(**new_values)
            else:
                update_stmt = update(self.tablesql).where(self.tablesql.columns.id == id_value).values(**new_values)
            # Ejecutar la sentencia
            self.engine.execute(update_stmt)
            # Actualizar la tabla para mostrar los nuevos datos
            if self.from_clients:
                self.refresh_table()
            else:
                self.refresh_window()

        except ProgrammingError:
            QMessageBox.warning(self.main_window, 'Error', '''No se pudo realizar la actualización. 
              Tal vez la cancelaste o Hiciste algo mal. Intentalo de nuevo''')
            if self.from_clients:
                self.refresh_table()

    
    def delete_row(self):
        print('2')
        try:
            # Obtener el id de la fila seleccionada
            selected_row = self.table.currentRow()
            id_col = 0  # Asumimos que la columna con el id es la primera
            id_value = self.table.item(selected_row, id_col).text()

            # Crear un objeto de tipo delete
            delete_stmt = delete(self.tablesql).where(self.tablesql.columns.id == id_value)

            # Ejecutar la sentencia
            self.engine.execute(delete_stmt)

            # Actualizar la tabla
            if self.from_clients:
                self.regresh_table()
            else:
                self.refresh_window()

        except AttributeError:
            QMessageBox.warning(self.main_window, 'Error', '''No se pudo eliminar la fila. 
              Algo salió mal. Intentalo de nuevo''')
            if self.from_clients:
                self.refresh_table()
        

    def filter_table(self):
        search_text = self.search_bar.text()
        selected_column = self.filter_col.currentIndex()
        rows = self.table.rowCount()
        matches = []
        for row in range(rows):
            self.table.setRowHidden(row, True)
            item = self.table.item(row, selected_column)
            if item:
                ratio = fuzz.token_set_ratio(item.text(), search_text)
                if ratio >= 80:  # adjust this threshold as needed
                    matches.append((row, ratio))
        matches.sort(key=lambda x: x[1], reverse=True)
        for row, ratio in matches:
            self.table.setRowHidden(row, False)

    def add_row(self): ##METODO INESTABLE
        # Obtener los nombres de las columnas de la tabla
        column_names = self.tablesql.columns.keys()
        column_names.remove("id")

        if self.filtro is not None:
            for _ in self.filtro:
                column_names.remove(_)

        # Crear un diccionario vacío para almacenar los valores de las columnas
        data = {}
        # Iterar sobre los nombres de las columnas
        for column_name in column_names:
            # Pedir al usuario que ingrese un valor para la columna actual
            value,ok = QInputDialog.getText(self,'Insertar Nueva Fila',f"Ingresa un valor para la columna {column_name}: ",
                                         QLineEdit.Normal, "")
            # value = QInputDialog.getText(self,'Insertar Nueva Fila',f"Ingresa un valor para la columna {column_name}: ",QLineEdit.Normal, "")[0]
            # Agregar el valor al diccionario
            if value and ok:
                data[column_name] = value
            else:
                break

        # Crear un objeto de tipo insert
        try:
            insert_stmt = insert(self.tablesql).values(**data)
            # Ejecutar la sentencia
            self.engine.execute(insert_stmt)
            if self.from_clients:
                self.regresh_table()
            else:
                self.refresh_window()
        except IntegrityError:
            QMessageBox.warning(self.main_window, 'Error', '''No se pudo realizar la Inserción. 
              Tal vez la cancelaste o Hiciste algo mal. Intentalo de nuevo''')

    def get_table_data(self,dif_query=''):

        if dif_query == '':
            results,conn,cursor = execute_query(f'SELECT * FROM {self.table_name} ORDER BY id',self.ip,
                                                get_conncur=True)
        else: 
            results,conn,cursor = execute_query(dif_query,self.ip,get_conncur=True)
        column_names = [column[0] for column in cursor.description]
        conn.close()
        cursor.close()
        return results, column_names

    def refresh_window(self):
        current_state = self.table.horizontalHeader().saveState()
        current_geometry = self.geometry()
        current_h_scroll_value = self.table.horizontalScrollBar().value()
        current_v_scroll_value = self.table.verticalScrollBar().value()

        self.initUI()

        
        self.table.horizontalScrollBar().setValue(current_h_scroll_value)
        self.table.verticalScrollBar().setValue(current_v_scroll_value)
        self.table.horizontalHeader().restoreState(current_state)
        self.setGeometry(current_geometry)
    
    def refresh_table(self):
        self.main_window.window_info()


class Pestana(QMainWindow):
    def __init__(self, main_window, table_name,ip,edit=False,query='',filtro=None,add_row=True):
        self.main_window = main_window
        self.table_name = table_name
        self.filtro = filtro
        self.edit = edit
        self.ip = ip
        self.query=query
        self.add_row_bool = add_row 
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
        self.show_data = ShowData(self.main_window,self.table_name,self.ip,self.query,self.filtro,self.add_row_bool)
        x,y = adj_right(self.show_data)
        self.show_data.move(x,y)
        self.show_data.show()
        x,y = adj_left(self.main_window)
        self.main_window.move(x,y)



    #     today = datetime.now().strftime("%Y-%m-%d")
    #     ventas = {'Ventas': []}
    #     # Crea el diccionario con los datos de la venta
    #     data = {'name':self.result[0][0],
    #             'id_venta':self.result[0][1],
    #             'fecha':self.result[0][2].strftime("%Y-%m-%d %H:%M:%S"),
    #             'detalles':[{'prenda': self.result[i][3], 'talla': self.result[i][4],
    #              'precio': str(self.result[i][5]), 'cantidad': self.result[i][6], 'subtotal': 
    #              str(self.result[i][7])} for i in range(len(self.result))],
    #             'total':str(self.result[0][8])}
    #   #######
       
    #     if os.path.exists(f"registro_ventas/{today}.json"):
    #         # Escribe la lista de ventas con la venta actual en el archivo
    #         f = open(f"registro_ventas/{today}.json")
    #         read = json.load(f)
    #         with open(f"registro_ventas/{today}.json", "r+") as file:
    #             # Carga el contenido del archivo en formato JSON
    #             ventass = json.load(file)
    #             read['Ventas'].append(data)
    #             ventass.update(read)
    #             file.seek(0)
    #             json.dump(ventass, file, indent = 4)
    #     else:
    #         # Si no existe, abre el archivo en modo "w" (sobreescribir)
    #         with open(f"registro_ventas/{today}.json", "w") as f:
    #             # Escribe el diccionario en formato JSON en el archivo
    #             json.dump(ventas, f)
    #         # Escribe la lista de ventas con la venta actual en el archivo
    #         f = open(f"registro_ventas/{today}.json")
    #         read = json.load(f)
    #         with open(f"registro_ventas/{today}.json", "r+") as file:
    #             # Carga el contenido del archivo en formato JSON
    #             ventass = json.load(file)
    #             read['Ventas'].append(data)
    #             ventass.update(read)
    #             file.seek(0)
    #             json.dump(ventass, file, indent = 4)
    
  
    



            
        