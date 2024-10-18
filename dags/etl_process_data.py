# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
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
    dag_id='etl_dag',
    default_args=default_args,
    description='etl process',
    schedule_interval=timedelta(days=1),
)
# define the tasks
# define the first task
dowload_data = BashOperator(
    task_id='download-data',
    bash_command='curl https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz -o /opt/airflow/process_data'
)

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xvf /opt/airflow/process_data',
    dag=dag,
)
# define the second task
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d "," -f 1-4 /opt/airflow/process_data/vehicle-data.csv > /opt/airflow/process_data/csv_data.csv',
    dag=dag,
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -d "\t" -f 5,6,7 /opt/airflow/process_data/tollplaza-data.tsv > /opt/airflow/process_data/tsv_data.csv',
    dag=dag,
)

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -c 58-61,62-67 /opt/airflow/process_data/payment-data.txt > /opt/airflow/process_data/fixed_width_data.csv',
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste /opt/airflow/process_data/csv_data.csv /opt/airflow/process_data/tsv_data.csv /opt/airflow/process_data/fixed_width_data.csv > /opt/airflow/process_data/consolidate_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='extransform_data',
    bash_command="cut -d ',' -f 4 /opt/airflow/process_data/consolidate_data.csv | tr '[:lower:]' '[:upper:]' > /opt/airflow/process_data/transformed_data.csv",
    dag=dag,
)

dowload_data >> unzip_data >> [extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width] >> consolidate_data >> transform_data


