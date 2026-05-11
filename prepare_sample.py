import pandas as pd

def prepare_sample():
    df = pd.read_parquet('full_housing_data.parquet')
    # Focus on recent sales to show the "Crisis" effect
    df_recent = df[df['date'] >= '2022-01-01'].copy()
    
    # Take a sample of 500 (good balance of signal and geocoding time)
    df_sample = df_recent.sample(500, random_state=42)
    
    # Create full address for geocoding
    df_sample['full_address'] = df_sample['address'] + ", " + df_sample['zip_code'].astype(str) + " " + df_sample['city']
    
    df_sample[['full_address']].to_csv('sample_addresses_large.csv', index=False)
    print(f"Sample of {len(df_sample)} addresses saved to sample_addresses_large.csv")

if __name__ == "__main__":
    prepare_sample()
