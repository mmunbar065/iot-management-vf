from mqtt_client_handler import mqtt_client_handler as MQTTClient
import time
import sys


# MQTT Server Parameters
MQTT_CLIENT_ID = "python-weather-demo"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "wokwi-weather"

if __name__ == "__main__":
    # Crear una instancia del cliente MQTT

    mqtt_client = MQTTClient("broker.mqttdashboard.com", "wokwi-weather", "python-weather-demo")
    
    try:
        # Conectar al broker MQTT y suscribirse al tópico
        mqtt_client.__init__(MQTT_BROKER, MQTT_TOPIC, MQTT_CLIENT_ID)
        mqtt_client.conectar()
    except Exception as e:
        print(f"Error durante la conexión: {e}")
        sys.exit(1)

    try:
        while True:
            time.sleep(10)  # Evita que el script termine
    except KeyboardInterrupt:
        print("\n Desconectando del broker MQTT...")
        mqtt_client.desconectar()
        print("Conexiones cerradas. Saliendo del programa.")
        sys.exit(0)
    # Mantener el script en ejecución
    #mqtt_client.mantener_ejecucion()
# import json
# import sys
# import threading
# import time
# import paho.mqtt.client as mqtt
# import mysql.connector

# # MQTT Server Parameters
# MQTT_CLIENT_ID = "python-weather-demo"
# MQTT_BROKER = "broker.mqttdashboard.com"
# MQTT_TOPIC = "wokwi-weather"

# # Conexión a la base de datos MySQL
# attempts = 0
# db = None
# while attempts < 3:
#     try:
#         db = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             database="iot_management"
#         )
#         cursor = db.cursor()
#         print("✅ Conexión a la base de datos establecida correctamente.")
#         break
#     except mysql.connector.Error as e:
#         print(f"❌ Error al conectar a la base de datos: {e}")
#         print("Intentando reconectar...")
#         attempts += 1
#         time.sleep(2**attempts)  # Exponential backoff

# if not db:
#     print("No se pudo conectar a la base de datos. Saliendo del programa.")
#     sys.exit(1)

# # Función para manejar la conexión al broker MQTT
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("✅ Conectado exitosamente al broker MQTT")
#         client.subscribe(MQTT_TOPIC)
#     else:
#         print(f"❌ Error al conectar al broker MQTT: Código {rc}")
#         sys.exit(1)

# # Función para actualizar la base de datos
# def actualizar_bd(temperatura, humedad):
#     """Actualiza la base de datos en un hilo separado."""
#     try:
#         cursor = db.cursor()
#         query = """
#         UPDATE devices 
#         SET temperature = %s, humidity = %s, last_update = NOW() 
#         WHERE type = 'Sensor Temperatura' OR type = 'Sensor Humedad'
#         """
#         values = (temperatura, humedad)
#         cursor.execute(query, values)
#         db.commit()
#         print("✅ Base de datos actualizada correctamente.\n")
#     except Exception as e:
#         print(f"❌ Error al actualizar la base de datos: {e}")

#  # Función para manejar desconexiones y reconectar automáticamente
# def on_disconnect(client, userdata, rc):
#     print(f"Desconectado del broker MQTT con código {rc}. Intentando reconectar...")
#     while True:
#         try:
#             client.reconnect()
#             print("Reconexion exitosa.")
#             break
#         except Exception as e:
#             print(f"Error al reconectar: {e}")
#             time.sleep(5)

# # Función que se ejecuta cuando llega un mensaje MQTT
# def on_message(client, userdata, msg):
#     print("=" * 50) 
#     print(f"Nuevo mensaje recibido en {msg.topic}"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     print(f"Contenido del mensaje: {msg.payload.decode()}")
    
#     try:
#         # Convertimos el mensaje JSON en un diccionario
#         data = json.loads(msg.payload.decode())
#         temperatura = data.get("temp")
#         humedad = data.get("humidity")

#         # Verificamos que se recibieron datos válidos
#         if temperatura is not None and humedad is not None:
#             print(f"Datos extraídos - Temperatura: {temperatura}°C, Humedad: {humedad}%")

#             # Actualizar la base de datos con threading
#             thread = threading.Thread(target=actualizar_bd, args=(temperatura, humedad))
#             thread.start()

#         else:
#             print("Datos incompletos en el mensaje recibido.")

#     except json.JSONDecodeError:
#         print("Error: No se pudo decodificar el JSON correctamente.")
#     except Exception as e:
#         print(f"Error procesando el mensaje: {e}")

# # Configuración del cliente MQTT
# client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, protocol=mqtt.MQTTv311, transport="tcp")
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_message = on_message 

# # Conectarse al broker MQTT y suscribirse al tópico
# try:
#     client.connect(MQTT_BROKER, 1883, 60)
#     client.loop_start() # Inicia un hilo para procesar los mensajes
#     print(f"Escuchando en el tópico {MQTT_TOPIC}...\n")
# except Exception as e:
#     print(f"Error al conectar al broker MQTT: {e}")
#     sys.exit(1)


# # Mantener el script en ejecución y verificar conexión periódicamente
# try:
#     while True:
#         time.sleep(10)  # Evita que el script termine
# except KeyboardInterrupt:
#     print("\n Desconectando del broker MQTT...")
#     client.loop_stop()
#     client.disconnect()
#     db.close()
#     print("Conexiones cerradas. Saliendo del programa.")
#     sys.exit(0)