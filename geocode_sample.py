import requests
import concurrent.futures
import pandas as pd
import time

DAWA_URL = "https://api.dataforsyningen.dk/adresser"

def geocode_address(address_string):
    params = {"q": address_string, "per_side": 1}
    try:
        response = requests.get(DAWA_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            best_match = data[0]
            coords = best_match.get("adgangsadresse", {}).get("adgangspunkt", {}).get("koordinater", [])
            if len(coords) == 2:
                return {
                    "input": address_string,
                    "lon": coords[0],
                    "lat": coords[1],
                    "status": "success"
                }
    except Exception as e:
        return {"input": address_string, "status": f"error: {str(e)}"}
    return {"input": address_string, "status": "not_found"}

if __name__ == "__main__":
    df = pd.read_csv('sample_addresses_large.csv')
    addresses = df['full_address'].tolist()
    
    print(f"Geocoding {len(addresses)} addresses...")
    results = []
    # Increased workers for the larger sample
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_address = {executor.submit(geocode_address, addr): addr for addr in addresses}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_address)):
            results.append(future.result())
            if i % 50 == 0:
                print(f"Progress: {i}/{len(addresses)}")
            
    df_results = pd.DataFrame(results)
    df_results.to_csv('geocoded_sample_large.csv', index=False)
    print("Done. Sample results:")
    print(df_results.head())
