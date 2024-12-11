"""
DAG de Airflow para la ingestión y procesamiento de datos desde Oracle a BigQuery utilizando Dataflow.

Este DAG realiza las siguientes tareas:
1. Ejecuta un job de Dataflow (ingestión) que extrae datos desde una base de datos Oracle y los almacena en GCS en formato Avro.
2. Copia el archivo Avro generado desde la capa de ingest a la capa raw en GCS.
3. Ejecuta un job de Dataflow (depuración) que carga los datos desde el archivo Avro en GCS a una tabla de BigQuery.

El DAG está parametrizado para facilitar su configuración en diferentes entornos (dev, qa, prd) y para diferentes tablas.
"""

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from utils.notifications import google_chat_notification
from utils.load_sql_from_gcs import load_sql_query_from_gcs
from utils.dataflow_body import create_dataflow_body
from utils.df_job_name import ajust_job_name
from airflow.models import Variable
from datetime import datetime

# Definición de IDs de secretos necesarios para la conexión a la base de datos (si aplica)
SECRET_IDS = {
    'host': '',      # ID del secreto que contiene el host de la base de datos
    'user': '',      # ID del secreto que contiene el usuario de la base de datos
    'password': '',  # ID del secreto que contiene la contraseña de la base de datos
    'sid': ''        # ID del secreto que contiene el SID de la base de datos
}

# Obtención de variables de Airflow para configuración del DAG y de los jobs de Dataflow
CONFIG_VARS = {
    'output_bucket_ingest': Variable.get('OUTPUT_BUCKET_INGEST'),                 # Bucket de salida para la capa de ingest
    'output_bucket_raw': Variable.get('OUTPUT_BUCKET_RAW'),                       # Bucket de salida para la capa raw
    'base_path_dataflow_templates': Variable.get('TEMPLATES_PATH'),               # Ruta base donde se encuentran los templates de Dataflow
    'dataflow_workspace_bucket': Variable.get('BUCKET_DF_BATCH'),                 # Bucket de trabajo para Dataflow
    'data_ingest_service_account': Variable.get('SERVICE_ACCOUNT_DATA_INGEST'),   # Service Account utilizada para los jobs de Dataflow
    'subnetwork': Variable.get('SUBNETWORK'),                                     # Subred utilizada por Dataflow
    'network': Variable.get('NETWORK'),                                           # Red utilizada por Dataflow
    'data_ingest_project_id': Variable.get('DATA_INGEST_PROJECT_ID'),             # ID del proyecto donde se ejecuta la ingestión de datos
    'datagov_project_id': Variable.get('DATAGOV_PROJECT_ID'),                     # ID del proyecto Data Governance
    'location': Variable.get('LOCATION'),                                         # Ubicación (región) donde se ejecutan los jobs
    'lakehouse_andes_project_id': Variable.get('PROJECT_LAKEHOUSE_ID'),           # ID del proyecto Lakehouse Andes
    'env': Variable.get('ENV'),                                                   # Entorno (dev, qa, prd)
    'bucket_schemas_avro': f"schemas_avro_{Variable.get('ENV')}"                        # Bucket donde se almacenan los esquemas Avro
}

# --- Configuración de rutas y constantes específicas ---

# Nombre del DAG (debe ser el mismo nombre del archivo .py)
DAG_NAME = "<DAG_NAME>"  # Reemplazar con el nombre del archivo .py (sin la extensión)

# Fecha de procesamiento (en formato YYYYMMDD)
PROCESS_DATE = datetime.now().strftime('%Y%m%d')

# Programación del DAG (vacío en producción para ejecutar inmediatamente, None en otros entornos para no programar)
SCHEDULE = '' if CONFIG_VARS['env'] == 'prd' else None

# Bucket donde se encuentran las consultas SQL para Oracle
BUCKET_QUERY = f"querys-oracle-{CONFIG_VARS['env']}"

# Ruta y nombre del archivo SQL dentro del bucket (reemplazar con tu ruta)
OBJECT_QUERY_NAME = f"path/query/file.sql"

# Carga la consulta SQL desde GCS
QUERY = load_sql_query_from_gcs(BUCKET_QUERY, OBJECT_QUERY_NAME)

# Nombre de la tabla en Oracle (debe estar en mayúsculas)
ORACLE_TABLE_NAME = "<ORACLE_TABLE_NAME>"

