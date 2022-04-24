import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
import os
import datetime
import boto3

load_dotenv()

key = os.getenv('APIKEY')

df = pd.read_csv('/Users/guillaumearp/Python_Projects/Kayak_Project/df_complete.csv')
now = datetime.datetime.now()

def get_weather_data(df):

    df_full = df.copy(deep=True)
    df_full.drop(['felt_temperature', 'rain_chances', 'humidity', 'score_weather'], axis=1, inplace=True)
    temps_list = []
    rain_pop = []
    humidity_list = []

    for i in df_full.itertuples():
        lat = i.lat
        lon = i.lon
        r = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={key}").json()
        weather_7_days = r['daily'][1:] 
        temps = [j['feels_like']['day'] for j in weather_7_days]
        rain = [int(j['pop'] * 100) for j in weather_7_days]
        humidity = [j['humidity'] for j in weather_7_days]
        temps_list.append(temps)
        rain_pop.append(rain)
        humidity_list.append(humidity)        

    df_full['felt_temperature'] = temps_list
    df_full['rain_chances'] = rain_pop
    df_full['humidity'] = humidity_list
    df_full['score_weather'] = df_full.apply(lambda x: abs((35 - np.mean(x['felt_temperature'])) * 2) + np.mean(x['rain_chances']) + (np.mean(x['humidity']) / 2), axis=1)
    df_full['updated_at'] = now
    
    return df_full

df_complete = get_weather_data(df)
df_complete.to_csv('/Users/guillaumearp/Python_Projects/Kayak_Project/df_complete.csv', index=False, header=True)

session = boto3.Session()
s3 = boto3.resource('s3')
s3.Bucket('kayak-project-garp').upload_file('/Users/guillaumearp/Python_Projects/Kayak_Project/df_complete.csv', 'df_complete.csv')