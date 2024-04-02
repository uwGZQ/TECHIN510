import streamlit as st
from datetime import datetime
import pytz
import time

# Function to display world clocks and UNIX timestamp
def display_world_clocks():
    st.title("World Clock")
    cities = st.multiselect('Select Cities', options=pytz.all_timezones, default=['UTC'])
    show_unix_timestamp = st.checkbox("Show UNIX Timestamp", value=True)

    # Display the current UNIX timestamp
    if show_unix_timestamp:
        unix_time = int(time.time())
        st.write(f"Current UNIX Timestamp: {unix_time}")

    # Continuously update and display the time for the selected cities
    while True:
        if cities:
            current_times = {}
            for city in cities:
                current_time = datetime.now(pytz.timezone(city)).strftime('%Y-%m-%d %H:%M:%S')
                current_times[city] = current_time

            for city, current_time in current_times.items():
                st.write(f"{city}: {current_time}")
            
            time.sleep(1)
            st.experimental_rerun()

# Function for UNIX timestamp conversion page
def unix_timestamp_conversion():
    st.title("UNIX Timestamp Conversion")
    
    # Input for UNIX timestamp
    unix_timestamp = st.number_input('Enter UNIX timestamp', value=int(time.time()), step=1)
    
    # Convert UNIX timestamp to human-readable time
    human_time = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    st.write(f"Human-readable time: {human_time}")

# Layout
st.title("Timer App")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ('World Clocks', 'UNIX Timestamp Conversion'))

if page == 'World Clocks':
    display_world_clocks()
elif page == 'UNIX Timestamp Conversion':
    unix_timestamp_conversion()
