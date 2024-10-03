import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load data
@st.cache_data
def load_data():
    df_day = pd.read_csv('https://raw.githubusercontent.com/Leon24k/BicycleData/refs/heads/master/Dashboard/day.csv')
    df_hour = pd.read_csv('https://raw.githubusercontent.com/Leon24k/BicycleData/refs/heads/master/Dashboard/hour.csv')

    # Convert date columns to datetime
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

    # Map season and weathersit
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weathersit_map = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}

    df_day['season'] = df_day['season'].map(season_map)
    df_day['weathersit'] = df_day['weathersit'].map(weathersit_map)
    df_hour['season'] = df_hour['season'].map(season_map)
    df_hour['weathersit'] = df_hour['weathersit'].map(weathersit_map)

    return df_day, df_hour


df_day, df_hour = load_data()

# Sidebar
st.sidebar.header('Date Range Selection')
start_date = st.sidebar.date_input('Start Date', min(df_day['dteday']))
end_date = st.sidebar.date_input('End Date', max(df_day['dteday']))

# Filter data based on date range
mask = (df_day['dteday'].dt.date >= start_date) & (df_day['dteday'].dt.date <= end_date)
df_day_filtered = df_day.loc[mask]
df_hour_filtered = df_hour[df_hour['dteday'].dt.date.between(start_date, end_date)]

# Main page
st.title('Bike Sharing Dashboard')

# Visualization 1: Trend of bike rentals over time
st.subheader('Trend of Bike Rentals Over Time')
fig_trend = px.line(df_day_filtered, x='dteday', y='cnt', title='Daily Bike Rentals')
fig_trend.update_xaxes(title='Date')
fig_trend.update_yaxes(title='Number of Rentals')
st.plotly_chart(fig_trend)

# Visualization 2: Average rentals by season
st.subheader('Average Bike Rentals by Season')
season_avg = df_day_filtered.groupby('season')['cnt'].mean().sort_values(ascending=False)
fig_season = px.bar(x=season_avg.index, y=season_avg.values, labels={'x': 'Season', 'y': 'Average Number of Rentals'})
fig_season.update_layout(title='Average Bike Rentals by Season')
st.plotly_chart(fig_season)

# Visualization 3: Hourly pattern on weekdays vs weekends
st.subheader('Hourly Rental Pattern: Weekdays vs Weekends')
hourly_pattern = df_hour_filtered.groupby(['hr', 'workingday'])['cnt'].mean().unstack()
fig_hourly = go.Figure()
fig_hourly.add_trace(go.Scatter(x=hourly_pattern.index, y=hourly_pattern[0], name='Weekend/Holiday', mode='lines'))
fig_hourly.add_trace(go.Scatter(x=hourly_pattern.index, y=hourly_pattern[1], name='Weekday', mode='lines'))
fig_hourly.update_layout(title='Hourly Rental Pattern: Weekdays vs Weekends',
                         xaxis_title='Hour of Day',
                         yaxis_title='Average Number of Rentals')
st.plotly_chart(fig_hourly)

# Visualization 4: Impact of weather on rentals
st.subheader('Impact of Weather on Bike Rentals')
fig_weather = px.box(df_day_filtered, x='weathersit', y='cnt',
                     labels={'weathersit': 'Weather Situation', 'cnt': 'Number of Rentals'})
fig_weather.update_layout(title='Impact of Weather on Bike Rentals')
st.plotly_chart(fig_weather)

# Visualization 5: Rental distribution by day of week
st.subheader('Rental Distribution by Day of Week')
df_day_filtered['dayofweek'] = df_day_filtered['dteday'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig_weekday = px.box(df_day_filtered, x='dayofweek', y='cnt', category_orders={'dayofweek': day_order},
                     labels={'dayofweek': 'Day of Week', 'cnt': 'Number of Rentals'})
fig_weekday.update_layout(title='Rental Distribution by Day of Week')
st.plotly_chart(fig_weekday)