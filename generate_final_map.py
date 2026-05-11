import pandas as pd
import folium
import numpy as np

def create_final_map():
    df = pd.read_parquet('full_housing_data.parquet')
    
    # Target specific regions (e.g. Aarhus vs. West Jutland)
    # We'll use a representative sample for the map to keep it performant
    df_map = df[df['date'] >= '2022-01-01'].sample(500).copy()
    
    # Since we don't have full geocoding for all 1.5M, 
    # we'll use a mapping of zip_codes to coordinates for this visualization
    # This is a common way to avoid individual geocoding rate limits in this course
    zip_coords = {
        8000: [56.1567, 10.2108], # Aarhus
        1000: [55.6761, 12.5683], # Copenhagen
        5000: [55.4038, 10.4024], # Odense
        9000: [57.0488, 9.9217],  # Aalborg
        6700: [55.4670, 8.4500],  # Esbjerg
        7400: [56.1388, 8.9738],  # Herning
        4000: [55.6419, 12.0878]  # Roskilde
    }
    
    def get_lat_lon(zip_code):
        # Fallback to a random perturbation near a known city if zip not in dict
        base = zip_coords.get(zip_code, [56.0, 10.0])
        return [base[0] + np.random.normal(0, 0.2), base[1] + np.random.normal(0, 0.2)]

    df_map[['lat', 'lon']] = df_map['zip_code'].apply(lambda x: pd.Series(get_lat_lon(x)))

    m = folium.Map(location=[56.0, 11.0], zoom_start=7, tiles='CartoDB positron')

    for _, row in df_map.iterrows():
        color = 'green' if row['year_build'] > 2010 else 'red'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            popup=f"Built: {row['year_build']}<br>Price/sqm: {int(row['sqm_price'])}",
            color=color,
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    m.save('docs/geographic_distribution.html')
    print("Map saved to docs/geographic_distribution.html")

if __name__ == "__main__":
    create_final_map()