# Nombre del dataset y tabla en BigQuery (reemplazar con los valores correspondientes)
BIGQUERY_DATASET = "<bigquery_dataset>"  # Nombre del dataset en BigQuery
BIGQUERY_TABLE_NAME = "<bigquery_table>"  # Nombre de la tabla en BigQuery (en minúsculas)

# Nombre del procedimiento almacenado que realiza el merge en caso de usar tabla staging
STORE_PROCEDURE = "<name_store_prcedure>"

# Ruta del esquema Avro en GCS (ejemplo: core/menu_andes/OPSANDES/afi_persona.avsc)
PATH_AVRO_SCHEMA = "<PATH_AVRO_SCHEMA>"

# Ruta de salida para el archivo Avro en la capa de ingest (reemplazar con tu ruta)
INGEST_OUTPUT_PATH = "<INGEST_OUTPUT_PATH>"

# Ruta del archivo de mapeo de tipos de datos (archivo JSON)
MAPPING_SCHEMA_PATH = "<MAPPING_SCHEMA_PATH>"

# Ruta de entrada del archivo Avro en la capa raw (reemplazar con tu ruta, conservar la variable PROCESS_DATE y ORACLE_TABLE_NAME)
RAW_INPUT_AVRO = f"<RAW_INPUT_AVRO_PATH>/{PROCESS_DATE}/{ORACLE_TABLE_NAME}.avro"

# Parámetros para nombrar los jobs de Dataflow (reemplazar con los valores correspondientes)
ORIGEN = "<origen>"           # Origen de los datos (ejemplo: 'menuandes')
DOMINIO = "<dominio>"         # Dominio de los datos
SUBDOMINIO = "<subdominio>"   # Subdominio de los datos
TABLA = "<tabla>"             # Nombre de la tabla minusculas

# Argumentos por defecto para el DAG
DEFAULT_ARGS = {
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    "retries": 0,
}

# Configuración del cuerpo (body) para el job de Dataflow de ingestión
ingest_body = create_dataflow_body(
    # Nombre del job de Dataflow (reemplazar <origen>, <dominio>, <subdominio>, <tabla>)
    job_name= ajust_job_name(f"df-batch-{ORIGEN}-ingest-{DOMINIO}-{SUBDOMINIO}-{TABLA}"),

    # Ruta al archivo JSON del template de Dataflow (Jdbc-To-Gcs-Avro)
    container_spec_path=f"{CONFIG_VARS['base_path_dataflow_templates']}/Jdbc-To-Gcs-Avro/Jdbc-To-Gcs-Avro.json",

    # Parámetros para el job de Dataflow
    parameters={
        'secret_id_host': SECRET_IDS['host'],  # ID del secreto del host de la base de datos
        'port': '1521',                        # Puerto de la base de datos Oracle
        'secret_id_service_name': SECRET_IDS['sid'],  # ID del secreto del SID (Service Name) de la base de datos
        'secret_id_user': SECRET_IDS['user'],  # ID del secreto del usuario de la base de datos
        'secret_id_password': SECRET_IDS['password'],  # ID del secreto de la contraseña de la base de datos
        'datagov_project_id': CONFIG_VARS['datagov_project_id'],  # ID del proyecto de Data Governance
        'query': QUERY,                        # Consulta SQL a ejecutar en Oracle
        'table_name': ORACLE_TABLE_NAME,       # Nombre de la tabla en Oracle
        'avro_schema_gcs_path': f"gs://{CONFIG_VARS['bucket_schemas_avro']}/{PATH_AVRO_SCHEMA}",  # Ruta al esquema Avro en GCS
        'output_path': f"gs://{CONFIG_VARS['output_bucket_ingest']}/{INGEST_OUTPUT_PATH}",        # Ruta de salida en GCS para el archivo Avro
        'output_prefix': ORACLE_TABLE_NAME,    # Prefijo para el archivo de salida
        'data_type_schema_gcs_path': f"gs://data_type_mappings_{CONFIG_VARS['env']}/{MAPPING_SCHEMA_PATH}",  # Ruta al mapeo de tipos de datos
    }
)

