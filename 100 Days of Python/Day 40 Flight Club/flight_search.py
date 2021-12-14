import requests
from flight_data import FlightData
import datetime

API_KEY = "N-0YJK85InyMp-B5uSFR7JhR2NCQrmVS"
HEADERS = {
    "apikey": API_KEY,
}
FLY_FROM = "SIN"
CURR = "SGD"
FLIGHT_TYPE = "round"
MIN_LENGTH_STAY = 7
MAX_LENGTH_STAY = 28
DATE_FROM = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
DATE_TO = (datetime.datetime.now() + datetime.timedelta(days=180)).strftime("%d/%m/%Y")

class FlightSearch:
    # This class is responsible for talking to the Flight Search API via Tequila, kiwi.com
    def __init__(self):
        pass

    def get_IATA_code(self, city):
        api_endpoint = "https://tequila-api.kiwi.com/locations/query"
        params = {
            "term": city,
            "location_types": "city",
        }
        response = requests.get(url=api_endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()["locations"][0]["code"]

    def search_flight(self, fly_to: str, max_price: int):
        api_endpoint = "https://tequila-api.kiwi.com/v2/search"
        params = {
            "fly_from": FLY_FROM,
            "fly_to": fly_to,
            "date_from": DATE_FROM,
            "date_to": DATE_TO,
            "curr": CURR,
            "flight_type": FLIGHT_TYPE,
            "nights_in_dst_from": MIN_LENGTH_STAY,
            "nights_in_dst_to": MAX_LENGTH_STAY,
            "one_for_city": 1,
            "max_stopovers": 0,
            "price_to": max_price,
            # "adults" 4             5 Need to update lowest price in google sheets accordingly
        }
        response = requests.get(url=api_endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        try:
            data = response.json()["data"][0] # If doesn't exist, gives []
        except IndexError:
            print(f"No flight cheaper than {max_price} for {fly_to} with {params['max_stopovers']} stopovers found, sorry!")
            params["max_stopovers"] = 1
            response = requests.get(url=api_endpoint, params=params, headers=HEADERS)
            response.raise_for_status()
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"No flight cheaper than {max_price} for {fly_to} with {params['max_stopovers']} stopovers found, sorry!")
            else:
                # will depart from origin city to interim city to final destination city
                return FlightData(price=data["price"],
                                  departure_city=data["cityFrom"],
                                  departure_airport=data["flyFrom"],
                                  destination_city=data["route"][1]["cityTo"],
                                  destination_airport=data["route"][1]["flyTo"],
                                  depart_date=data["route"][0]["local_departure"].split("T")[0],
                                  return_date=data["route"][1]["local_departure"].split("T")[0],
                                  # put [1] to test that data from API might be wrong, as SIN-TOKYO recorded as stop_over=1,
                                  # hence passes first exception, but doesn't have route[2] or stopovers=1 in data, hence gives IndexError unexpectedly
                                  stop_overs=1, via_city=data["cityTo"])
        else:
            return FlightData(price=data["price"],
                              departure_city=data["cityFrom"],
                              departure_airport=data["flyFrom"],
                              destination_city=data["cityTo"],
                              destination_airport=data["flyTo"],
                              depart_date=data["route"][0]["local_departure"].split("T")[0],
                              return_date=data["route"][1]["local_departure"].split("T")[0])
