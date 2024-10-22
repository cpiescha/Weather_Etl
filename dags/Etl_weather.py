from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
import requests
import json
from datetime import datetime
import os
import pandas as pd
#defining DAG arguments
# You can override them on a per-task basis during operator initialization
def send_text(bot_message):                                        #funcion que envia mensajes al chatbot de telegram
    bot_token = '7706822133:AAFDfID_VjRuyE5DAdlwPwneAEv2GZG7VtQ'
    chat_ID = '6823995584'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_ID + '&parse_mode=Markdown&text=' + bot_message

    res = requests.post(send_text)
    return res


def task_1():
    
    lat=6.25184
    lon=-75.56359
    API_key='cc86cf368327ae7b03bff8ac2ddae208'
    
    response= requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric')
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
    # Convertir la respuesta en formato JSON
        response=response.text
        response=json.loads(response)
        print(response)
        data=response["main"]

        weather_info = {
            'ciudad': response['name'],
            'temp':data['temp'],
            'temp_min': data['temp_min'],
            'temp_max': data['temp_max'],
            'pressure': data['pressure'],
            'humidity': data['humidity'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        df = pd.DataFrame([weather_info])
        if not os.path.isfile('weather_data.tsv'):
            df.to_csv('weather_data.tsv', sep='\t', index=False, mode='w')
        else:
            df.to_csv('weather_data.tsv', sep='\t', index=False, mode='a', header=False)
        
        send_text(f'Informacion meteorologica \n ciudad: {weather_info['ciudad']} \n temperatura: {weather_info['temp']} °C \n Temperatura minima: {weather_info['temp_min']} °C \n Temperatura maxima: {weather_info['temp_max']} °C \n Presion {weather_info['pressure']} hPa \n  humedad: {weather_info['humidity']} % \n fecha y hora: {weather_info['timestamp']}')
        # file_exists = os.path.isfile('weather_data.tsv')
        # with open('weather_data.tsv', mode='a', newline='') as file:
        #     writer = csv.DictWriter(file, fieldnames=['ciudad', 'temp','temp_min','temp_max','pressure','humidity', 'timestamp'], delimiter='\t')

        #     if not file_exists:
        #         writer.writeheader()  # Escribe la cabecera si el archivo no existe

        #     writer.writerow(weather_info)
                    
    else:
        print(f"Error: {response.status_code}")


task_1()
    

    
    
# default_args = {
#     'owner': 'milo',
#     'start_date': days_ago(0),
#     'email': ['milo0@gmail.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }
# # defining the DAG
# # define the DAG
# dag = DAG(
#     dag_id='etl_dag',
#     default_args=default_args,
#     description='etl process',
#     schedule_interval=timedelta(days=1),
# )

# Extract_data = PythonOperator(
#      task_id='download_dataset',
#     python_callable=extract_data_from_api,
#     dag=dag
# )

# create_table = PostgresOperator(
#         task_id='create_table',
#         postgres_conn_id='postgres_default',
#         sql="""
#         CREATE TABLE IF NOT EXISTS weather_medellin (
#             city VARCHAR(255),
#             temp FLOAT,
#             temp_min FLOAT,
#             temp_max FLOAT,
#             pressure INT,
#             humidity INT,
#             timestamp DATE
#         );
#         """
#     )
