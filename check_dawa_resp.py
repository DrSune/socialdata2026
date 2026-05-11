import requests
import json

DAWA_URL = "https://api.dataforsyningen.dk/datavask/adresser"

def test_dawa():
    address_string = "Lønborgvej 26, 6880 Tarm"
    params = {"betegnelse": address_string}
    response = requests.get(DAWA_URL, params=params)
    data = response.json()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    test_dawa()
