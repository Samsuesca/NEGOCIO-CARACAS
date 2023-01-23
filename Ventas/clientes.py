from PyQt5.QtWidgets import QInputDialog,QLineEdit,QMessageBox 
from Utils.util_sql import connectsql, make_query

def insertar(parent,type,insert_query):
    client, ok = QInputDialog.getText(parent,f'Realizar {type}',
                                        'Inserta el nombre del cliente',
                                        QLineEdit.Normal, "")
    if ok:
        phone, ok1 = QInputDialog.getText(parent,f'Realizar {type}',
                                        'Inserta el teléfono del cliente', 
                                        QLineEdit.Normal, "3000000000")
        if ok1:
            if phone.isdigit() and len(phone) == 10:
                # CREAR CLIENTE
                conn, cursor = connectsql(host=parent.ip)
                # Construir la consulta para insertar una nueva fila
                query = f'''INSERT INTO public.clientes (nombre, telefono)
                VALUES ('{client}',{int(phone)})'''
                # Ejecutar la consulta
                make_query(conn,cursor, query)

                #OBTENER ID_CLIENTE:
                conn1, cursor1 = connectsql(host=parent.ip)
                query1 = f'''SELECT Max(id) FROM clientes WHERE nombre = '{client}' '''
                cursor1.execute(query1)
                id_cliente= cursor1.fetchone()
                conn1.commit()
                cursor1.close()
                conn1.close()
        
                #CREAR VENTA
                conn2, cursor2 = connectsql(host=parent.ip)
                make_query(conn2,cursor2, insert_query)
            
                #OBTENER id_encargo:
                conn3, cursor3 = connectsql(host=parent.ip)
                query3 = f'''SELECT Max(id) FROM {type} WHERE id_cliente = {id_cliente[0]}'''
                cursor3.execute(query3)
                parent.id_operation= cursor3.fetchone()
            
                conn3.commit()
                cursor3.close()
                conn3.close()
                parent.bool = True
            else:
                # El número de teléfono no es válido, muestra un mensaje de error y vuelve a mostrar el cuadro de diálogo
                QMessageBox.warning(parent, 'Error', 'El número de teléfono debe tener 10 dígitos')
                parent.bool = False
        else:
            parent.bool = False
    else:
        parent.bool = False

    return parent.bool,id_cliente,parent.id_operation