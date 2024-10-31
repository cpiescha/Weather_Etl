
import requests
from datetime import datetime
import json
import pandas as pd
import os

def send_text(bot_message):                                        #funcion que envia mensajes al chatbot de telegram
    bot_token = '7706822133:AAFDfID_VjRuyE5DAdlwPwneAEv2GZG7VtQ'
    chat_ID = '6823995584'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_ID + '&parse_mode=Markdown&text=' + bot_message

    res = requests.post(send_text)
    return res

def extract_weather_data():
    
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
        if not os.path.isfile("C:/Users/USUARIO/Desktop/weather_etl/plugins/tmp/weather_data.tsv"):
            df.to_csv("C:/Users/USUARIO/Desktop/weather_etl/plugins/tmp/weather_data.tsv", sep='\t', index=False, mode='w')
        else:
            df.to_csv("C:/Users/USUARIO/Desktop/weather_etl/plugins/tmp/weather_data.tsv", sep='\t', index=False, mode='a', header=False)
            

        
        send_text(f"Informacion meteorologica \n ciudad: {weather_info['ciudad']} \n temperatura: {weather_info['temp']} °C \n Temperatura minima: {weather_info['temp_min']} °C \n Temperatura maxima: {weather_info['temp_max']} °C \n Presion: {weather_info['pressure']} hPa \n  humedad: {weather_info['humidity']} % \n fecha y hora: {weather_info['timestamp']}")
                    
    else:
        print(f"Error: {response.status_code}")


extract_weather_data()