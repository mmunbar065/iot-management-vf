import mysql.connector as connector
from flask import Flask, jsonify, request, make_response

# devices_model.py

def get_devices_model(cursor, sort_by='id', order='ASC'):
    sort_by = request.args.get('sort_by', 'id')  # Por defecto ordena por ID
    order = request.args.get('order', 'ASC')  # Por defecto orden ascendente
    valid_columns = ['id', 'name', 'type', 'status', 'timestamp', 'last_update', 'temperature', 'humidity', 'pressure', 'battery_level', 'last_motion']
    valid_orders = ['ASC', 'DESC']

    if sort_by not in valid_columns:
        return jsonify({'error': 'Parámetro de ordenación inválido'}), 400

    if order.upper() not in valid_orders:
        return jsonify({'error': 'Parámetro de orden inválido, debe ser ASC o DESC'}), 400

    query = f"SELECT * FROM devices ORDER BY {sort_by} {order.upper()}"  # Orden ascendente o descendente
    try:
        cursor.execute(query)
        return cursor.fetchall(), None
    except connector.Error as err:
        return None, f'Error al obtener dispositivos: {err}'

def add_device_model(cursor, db, new_device):
    # Validación: comprobamos que todos los campos obligatorios están presentes
    if not new_device.get('name') or not new_device.get('type') or not new_device.get('status'):
        # Si falta algún campo, devolvemos un error (400 Bad Request)
        return jsonify({'error': 'Faltan campos obligatorios (name, type, status)'}), 400
    query="INSERT INTO devices (name,type,status,battery_level) VALUES (%s,%s,%s,%s)"
    values=(new_device['name'],new_device['type'],new_device['status'],new_device['battery_level'])
    try:
        cursor.execute(query,values)
    except connector.Error as err:
        return jsonify({'error': f'Error al añadir el dispositivo: {err}'}), 500
    db.commit()
    # Devolvemos un mensaje de éxito con el estado 201 (Created)
    return jsonify({'message': 'Dispositivo añadido exitosamente', 'Devices': new_device}), 201

def update_device_model(cursor, db, device_id, updated_device):
     # Obtenemos los valores actuales para evitar sobrescribir con NULL
    cursor.execute("SELECT * FROM devices WHERE id = %s", (device_id,))
    existing_device = cursor.fetchone()
    print(existing_device)
    if not existing_device:
        return jsonify({'message': 'No se encontró el dispositivo con el ID proporcionado'}), 404
    
    # Usamos los valores actuales si no se envían nuevos datos
    name = updated_device.get('name', existing_device['name'])
    print(name)
    type = updated_device.get('type', existing_device['type'])
    print(type)
    status = updated_device.get('status', existing_device['status'])
    print(status)

    query = "UPDATE devices SET name=%s, type=%s, status=%s WHERE id=%s"
    values = (name, type, status, device_id)
    print(values)

    try:
        cursor.execute(query, values)

        db.commit()

    except connector.Error as err:
        return jsonify({'error': f'Error al actualizar el dispositivo: {err}'}), 500
    except Exception as e:
        import traceback
        print("ERROR en actualización:", traceback.format_exc())  # 🔍 Imprimir error en consola
        return jsonify({'error': str(e)}), 500
    return jsonify({
        'message': f'Dispositivo con ID {device_id} actualizado',
        'device': {'id': device_id, 'name': name, 'type': type, 'status': status}
    }), 200

def toggle_device_model(cursor, db, device_id, new_status):
    query = "UPDATE devices SET status=%s WHERE id=%s"
    values = (new_status, device_id)
    print(values)
    print(query)
    print(cursor)
    try:
        cursor.execute(query, values)
        print(cursor)
        cursor.fetchall()
        cursor.close()
        db.commit()
        return None  # Sin errores
    except connector.Error as err:
        return f'Error al cambiar el estado del dispositivo: {err}'
    

def delete_device_model(cursor, db, device_id):
    query = "DELETE FROM devices WHERE id=%s"
     
    try:
        cursor.execute(query,(device_id,))
    except mysql.connector.Error as err:
        return jsonify({'error': f'Error al eliminar el dispositivo: {err}'}), 500
        
    db.commit()
    if cursor.rowcount==0:
        return jsonify({'message': 'No se encontró el dispositivo con el ID proporcionado'}), 404
    return jsonify({'message': f'Dispositivo con ID {device_id} eliminado'}), 200
   
   