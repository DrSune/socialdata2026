import pandas as pd
import numpy as np

def create_final_dataset():
    print("Loading datasets...")
    df_housing = pd.read_parquet('full_housing_data.parquet')
    df_nature = pd.read_csv('geocoded_with_nature.csv')
    
    # Pre-calculate Efficiency Era
    def get_efficiency_era(year):
        if year < 1961: return 'G/F (Pre-Insulation)'
        if year < 1977: return 'E (Minimal)'
        if year < 1995: return 'D (Standard)'
        if year < 2010: return 'C (Modern)'
        return 'B/A (High Efficiency)'

    df_housing['Efficiency_Era'] = df_housing['year_build'].apply(get_efficiency_era)
    
    # Merge on full address
    # We need to recreate the full address in df_housing to match
    df_housing['full_address'] = df_housing['address'] + ", " + df_housing['zip_code'].astype(str) + " " + df_housing['city']
    
    df_merged = pd.merge(df_nature, df_housing, left_on='input', right_on='full_address')
    
    print(f"Merged dataset has {len(df_merged)} records.")
    
    # Calculate Residuals (Price Deviation from City Median)
    # We use the full dataset for medians to be accurate
    city_medians = df_housing.groupby(['city'])['sqm_price'].median().reset_index()
    city_medians.columns = ['city', 'city_median_sqm_price']
    
    df_merged = pd.merge(df_merged, city_medians, on='city')
    df_merged['Price_Deviation_%'] = ((df_merged['sqm_price'] - df_merged['city_median_sqm_price']) / df_merged['city_median_sqm_price']) * 100
    
    # Categorize Nature Proximity
    df_merged['Nature_Proximity'] = pd.cut(df_merged['distance_to_nature_m'], 
                                           bins=[0, 1000, 5000, 10000, 100000], 
                                           labels=['Immediate (<1km)', 'Close (1-5km)', 'Nearby (5-10km)', 'Distant (>10km)'])

    df_merged.to_csv('final_viz_data.csv', index=False)
    print("Final visualization data saved to final_viz_data.csv")
    print(df_merged[['input', 'Efficiency_Era', 'Price_Deviation_%', 'Nature_Proximity']].head())

if __name__ == "__main__":
    create_final_dataset()
