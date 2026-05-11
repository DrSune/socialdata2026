import requests
import pandas as pd
import time

DAWA_URL = "https://api.dataforsyningen.dk/datavask/adresser"

def geocode_address(address_string):
    params = {"betegnelse": address_string}
    try:
        response = requests.get(DAWA_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("resultater"):
            best_match = data["resultater"][0]
            # DAWA 'datavask' returns 'adresse' field with lat/lon in 'adgangsadresse'
            # Let's check the structure carefully
            addr = best_match.get("adresse", {})
            return {
                "input": address_string,
                "lat": addr.get("y"),
                "lon": addr.get("x"),
                "status": "success"
            }
    except Exception as e:
        return {"input": address_string, "status": f"error: {str(e)}"}
    return {"input": address_string, "status": "not_found"}

if __name__ == "__main__":
    # Test with 5 addresses first
    test_addresses = [
        "Lønborgvej 26, 6880 Tarm",
        "Smalle Vorkvej 16, 6040 Egtved",
        "Skulpturvej 10, 4293 Dianalund",
        "Hedetoften 79, 7800 Skive",
        "Nordrevej 26A, 8700 Horsens"
    ]
    
    results = []
    for addr in test_addresses:
        print(f"Geocoding: {addr}")
        res = geocode_address(addr)
        print(f"Result: {res}")
        results.append(res)
        time.sleep(0.5)
            
    df_results = pd.DataFrame(results)
    print("\nTest Results:")
    print(df_results)
