import json
import sys
import threading
import time
sys.path.append('C:/Users/marmu/OneDrive/Documentos/TFG/backend/app')
from models.mqtt_data_handler import actualizar_bd, procesar_mensaje
import paho.mqtt.client as mqtt
import mysql.connector

#mqtt_client_handler.py

# MQTT Client Handler Class
class mqtt_client_handler:
    MQTT_TOPIC = "wokwi-weather"
    MQTT_CLIENT_ID = "python-weather-demo"
    MQTT_BROKER = "broker.mqttdashboard.com"

    def __init__(self, broker, topic, client_id):
        self.broker = broker
        self.topic = topic
        self.client_id = client_id
        self.client = mqtt.Client(client_id=self.client_id, clean_session=True, protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    # Función que se ejecuta cuando se conecta al broker MQTT
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Conectado al broker MQTT")
            client.subscribe("wokwi-weather")  # ¡IMPORTANTE! Debe suscribirse al tópico correcto
            print(f"Escuchando en el tópico {self.topic}...\n")

        else:
            print(f"Error al conectar al broker MQTT: Código {rc}")
            sys.exit(1)

    # Función para manejar desconexiones y reconectar automáticamente
    def on_disconnect(self, client, userdata, rc):
        print(f"Desconectado del broker MQTT con código {rc}. Intentando reconectar...")
        while True:
            try:
                self.client.reconnect()
                print("Reconexion exitosa.")
                break
            except Exception as e:
                print(f"Error al reconectar: {e}")
                time.sleep(5)

    # Función que se ejecuta cuando llega un mensaje MQTT
    def on_message(self, client, userdata, msg):
        print("=" * 50) 
        print(f"Nuevo mensaje recibido en {msg.topic}"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f"Contenido del mensaje: {msg.payload.decode()}")
        procesar_mensaje(msg.payload.decode())
        
    def conectar(self):
    # Conectarse al broker MQTT y suscribirse al tópico
        try:
            self.client.connect("broker.mqttdashboard.com", 1883, 60)
            print(f"Conectado al broker MQTT")
            self.client.loop_start() # Inicia un hilo para procesar los mensajes
            print(f"Escuchando en el tópico {"wokwi-weather"}...\n")
        except Exception as e:
            print(f"Error al conectar al broker MQTT: {e}")
            sys.exit(1)

    def desconectar(self):
        print("\n Desconectando del broker MQTT...")
        self.client.loop_stop()
        self.client.disconnect()
        print("Conexiones cerradas. Saliendo del programa.")
        sys.exit(0)

    def mantener_ejecucion(self):
    # Mantener el script en ejecución y verificar conexión periódicamente
        try:
            while True:
                time.sleep(10)  # Evita que el script termine
        except KeyboardInterrupt:
            print("\nDesconectando del broker MQTT...")
            self.desconectar()
            sys.exit(0)

 




