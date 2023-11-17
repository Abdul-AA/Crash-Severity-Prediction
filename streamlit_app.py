import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Function to load data (ensure to replace with your actual data path)
@st.cache
def load_data():
    return pd.read_csv('Crash_Reporting_-_Drivers_Data.csv', parse_dates=['Crash Date/Time'])

df = load_data()

# Sidebar for Filters
st.sidebar.header("Filters")
severity_filter = st.sidebar.selectbox("Select Injury Severity", ['All'] + list(df['Injury Severity'].unique()))
time_granularity = st.sidebar.selectbox("Select Time Granularity", ['Daily', 'Monthly', 'Yearly'])

# Filter data based on severity
if severity_filter != 'All':
    df = df[df['Injury Severity'] == severity_filter]

# Map Visualization
st.header("Accident Locations on Map")
map_fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Injury Severity",
                            hover_data=['Route Type', 'Weather', 'Light'],
                            zoom=10, height=500, mapbox_style="open-street-map")
st.plotly_chart(map_fig)

# Time Trend Analysis
st.header("Time Trend Analysis of Accidents")
# Resampling data based on selected time granularity
if time_granularity == 'Daily':
    trend_data = df['Crash Date/Time'].dt.date.value_counts().sort_index()
elif time_granularity == 'Monthly':
    trend_data = df['Crash Date/Time'].dt.to_period('M').value_counts().sort_index()
elif time_granularity == 'Yearly':
    trend_data = df['Crash Date/Time'].dt.to_period('Y').value_counts().sort_index()

trend_fig = px.line(x=trend_data.index, y=trend_data.values, labels={'x': time_granularity, 'y': 'Number of Accidents'})
st.plotly_chart(trend_fig)

# Weather Conditions Analysis
st.header("Accidents by Weather Conditions")
weather_fig = px.bar(df, x='Weather', title='Number of Accidents by Weather Conditions')
st.plotly_chart(weather_fig)

# Types of Accidents Analysis
st.header("Types of Accidents Analysis")
collision_type_fig = px.pie(df, names='Injury Severity', title='Proportion of Accident Injury Severity Levels')
st.plotly_chart(collision_type_fig)

# Additional Insights (Optional)
# ...

# Ensure to replace '/path/to/your/data.csv' with the actual path to your dataset.
