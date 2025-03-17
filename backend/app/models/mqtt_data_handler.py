import json
import sys
import threading
import time
from models.bd_conf import connect

#mqtt_data_handler.py


def actualizar_bd(temperatura, humedad):
    """Función para actualizar la base de datos en un hilo separado."""
    try:
        db = connect()  # Conectar a la base de datos
        cursor =  db.cursor()
        query = """
        UPDATE devices 
        SET temperature = %s, humidity = %s, last_update = NOW() 
        WHERE type = 'Sensor Temperatura' OR type = 'Sensor Humedad'
        """
        values = (temperatura, humedad)
        cursor.execute(query, values)
        db.commit()
        print("Base de datos actualizada correctamente.\n")
    except Exception as e:
        print(f"Error al actualizar la base de datos: {e}")

# Función que se ejecuta cuando llega un mensaje MQTT
def procesar_mensaje(mensaje):     
    try:
        # Convertimos el mensaje JSON en un diccionario
        data = json.loads(mensaje)
        temperatura = data.get("temp")
        humedad = data.get("humidity")

        # Verificamos que se recibieron datos válidos
        if temperatura is not None and humedad is not None:
            print(f"Datos extraídos - Temperatura: {temperatura}°C, Humedad: {humedad}%")
            # Actualizar la base de datos en un hilo separado
            thread = threading.Thread(target=actualizar_bd, args=(temperatura, humedad))
            thread.start()
        else:
            print("Datos incompletos en el mensaje recibido.")
    except json.JSONDecodeError:
        print("Error: No se pudo decodificar el JSON correctamente.")
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

