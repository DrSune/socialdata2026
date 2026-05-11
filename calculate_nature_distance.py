import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json

def calculate_distances():
    print("Loading data...")
    # 1. Load geocoded houses
    df = pd.read_csv('geocoded_sample_large.csv')
    df = df[df['status'] == 'success'].copy()
    
    # Create GeoDataFrame for houses
    gdf_houses = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.lon, df.lat),
        crs="EPSG:4326"
    )
    
    # 2. Load nature polygons
    gdf_nature = gpd.read_file('nature_types_small.json')
    if gdf_nature.crs is None:
        gdf_nature.set_crs("EPSG:4326", inplace=True)
    
    # 3. Project to UTM 32N for accurate meter-based distance calculation
    print("Projecting to UTM 32N...")
    gdf_houses = gdf_houses.to_crs("EPSG:25832")
    gdf_nature = gdf_nature.to_crs("EPSG:25832")
    
    # 4. Calculate minimum distance to any nature polygon
    print("Calculating distances (this may take a moment)...")
    def get_min_dist(house_geom):
        # We can speed this up by using sindex.nearest if we had many points,
        # but for 100 points, distance() to the whole series is fine.
        return gdf_nature.distance(house_geom).min()

    gdf_houses['distance_to_nature_m'] = gdf_houses.geometry.apply(get_min_dist)
    
    # 5. Save results
    print("Saving results...")
    # Drop geometry before saving to CSV
    df_out = pd.DataFrame(gdf_houses.drop(columns='geometry'))
    df_out.to_csv('geocoded_with_nature.csv', index=False)
    print("Done. Results saved to geocoded_with_nature.csv")
    print(df_out[['input', 'distance_to_nature_m']].head())

if __name__ == "__main__":
    calculate_distances()
