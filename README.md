# Proyecto: Análisis de Casos COVID-19 en Colombia (Batch y Streaming)

Este proyecto implementa una solución de procesamiento de datos en batch y en tiempo real utilizando Apache Spark y Apache Kafka, basado en los instructivos del curso (Anexo 2 y Anexo 3). El objetivo es analizar la propagación histórica del COVID-19 en Colombia y monitorear nuevos casos reportados.

## 1. Definición del Problema y Conjunto de Datos

* **Problema:** Realizar un análisis retrospectivo (batch) de la propagación del virus, identificando las zonas más afectadas y los patrones demográficos. Simultáneamente, simular un sistema de vigilancia epidemiológica (streaming) que procese nuevos casos reportados en tiempo real.
* **Conjunto de Datos:** Casos positivos de COVID-19 en Colombia.
* **Fuente:** Portal de Datos Abiertos de Colombia.
* **API del Dataset (CSV):** `https://www.datos.gov.co/resource/gt2j-8ykr.csv`

## 2. Descripción de la Solución

La solución se divide en dos partes, implementadas con Python y Spark en el entorno de la máquina virtual proporcionada.

### Procesamiento en Batch
1.  **Carga:** Se descargan los datos históricos (un archivo CSV de gran volumen) desde la API de Datos Abiertos y se cargan en el sistema de archivos HDFS de Hadoop.
2.  **Análisis:** Un script de PySpark (`src/batch/procesamiento_batch.py`), similar al `tarea3.py` del instructivo, lee este CSV desde HDFS. Realiza un análisis exploratorio (EDA) para determinar el conteo de casos por departamento, el estado de los pacientes (Fallecido, Leve, etc.) y la distribución por edad.
3. **Almacenamiento:** Los resultados del análisis se muestran en la consola.

### Procesamiento en Tiempo Real (Spark Streaming & Kafka)
1.  **Productor de Kafka:** Un script (`src/streaming/productor_kafka.py`) simula la llegada de **nuevos reportes de casos**. 
Genera datos aleatorios (ej. `{"municipio": "CALI", "estado": "Leve", "edad": 45}`) y los envía a un topic de Kafka llamado `nuevos_casos_covid`.
2.  **Consumidor Spark Streaming:** Un script (`src/streaming/consumidor_streaming.py`) se conecta a Spark y se suscribe al topic de Kafka 
3.  **Análisis:** Procesa los datos en micro-lotes, contando el número de nuevos casos reportados por estado (Leve, Grave, Fallecido) en ventanas de tiempo de 1 minuto.
4.  **Visualización:** Muestra los resultados del conteo en tiempo real en la consola.

## 3. Instrucciones de Ejecución

Estas instrucciones asumen que ya tienes Hadoop, Spark y Kafka instalados y configurados en tu máquina virtual.

### Prerrequisitos
* Bibliotecas de Python instaladas:
    ```bash
    # (Como usuario vboxuser)
    sudo apt install -y python3-pip
    sudo pip install pyspark 
    pip install kafka-python
    ```

### Paso 1: Clonar este Repositorio
```bash
# (Como usuario vboxuser)
git clone [https://github.com/tu-companero/proyecto-spark-covid-colombia.git](https://github.com/tu-companero/proyecto-spark-covid-colombia.git)
cd proyecto-spark-covid-colombia
