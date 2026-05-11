import pandas as pd
import folium
import numpy as np

def create_hex_choropleth():
    print("Loading data for Hex Choropleth...")
    df = pd.read_csv('final_viz_data.csv')
    
    # We'll create a Folium map with multiple layers to show "Interconnectedness"
    m = folium.Map(location=[56.0, 11.0], zoom_start=7, tiles='CartoDB positron')
    
    # Layer 1: Energy Labels (The Macro)
    # Since we can't easily do hexbins in pure Folium without extra libraries, 
    # we'll use CircleMarkers with radius scaled by price deviation to show "Stress"
    
    fg_penalty = folium.FeatureGroup(name="Crisis Price Penalty (G-E Eras)")
    
    legacy = df[df['Efficiency_Era'].isin(['G/F (Pre-Insulation)', 'E (Minimal)', 'D (Standard)'])].copy()
    
    for _, row in legacy.iterrows():
        # Redder/Larger means bigger price drop
        color = 'red' if row['Price_Deviation_%'] < 0 else 'green'
        radius = abs(row['Price_Deviation_%']) / 5 + 2
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=min(radius, 15),
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"Era: {row['Efficiency_Era']}<br>Premium: {row['Price_Deviation_%']:.1f}%<br>Nature Dist: {int(row['distance_to_nature_m'])}m"
        ).add_to(fg_penalty)
        
    fg_penalty.add_to(m)
    
    # Layer 2: Nature "Buffer" Zones
    # We'll add a subset of nature points/markers to show spatial correlation
    fg_nature = folium.FeatureGroup(name="Resilient Nature Clusters", show=False)
    
    # Focus on "Outliers" (Legacy era but selling high near nature)
    outliers = legacy[(legacy['Price_Deviation_%'] > 0) & (legacy['distance_to_nature_m'] < 2000)]
    
    for _, row in outliers.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            icon=folium.Icon(color='green', icon='leaf'),
            popup=f"<b>Resilient Asset</b><br>Era: {row['Efficiency_Era']}<br>Premium: +{row['Price_Deviation_%']:.1f}%"
        ).add_to(fg_nature)
        
    fg_nature.add_to(m)
    
    folium.LayerControl().add_to(m)
    
    m.save('docs/geographic_distribution.html')
    print("Advanced Folium Map saved.")

if __name__ == "__main__":
    create_hex_choropleth()
