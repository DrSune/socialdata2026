import requests
import json

DAWA_URL = "https://api.dataforsyningen.dk/adresser"

def test_dawa_adresser():
    address_string = "Lønborgvej 26, 6880 Tarm"
    params = {"q": address_string, "per_side": 1}
    response = requests.get(DAWA_URL, params=params)
    data = response.json()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    test_dawa_adresser()
