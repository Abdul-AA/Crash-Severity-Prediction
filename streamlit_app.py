import streamlit as st
import pandas as pd
import plotly.express as px


# Function to load data (ensure to replace with your actual data path)
@st.cache
def load_data():
    return pd.read_csv('Crash_Reporting_-_Drivers_Data.csv', parse_dates=['Crash Date/Time'])

df = load_data()

# Sidebar for Filters
st.sidebar.header("Filters")
severity_filter = st.sidebar.selectbox("Select Injury Severity", ['All'] + list(df['Injury Severity'].unique()))


# Filter data based on severity
if severity_filter != 'All':
    df = df[df['Injury Severity'] == severity_filter]

# Map Visualization
st.header("Accident Locations on Map")
map_fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Injury Severity",
                            hover_data=['Route Type', 'Weather', 'Light'],
                            zoom=10, height=500, mapbox_style="open-street-map")
st.plotly_chart(map_fig)




# Additional Insights (Optional)
# ...

# Ensure to replace '/path/to/your/data.csv' with the actual path to your dataset.
