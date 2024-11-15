import streamlit as st
import pandas as pd
import plotly.express as px

# Title and Description
st.set_page_config(page_title="NYC Bike Dashboard", layout="wide")
st.title("NYC Citibike and Weather Dashboard")
st.write("This dashboard visualizes bike usage patterns and weather data.")

# Load data
bike_data = pd.read_csv('merged_citibike_weather.csv', low_memory=False)
weather_data = pd.read_csv('weather_2022.csv')

# Fix 'started_at' column with error handling
# Use errors='coerce' to handle invalid datetime entries
bike_data['started_at'] = pd.to_datetime(bike_data['started_at'], errors='coerce')

# Drop rows with invalid dates
bike_data.dropna(subset=['started_at'], inplace=True)

# Convert 'started_at' to date only (ignoring time)
bike_data['start_date'] = bike_data['started_at'].dt.date

# Convert 'DATE' column in weather data to date format
weather_data['DATE'] = pd.to_datetime(weather_data['DATE'], errors='coerce').dt.date

# Aggregate bike trips by day
daily_trips = bike_data.groupby('start_date').size().reset_index(name='Trips')
daily_trips.columns = ['Date', 'Trips']

# Merge with weather data
merged_data = pd.merge(daily_trips, weather_data, left_on='Date', right_on='DATE')

# Popular Stations Bar Chart
popular_stations = bike_data['start_station_name'].value_counts().head(10).reset_index()
popular_stations.columns = ['Station', 'Trips']
fig1 = px.bar(popular_stations, x='Station', y='Trips', title="Top 10 Most Popular Stations")

# Daily Trips and Temperature Chart
fig2 = px.line(merged_data, x='Date', y=['Trips', 'TMAX'], 
               labels={'value': 'Count/Temperature', 'variable': 'Metric'}, 
               title="Daily Bike Trips vs Maximum Temperature")

# Display Charts
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
