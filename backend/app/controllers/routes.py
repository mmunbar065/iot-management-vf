from flask import Flask, jsonify, request, make_response
from mysql import connector
from flask_cors import CORS
import sys
sys.path.append('C:/Users/marmu/OneDrive/Documentos/TFG/backend/app')
from models.devices_model import get_devices_model, add_device_model, update_device_model, toggle_device_model, delete_device_model
from models.bd_conf import connect

app = Flask(__name__)
CORS(app)


#cursor=db.cursor(dictionary=True) #Para que los resultados sean en formato diccionario

# Ruta para obtener todos los dispositivos (método GET)
@app.route('/devices', methods=['GET'])
def get_devices():
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    devices, error = get_devices_model(cursor)
    cursor.close()
    connection.close()
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'Devices': devices}), 200


# # Ruta para añadir un nuevo dispositivo (método POST)
# @app.route('/add_device', methods=['POST'])
# def add_device():
#     connection = connect()
#     cursor = connection.cursor(dictionary=True)
#     new_device = request.get_json()
#     if not new_device.get('name') or not new_device.get('type') or not new_device.get('status'):
#         return jsonify({'error': 'Faltan campos obligatorios (name, type, status)'}), 400
#     devices, error = add_device_model(cursor, connection, new_device)  
#     if error:
#         return jsonify({'error': error}), 500
#     return jsonify({'message': 'Dispositivo añadido exitosamente', 'Devices': new_device}), 201

# Ruta para añadir un nuevo dispositivo (método POST)
@app.route('/add_device', methods=['POST'])
def add_device():
    db = connect()
    cursor = db.cursor(dictionary=True)
    # Obtenemos los datos enviados por el cliente
    new_device = request.get_json()
    # Validación: comprobamos que todos los campos obligatorios están presentes
    if not new_device.get('name') or not new_device.get('type') or not new_device.get('status'):
        # Si falta algún campo, devolvemos un error (400 Bad Request)
        return jsonify({'error': 'Faltan campos obligatorios (name, type, status)'}), 400
    query="INSERT INTO devices (name,type,status,battery_level) VALUES (%s,%s,%s,%s)"
    values=(new_device['name'],new_device['type'],new_device['status'],new_device['battery_level'])
    try:
        cursor.execute(query,values)
        cursor.close() # Cerramos el cursor para evitar fugas de memoria
    except connector.Error as err:
        return jsonify({'error': f'Error al añadir el dispositivo: {err}'}), 500
    db.commit()
    db.close() # Cerramos la conexión a la base de datos
    # Devolvemos un mensaje de éxito con el estado 201 (Created)
    return jsonify({'message': 'Dispositivo añadido exitosamente', 'Devices': new_device}), 201



    
@app.route('/update_device/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    updated_device = request.get_json()
    print("JSON recibido:", updated_device)  # 🔍 Ver qué está recibiendo

    # Obtenemos los valores actuales para evitar sobrescribir con NULL
    cursor.execute("SELECT * FROM devices WHERE id = %s", (device_id,))
    existing_device = cursor.fetchone()

    if not existing_device:
        return jsonify({'message': 'No se encontró el dispositivo con el ID proporcionado'}), 404
    
    # Usamos los valores actuales si no se envían nuevos datos
    name = updated_device.get('name', existing_device['name'])
    type = updated_device.get('type', existing_device['type'])
    status = updated_device.get('status', existing_device['status'])
    print(name, type, status)
    query = "UPDATE devices SET name=%s, type=%s, status=%s WHERE id=%s"
    values = (name, type, status, device_id)

    try:
        cursor.execute(query, values)
        cursor.close()
        connection.commit()
        connection.close()
    except connector.Error as err:
        return jsonify({'error': f'Error al actualizar el dispositivo: {err}'}), 500

    return jsonify({
        'message': f'Dispositivo con ID {device_id} actualizado',
        'device': {'id': device_id, 'name': name, 'type': type, 'status': status}
    }), 200
   
# @app.route('/update_device/<int:device_id>', methods=['PUT'])
# def update_device(device_id):
#     connection = connect()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         updated_device = request.get_json()
#         print("JSON recibido:", updated_device)  # 🔍 Ver qué está recibiendo
#     except Exception as e:
#         return jsonify({"error": "Error procesando JSON"}), 400
#     print(updated_device)
#     devices, error = update_device_model(cursor, connection, device_id, updated_device)
#     print(cursor)
#     if error:
#         return jsonify({'error': error}), 500
#     return jsonify({'message': f'Dispositivo con ID {device_id} actualizado', 'device': updated_device}), 200


# Ruta para cambiar el estado de un dispositivo (método PUT)
@app.route('/toggle_device/<int:device_id>', methods=['PUT'])
def toggle_device(device_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    data = request.get_json()
    print(data)
    new_status = data.get('status')
    print(new_status)
    if new_status not in ['on', 'off']:
        return jsonify({'error': 'Estado inválido. Debe ser "on" o "off"'}), 400  
    error = toggle_device_model(cursor, connection, device_id, new_status)
    print(error)
    if error:
        return jsonify({'error': error}), 500

    return jsonify({'message': f'Estado del dispositivo con ID {device_id} actualizado a {new_status}'}), 200


# Ruta para eliminar un dispositivo por ID (método DELETE)
@app.route('/delete_device/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    devices, error = delete_device_model(cursor, connection, device_id)
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'message': f'Dispositivo con ID {device_id} eliminado'}), 200
 

if __name__=="__main__": #Para que se ejecute el servidor de Flask al ejecutar este archivo y no al importarlo 
    app.run(debug=True) #Para que se reinicie el servidor automáticamente al guardar cambios en el código
