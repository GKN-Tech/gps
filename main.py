import streamlit as st
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import requests
import ipinfo

# Access the environment variables
access_token = st.secrets["ACCESS_TOKEN"]
# This access token is issued on my personal email, max. 50,000 reqs/month

# Function to create a map and add markers
def create_map(user_location, library_location):
    map_center = [(user_location[0] + library_location[0]) / 2, (user_location[1] + library_location[1]) / 2]
    m = folium.Map(location=map_center, zoom_start=13)
    
    # Add user marker
    folium.Marker(
        location=user_location,
        popup="You are here",
        icon=folium.Icon(color="blue")
    ).add_to(m)
    
    # Add library marker
    folium.Marker(
        location=library_location,
        popup="KPU Surrey Library",
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    # Adjust zoom level to fit both markers
    m.fit_bounds([user_location, library_location])
    
    return m

# Retreiving the IP address of user and then location data from IP add. using two APIs ipify and ipinfo
def get_ip(): 
    try:
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]
    except Exception as e:
        st.error(f"Error retrieving ip address: {e}")
        return None

def get_user_location(): 
    try:
        ip_address = get_ip()
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip_address)
        loc = details.loc.split(',')
        latitude = float(loc[0])
        longitude = float(loc[1])
        return (latitude, longitude)
    except Exception as e:
        st.error(f"Error retrieving location: {e}")
        return None

# Streamlit app
st.title("Find Your Distance to the KPU Library")

# Hardcoding fields for KPU Library location from Google Maps
library_location = (49.13219049263347, -122.87144344764631)

# Get user's location
user_location = get_user_location()

# Display the map and distance if user location is available
if user_location:
    # Calculate distance
    distance = geodesic(user_location, library_location).kilometers
    st.write(f"Distance to KPU library: {distance:.2f} km")
    
    # Create and display map
    m = create_map(user_location, library_location)
    st_folium(m, width=700, height=500)
else:
    st.write("Could not retrieve user location.")

