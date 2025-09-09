import requests

url = "https://countriesnow.space/api/v0.1/countries/states"
data = {"country": "Pakistan"}
response = requests.post(url, json=data)
if response.status_code == 200:
    states = response.json()
    print(f"states: {states["data"]["states"]}")
    print([state["name"] for state in states["data"]["states"]])
else:
    print("Failed to fetch states:", response.status_code)