# Configuración del cuerpo (body) para el job de Dataflow de depuración
depure_body = create_dataflow_body(
    # Nombre del job de Dataflow (reemplazar <origen>, <dominio>, <subdominio>, <tabla>)
    job_name=ajust_job_name(f"df-batch-{ORIGEN}-depure-{DOMINIO}-{SUBDOMINIO}-{TABLA}"),

    # Ruta al archivo JSON del template de Dataflow (Depure_Avro_To_Bigquery)
    container_spec_path=f"{CONFIG_VARS['base_path_dataflow_templates']}/Depure_Avro_To_Bigquery.json",

    # Parámetros para el job de Dataflow
    parameters={
        'input_avro': f"gs://{CONFIG_VARS['output_bucket_raw']}/{RAW_INPUT_AVRO}",  # Ruta del archivo Avro de entrada en la capa raw
        'bigquery_table': f"{CONFIG_VARS['lakehouse_andes_project_id']}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE_NAME}",  # Tabla de destino en BigQuery
        'write_disposition':'WRITE_TRUNCATE' # Write_truncate solo en caso de realizar merge

        # Los siguientes parámetros solo se incluyen si se desea realizar un upsert
        # 'upsert': 'true',                         # Indica si se realiza un upsert (true/false)
        # 'primary_keys': '<primary_key_column>',   # Clave primaria para el upsert (reemplazar con la columna correspondiente)
        # 'staging_table': f"{CONFIG_VARS['lakehouse_andes_project_id']}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE_NAME}_staging"  # Tabla staging en BigQuery para el upsert
    },
    # Sobrescritura de parámetros de entorno
    environment_overrides={
        'ipConfiguration': 'WORKER_IP_PRIVATE'  # Configuración de IP privada para los workers
    }
)

# Definición del DAG de Airflow
with DAG(
    DAG_NAME,                         # Nombre del DAG
    default_args=DEFAULT_ARGS,        # Argumentos por defecto
    schedule_interval=SCHEDULE,       # Programación del DAG
    catchup=False,                    # No ejecutar tareas atrasadas
    tags=[CONFIG_VARS['env']]         # Etiquetas (tags) del DAG (por ejemplo, el entorno)
) as dag:

    # Tarea inicial (DummyOperator)
    start = DummyOperator(
        task_id='start'
    )

    # Tarea de ingestión (ejecuta el job de Dataflow para extraer datos de Oracle a GCS en formato Avro)
    ingest = DataflowStartFlexTemplateOperator(
        task_id='ingest',
        body=ingest_body,
        location=CONFIG_VARS['location'],
        project_id=CONFIG_VARS['data_ingest_project_id'],
        on_failure_callback=google_chat_notification  # Notificación en caso de falla
    )

    # Tarea de copia del archivo Avro de la capa ingest a la capa raw
    raw = GCSToGCSOperator(
        task_id='raw',
        source_bucket=CONFIG_VARS['output_bucket_ingest'],  # Bucket de origen (capa ingest)
        source_object=f"{INGEST_OUTPUT_PATH}/{ORACLE_TABLE_NAME}.avro",  # Objeto (archivo Avro) de origen
        destination_bucket=CONFIG_VARS['output_bucket_raw'],  # Bucket de destino (capa raw)
        destination_object=RAW_INPUT_AVRO,  # Objeto (ruta) de destino
        move_object=False,  # No mover el objeto, solo copiarlo
        on_failure_callback=google_chat_notification  # Notificación en caso de falla
    )

    # Tarea de depuración (ejecuta el job de Dataflow para cargar datos desde GCS a BigQuery)
    depure = DataflowStartFlexTemplateOperator(
        task_id='depure',
        body=depure_body,
        location=CONFIG_VARS['location'],
        project_id=CONFIG_VARS['data_ingest_project_id'],
        on_failure_callback=google_chat_notification  # Notificación en caso de falla
    )
    # Tarea para realizar el upsert en caso de aplicar 
    merge_table = BigQueryInsertJobOperator(
        task_id=f"merge_table",  # ID de la tarea, dinámicamente generado
        configuration={
            "query": {
                "query": f"CALL `{CONFIG_VARS['lakehouse_andes_project_id']}.staging_dataset.{STORE_PROCEDURE}`()",  # Llamada al procedimiento almacenado
                "useLegacySql": False,  # Usar SQL estándar en lugar de Legacy SQL
                "priority": "BATCH",  # Prioridad del trabajo en BigQuery
            }
        },
        location=CONFIG_VARS['location'],  # Ubicación geográfica de BigQuery
        on_failure_callback=google_chat_notification  # Callback en caso de fallo de la tarea
    )

    # Tarea final (DummyOperator)
    end = DummyOperator(
        task_id='end'
    )

    # Definición de la secuencia de tareas
    start >> ingest >> raw >> depure >> merge_table >> end
