import time
import json
import random
from kafka import KafkaProducer

# Lista de municipios y estados para simular
MUNICIPIOS = ["MEDELLIN", "CALI", "BARRANQUILLA", "PASTO", "MANIZALES", "IBAGUE"]
ESTADOS = ["Leve", "Grave", "Fallecido", "Leve"] 
SEXO = ["F", "M"]

def generar_nuevo_caso():
    """ Simula un nuevo reporte de caso COVID. """
    return {
        # (Adaptado de 'sensor_id', 'temperature', 'humidity')
        "municipio": random.choice(MUNICIPIOS),
        "estado": random.choice(ESTADOS),
        "sexo": random.choice(SEXO),
        "edad": random.randint(1, 90),
        "timestamp": int(time.time())
    }

# Creamos el Productor de Kafka
productor = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Definimos el topic (debe ser el mismo que creaste)
TOPIC_NAME = 'nuevos_casos_covid'

print(f"--- Enviando mensajes al topic: {TOPIC_NAME} ---")
print("--- Presiona Ctrl+C para detener ---")

while True:
    try:
        data = generar_nuevo_caso()
       
        # Enviar datos al topic (adaptado de 'sensor_data')
        productor.send(TOPIC_NAME, value=data)
       
        print(f"Sent: {data}")
       
        # Esperar 1 segundo
        time.sleep(1)
       
    except KeyboardInterrupt:
        print("\n--- Deteniendo productor ---")
        break

productor.close()
