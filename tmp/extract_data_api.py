
import requests
from datetime import datetime
import json
import pandas as pd
import os
import pytz
from dotenv import load_dotenv

load_dotenv()

def send_text(bot_message):                                        #funcion que envia mensajes al chatbot de telegram
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_ID = os.getenv('TELEGRAM_CHAT_ID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_ID + '&parse_mode=Markdown&text=' + bot_message

    res = requests.post(send_text)
    return res

def extract_weather_data():
    
    lat = 6.25184
    lon = -75.56359
    API_key = os.getenv('WEATHER_API_KEY')
    bogota_tz = pytz.timezone('America/Bogota')
    
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
            'temp':float(data['temp']),
            'temp_min': data['temp_min'],
            'temp_max': data['temp_max'],
            'pressure': data['pressure'],
            'humidity': data['humidity'],
            'timestamp': datetime.now(bogota_tz).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        df = pd.DataFrame([weather_info])
        
        
        if not os.path.isfile('/opt/airflow/tmp/weather_data.tsv'):
            df.to_csv("/opt/airflow/tmp/weather_data.tsv", sep='\t', index=False,header=False, mode='w')
        else:
            df.to_csv("/opt/airflow/tmp/weather_data.tsv", sep='\t', index=False, mode='a', header=False)
            

        #enviar mensaje a telegram
        send_text(f"Informacion meteorologica \n ciudad: {weather_info['ciudad']} \n temperatura: {weather_info['temp']} °C \n Temperatura minima: {weather_info['temp_min']} °C \n Temperatura maxima: {weather_info['temp_max']} °C \n Presion: {weather_info['pressure']} hPa \n  humedad: {weather_info['humidity']} % \n fecha y hora: {weather_info['timestamp']}")
                    
    else:
        print(f"Error: {response.status_code}")


extract_weather_data()