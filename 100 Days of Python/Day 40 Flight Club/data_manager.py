import requests

API_KEY = "e72a15a20fe7c8bcf5262a8a2f00ea11"
PRICES_API_ENDPOINT = f"https://api.sheety.co/{API_KEY}/flightDeals/prices"
USERS_API_ENDPOINT = f"https://api.sheety.co/{API_KEY}/flightDeals/users"
HEADERS = {
    "Authorization": "Bearer iks8rthw9neinviu4hv92h59v28y45v9h4toiele"
}

class DataManager:
    #This class is responsible for talking to the Google Sheet via Sheetly
    def __init__(self):
        pass

    def get_prices_data(self):
        response = requests.get(url=PRICES_API_ENDPOINT, headers=HEADERS)
        return response.json()["prices"]

    def save_prices_data(self, data):
        params = {
            "prices": {
                "iataCode": data,
            }
        }
        requests.post(url=PRICES_API_ENDPOINT, json=params, headers=HEADERS)

    def edit_prices_data(self, row_num, data):
        put_api_endpoint = f"https://api.sheety.co/{API_KEY}/flightDeals/prices/{row_num}"
        params = {
            "prices": {
                "iataCode": data,
            }
        }
        requests.put(url=put_api_endpoint, json=params, headers=HEADERS)

    def del_prices_data(self, row_num):
        delete_api_endpoint = f"https://api.sheety.co/{API_KEY}/flightDeals/prices/{row_num}"
        pass

    def get_users_data(self):
        response = requests.get(url=USERS_API_ENDPOINT, headers=HEADERS)
        return response.json()["users"]

    def save_users_data(self, first_name, last_name, email):
        params = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        }
        requests.post(url=USERS_API_ENDPOINT, json=params, headers=HEADERS)
