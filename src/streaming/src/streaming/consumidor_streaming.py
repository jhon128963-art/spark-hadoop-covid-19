from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType  # (Tipos adaptados)

# --- Configuración de la Sesión de Spark ---
spark = SparkSession.builder \
    .appName("StreamingCovid") \
    .getOrCreate() 

# Reducir el nivel de log para limpiar la salida
spark.sparkContext.setLogLevel("WARN")

# --- Definición del Esquema ---
# El esquema debe coincidir con los datos JSON del productor
schema = StructType([
    # (Adaptado del esquema de sensores)
    StructField("municipio", StringType()),
    StructField("estado", StringType()),
    StructField("sexo", StringType()),
    StructField("edad", IntegerType()),
    StructField("timestamp", TimestampType())
])

# --- Lectura del Stream de Kafka ---
df_kafka = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "nuevos_casos_covid") \
    .load()

# --- Transformación de Datos ---
# Convertir el 'value' de Kafka (binario) a String y luego a JSON
parsed_df = df_kafka.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# --- Análisis en Tiempo Real: Conteo por Ventana ---
# Contar nuevos casos por 'estado' (Leve, Grave, Fallecido) en ventanas de 1 minuto
# (Adaptado de la agrupación por 'sensor_id')
windowed_counts = parsed_df \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("estado")
    ) \
    .count() \
    .orderBy(col("window").desc(), col("count").desc()) # (Ordenado para mejor visualización)

# --- Salida a Consola ---
# Mostrar los resultados en la consola
query = windowed_counts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

print(f"--- Esperando datos del stream de Kafka (topic: nuevos_casos_covid) ---")
query.awaitTermination()
