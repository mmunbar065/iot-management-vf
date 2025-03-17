import time
import json
import paho.mqtt.client as mqtt  # Usamos paho-mqtt en lugar de umqtt.simple
import random  # Usamos random para simular el sensor DHT22.

# Parámetros de simulación del sensor DHT22
MQTT_CLIENT_ID = "python-weather-demo"
MQTT_BROKER ="broker.mqttdashboard.com"
MQTT_TOPIC ="wokwi-weather"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_QOS = 1
SENSOR_INTERVAL = 2
SENSOR_MIN_TEMP =20
SENSOR_MAX_TEMP = 30
SENSOR_MIN_HUM = 40
SENSOR_MAX_HUM = 60


# Función para simular la lectura del sensor DHT22
def leer_sensor_dht22():
    try:
        temperatura = round(random.uniform(SENSOR_MIN_TEMP, SENSOR_MAX_TEMP), SENSOR_INTERVAL)  # Genera temperatura aleatoria
        humedad = round(random.uniform(SENSOR_MIN_HUM, SENSOR_MAX_HUM), SENSOR_INTERVAL)  # Genera humedad aleatoria
        return temperatura, humedad
    except Exception as e:
        print(f"Error al leer el sensor DHT22: {e}")
        return None, None


# Función para conectarse al broker MQTT
def on_connect(client, userdata, flags, rc): # rc es el código de retorno
    if rc == 0: # 0 indica que la conexión fue exitosa
        print("Conectado exitosamente al broker MQTT")
        print("Publicando datos en el tópico", MQTT_TOPIC)
    else: # Cualquier otro código de retorno indica un error
        print(f"Error al conectar al broker MQTT: Código {rc}") 
        print("Intentando reconectar...")
        client.reconnect()  # Intenta reconectar al broker

# Función de validación para verificar el envío
def on_publish(client, userdata, mid):
    print(f"Mensaje {mid} publicado exitosamente")

# Inicialización del cliente MQTT
client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_publish = on_publish

# Conexión al broker MQTT
try:
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)  # El puerto 1883 es el predeterminado para MQTT sin SSL
    client.loop_start()
except Exception as e:
    print(f"Error al conectar al broker MQTT: {e}")
    exit(1)

prev_weather = ""
while True:
    print("Midiendo condiciones climáticas...")
    temperatura, humedad = leer_sensor_dht22()
    message = json.dumps({
        "temp": temperatura,
        "humidity": humedad,
    })
    if message != prev_weather:
        print("Actualizado!")
        print(f"Enviando al tópico MQTT {MQTT_TOPIC}: {message}")
        result = client.publish(MQTT_TOPIC, message, retain=True)  # Retain para que nuevos suscriptores reciban el último mensaje
        status = result.rc
        if status == 0:
            print("Mensaje enviado correctamente")
        else:
            print("Error al enviar mensaje")
        prev_weather = message
    else:
        print("Sin cambios en los valores")
    time.sleep(MQTT_KEEPALIVE)  # Reducido para mejorar la comunicación y evitar desconexiones
