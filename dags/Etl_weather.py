from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
#from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
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
     description='etl process weather',
     schedule_interval=timedelta(days=1),
 )

extract_data = BashOperator(
    task_id='extract_data',
    bash_command='python /opt/airflow/plugins/tmp/extract_data_api.py',
    dag=dag
)

create_table = PostgresOperator(
         task_id='create_table',
         postgres_conn_id='postgres_default',
         sql="""
         CREATE TABLE IF NOT EXISTS weather_medellin (
             city varchar(255),
             temp float,
             temp_min float,
             temp_max float,
             pressure integer,
             humidity integer,
             time timestamp
         );
         """
)

extract_data >> create_table