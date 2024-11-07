from datetime import timedelta,datetime
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
#from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators.postgres_file_operator import PostgresFileOperator
# from operators import PostgresFileOperator

#defining DAG arguments
# You can override them on a per-task basis during operator initialization

    
    
default_args = {
     'owner': 'milo',
     'start_date': days_ago(0),
     'email': ['milo0@gmail.com'],
     'email_on_failure': False,
     'email_on_retry': False,
     'retries': 1,
     'retry_delay': timedelta(minutes=5),
 }
 # defining the DAG
 # define the DAG
dag = DAG(
     dag_id='weather_dag',
     default_args=default_args,
     schedule_interval='@hourly',
     catchup=False,
     max_active_runs=1,
     concurrency=1
 )

extract_data = BashOperator(
    task_id='extract_data',
    bash_command='python /opt/airflow/tmp/extract_data_api.py',
    dag=dag
)

create_table_db = PostgresOperator(
         task_id='create_table',
         postgres_conn_id='postgres_default',
         sql="""
         CREATE TABLE IF NOT EXISTS weather_medellin (
             city varchar(55),
             temp varchar(55),
             temp_min varchar(55),
             temp_max varchar(55),
             pressure varchar(55),
             humidity varchar(55),
             time varchar(255)
         );
         """
)

insert_data_db = PostgresFileOperator(
     task_id = "insert_data",
     operation = "write",
     config = {"table_name":"weather_medellin"}
 )

extract_data >> create_table_db >> insert_data_db