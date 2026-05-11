import pandas as pd
import json

# 1. Housing Data
try:
    df_housing = pd.read_parquet('housing_data.parquet')
    print("### Housing Data Summary ###")
    print(df_housing.info())
    print("\nColumns:", df_housing.columns.tolist())
    
    # Search for coordinates or energy label clues in values
    print("\nSample values for 'address':", df_housing['address'].head(3).tolist())
    print("Sample values for 'house_type':", df_housing['house_type'].unique().tolist())
    
except Exception as e:
    print("Error reading parquet:", e)

# 2. Nature Data
try:
    with open('nature_types_small.json', 'r', encoding='utf-8') as f:
        nature_geojson = json.load(f)
    print("\n### Nature GeoJSON Sample ###")
    print("Feature count:", len(nature_geojson['features']))
    if len(nature_geojson['features']) > 0:
        feat = nature_geojson['features'][0]
        print("Properties:", feat['properties'].keys())
        print("Natyp_navn (Type):", feat['properties'].get('Natyp_navn'))
        print("Geometry type:", feat['geometry']['type'])
except Exception as e:
    print("Error reading GeoJSON:", e)
