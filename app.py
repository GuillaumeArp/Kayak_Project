import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import os
import datetime

st.set_page_config(page_title='Kayak', page_icon=':sunny:', layout='wide')

st.markdown("<h1 style='text-align: center;'>Kayak Project</h1>", unsafe_allow_html=True)

key = os.getenv('APIKEY')
mapbox_token = os.getenv('MAPBOX_TOKEN')

def load_data():
    'Loading data...'
    return pd.read_csv('df_complete.csv')

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
    
    return df_full

def hotel_data(df):

    df_hotels = df[['id', 'city', 'name', 'url', 'lat_hotels', 'lon_hotels', 'description', 'score', 'score_weather']]
    df_hotels_final = pd.DataFrame()
    df_hotels_final[['id', 'city', 'score_weather']] = df_hotels[['id', 'city', 'score_weather']]
    df_hotels_final['name'] = df_hotels['name'].apply(eval)
    df_hotels_final['url'] = df_hotels['url'].apply(eval)
    df_hotels_final['lat_hotels'] = df_hotels['lat_hotels'].apply(eval)
    df_hotels_final['lon_hotels'] = df_hotels['lon_hotels'].apply(eval)
    df_hotels_final['description'] = df_hotels['description'].apply(eval)
    df_hotels_final['score'] = df_hotels['score'].apply(eval)
    
    df_hotels_full = df_hotels_final.sort_values('score_weather')
    df_hotels_full.reset_index(inplace=True, drop=True)
    df_hotels_full = df_hotels_full.apply(pd.Series.explode)
    df_hotels_full['description'] = df_hotels_full['description'].replace("\\n", "", regex=True)
    df_hotels_full['score'] = df_hotels_full['score'].replace(",", ".", regex=True)
    df_hotels_full[['lat_hotels', 'lon_hotels', 'score']] = df_hotels_full[['lat_hotels', 'lon_hotels', 'score']].apply(pd.to_numeric)

    return df_hotels_full

def weather_data(df):

    df_weather = df[['id', 'city', 'lat', 'lon', 'day_plus', 'felt_temperature', 'rain_chances', 'humidity', 'score_weather']]
    df_weather_final = pd.DataFrame()
    df_weather_final[['id', 'city', 'lat', 'lon', 'felt_temperature', 'rain_chances', 'humidity', 'score_weather']] = df_weather[['id', 'city', 'lat', 'lon', 'felt_temperature', 'rain_chances', 'humidity', 'score_weather']]
    df_weather_final['day_plus'] = df_weather['day_plus'].apply(eval)
    df_weather_final[['lat', 'lon']] = df_weather[['lat', 'lon']].apply(pd.to_numeric)

    df_weather_full = df_weather_final.sort_values('score_weather')
    df_weather_full.reset_index(inplace=True, drop=True)
    df_weather_full = df_weather_full.apply(pd.Series.explode)
    df_weather_full[['day_plus', 'felt_temperature', 'rain_chances', 'humidity']] = df_weather_full[['day_plus', 'felt_temperature', 'rain_chances', 'humidity']].apply(pd.to_numeric)
    df_weather_full['inverted_score'] = max(df_weather_full['score_weather']) - df_weather_full['score_weather']
    
    return df_weather_full

df_s3 = load_data()
df = get_weather_data(df_s3)
df_weather_full = weather_data(df)
df_hotels_full = hotel_data(df)

now_1 = datetime.datetime.now()
now_string_1 = now_1.strftime("%d/%m/%Y %H:%M:%S")

with st.sidebar:
    'Click here to refresh the data from OpenWeather (please once per hour maximum).'
    if st.button('Refresh Weather Data'):
        now_2 = datetime.datetime.now()
        df_s3 = load_data()
        df = get_weather_data(df_s3)
        df_weather_full = weather_data(df)
        df_hotels_full = hotel_data(df)
        now_1 = now_2
        now_string_1 = now_1.strftime("%d/%m/%Y %H:%M:%S")
        st.write('Last refresh:', now_string_1)
    else:
        st.write('Last refresh:', now_string_1)

st.write('This page shows the two plots required as deliverables for the Kayak Project, as part of the Jedha Bootcamp Fullstack training.')
st.markdown('The repository of this project can be found [on this page](https://github.com/GuillaumeArp/Kayak_Project).')

def plot_weather():
    px.set_mapbox_access_token(mapbox_token)

    fig = px.scatter_mapbox(
        df_weather_full[:35],
        lat='lat',
        lon='lon',
        color='felt_temperature',
        size='inverted_score',
        color_continuous_scale=px.colors.sequential.Bluered,
        size_max=35,
        zoom=5,
        range_color = [min(df_weather_full[:35]['felt_temperature']), max(df_weather_full[:35]['felt_temperature'])],
        hover_name='city',
        hover_data={
            'lat': False,
            'lon': False,
            'day_plus': False,
            'rain_chances': True,
            'humidity': True,
            'felt_temperature': True,
            'inverted_score': False,
            },
        animation_frame='day_plus',
        labels={'felt_temperature': 'Felt Temperature', 'rain_chances': 'Rain Chances', 'humidity': 'Humidity'}
    )

    fig.update_layout(
        width = 1300,
        height = 950,
        template='plotly_dark',
        title_x=0.5,
        title_text='The 5 cities with the best weather over the next 7 days')
    
    return fig

def plot_hotels():
    px.set_mapbox_access_token(mapbox_token)

    fig = px.scatter_mapbox(
        df_hotels_full[:100],
        lat='lat_hotels',
        lon='lon_hotels',
        color='score',
        color_continuous_scale=px.colors.diverging.RdYlGn,
        size='score',
        size_max=25,
        zoom=5,
        range_color = [min(df_hotels_full[:100]['score']), max(df_hotels_full[:100]['score'])],
        hover_name='name',
        hover_data={
            'lat_hotels': False,
            'lon_hotels': False,
            'name': False,
            'city': True,
            'url': False,
            'description': False,
            'score_weather': False,
            'id': False,
            },
        labels={'score': 'Score', 'name': 'Hotel Name'}
    )

    fig.update_layout(
        width = 1300,
        height = 950,
        template='plotly_dark',
        title_x=0.5,
        title_text='20 best hotels from the 5 cities with the best weather')
    
    return fig


st.plotly_chart(plot_weather(), use_container_width=True)
st.write(' ')
st.plotly_chart(plot_hotels(), use_container_width=True)
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write('Made by Guillaume Arp.')
