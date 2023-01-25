from PyQt5.QtWidgets import QInputDialog,QLineEdit,QMessageBox 
from Utils.util_sql import connectsql, make_query

def clients(parent,type):
    client, ok = QInputDialog.getText(parent,f'Realizar {type.title()}',
                                        'Inserta el nombre del cliente',
                                        QLineEdit.Normal, "")
    if ok:
        phone, ok1 = QInputDialog.getText(parent,f'Realizar {type.title()}',
                                        'Inserta el teléfono del cliente', 
                                        QLineEdit.Normal, "3000000000")
        if ok1:
            if phone.isdigit() and len(phone) == 10:
                # CREAR CLIENTE
                        # Conectarse a la base de datos
                conn, cursor = connectsql(host=parent.ip)
                
                # Buscar si el cliente ya existe
                query = f"SELECT id FROM clientes WHERE nombre = '{client}' AND telefono = '{str(phone)}' "
                cursor.execute(query)
                result = cursor.fetchone()
                conn.commit()
                cursor.close()
                conn.close()
                
                if result and phone != '3000000000':
                    parent.cliente = result[0]
                    parent.bool = True
                    print('Existe')
                    # Si el cliente ya existe, retornar su ID
                    return parent.cliente, parent.bool
                else:
                    conn1, cursor1 = connectsql(host=parent.ip)
                    # Si el cliente no existe, insertar uno nuevo
                    query = f"INSERT INTO public.clientes (nombre, telefono) VALUES ('{client}', {int(phone)}) RETURNING id"
                    cursor1.execute(query)
                    result = cursor1.fetchone()
                    conn1.commit()
                    cursor1.close()
                    conn1.close()
                    print(result)
                    parent.cliente = result[0]
                    parent.bool = True
                    print('No existe')
                    return parent.cliente, parent.bool
            else:
                # El número de teléfono no es válido, muestra un mensaje de error y vuelve a mostrar el cuadro de diálogo
                QMessageBox.warning(parent, 'Error', 'El número de teléfono debe tener 10 dígitos')
                parent.bool = False
                parent.cliente = None
        else:
            parent.bool = False
            parent.cliente = None
    else:
        parent.bool = False
        parent.cliente = None
    return (parent.cliente, parent.bool)
                
def create_operation(parent,query,id_cliente,type):
    #CREAR VENTA
    conn2, cursor2 = connectsql(host=parent.ip)
    make_query(conn2,cursor2,query)

    #OBTENER id_encargo:
    conn3, cursor3 = connectsql(host=parent.ip)
    query3 = f'''SELECT Max(id) FROM {type} WHERE id_cliente = {id_cliente}'''
    cursor3.execute(query3)
    parent.id_operation= cursor3.fetchone()

    conn3.commit()
    cursor3.close()
    conn3.close()
    return parent.id_operation
   

    

def buscar_o_crear_cliente(parent,nombre, telefono):
    # Conectarse a la base de datos
    conn, cursor = connectsql(host=parent.ip)
    
    # Buscar si el cliente ya existe
    query = f"SELECT id FROM clientes WHERE nombre = '{nombre}' AND telefono = {telefono}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        # Si el cliente ya existe, retornar su ID
        return result[0]
    else:
        # Si el cliente no existe, insertar uno nuevo
        query = f"INSERT INTO clientes (nombre, telefono) VALUES ('{nombre}', {telefono}) RETURNING id"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
