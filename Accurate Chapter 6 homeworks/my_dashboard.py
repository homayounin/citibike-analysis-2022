import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="NYC Bike Dashboard", layout="wide")

# Title and description
st.title("NYC Citibike and Weather Dashboard")
st.write("""
This dashboard visualizes bike usage patterns and weather trends in New York City. 
Explore interactive charts to uncover insights into the relationship between bike trips and temperature.
""")

# Load datasets
try:
    bike_data = pd.read_csv('merged_citibike_weather.csv', low_memory=False)
    weather_data = pd.read_csv('weather_2022.csv')
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

# Preprocess data
bike_data['started_at'] = pd.to_datetime(bike_data['started_at'], errors='coerce')
bike_data['start_date'] = bike_data['started_at'].dt.date
weather_data['DATE'] = pd.to_datetime(weather_data['DATE'], errors='coerce').dt.date

daily_trips = bike_data.groupby('start_date').size().reset_index(name='Trips')
daily_trips.columns = ['Date', 'Trips']

merged_data = pd.merge(daily_trips, weather_data, left_on='Date', right_on='DATE', how='inner')

# Bar chart for most popular stations
popular_stations = bike_data['start_station_name'].value_counts().head(10).reset_index()
popular_stations.columns = ['Station', 'Trips']
fig1 = px.bar(popular_stations, x='Station', y='Trips', title="Top 10 Most Popular Stations")

# Dual-axis line chart for trips and temperature
fig2 = px.line(merged_data, x='Date', y=['Trips', 'TMAX'], 
               labels={'value': 'Count/Temperature', 'variable': 'Metric'},
               title="Daily Bike Trips vs Maximum Temperature")

# Streamlit interactive layout
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Add Kepler.gl map
st.subheader("NYC Bike Usage Map")
try:
    with open("kepler_map.html", "r") as f:
        st.components.v1.html(f.read(), height=600)
except FileNotFoundError:
    st.error("Kepler.gl map file ('kepler_map.html') not found. Please ensure the file exists.")
