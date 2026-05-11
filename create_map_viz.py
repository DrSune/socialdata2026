import pandas as pd
import folium
from folium.plugins import HeatMap

# Load recent data
df = pd.read_csv('solutions/recent.csv')

# Clean and filter
df['Category'] = df['Incident Category'].str.upper().str.replace('/', ' ')
crime_map = {'DRUG NARCOTIC': 'DRUG OFFENSE'}
df['Category'] = df['Category'].replace(crime_map)

# Filter for Drug Offenses
drugs = df[df['Category'] == 'DRUG OFFENSE'].dropna(subset=['Latitude', 'Longitude'])

# Create Map centered on SF
m = folium.Map(location=[37.7749, -122.4194], zoom_start=13, tiles='CartoDB positron')

# Add HeatMap
heat_data = [[row['Latitude'], row['Longitude']] for index, row in drugs.iterrows()]
HeatMap(heat_data, radius=10, blur=15, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)

# Add a marker for the Tenderloin to guide the reader
folium.Marker(
    location=[37.7842, -122.4140],
    popup='Tenderloin: Central Hub of Drug Enforcement',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Save
m.save('docs/drug_heatmap.html')
print("Map saved to docs/drug_heatmap.html")
