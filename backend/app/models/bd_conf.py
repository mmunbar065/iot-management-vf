import mysql.connector as connector
#bd_conf.py
# Conexión a la base de datos
def connect():
    return connector.connect(
        host="localhost",
        user="root",
        database="iot_management"
    )

