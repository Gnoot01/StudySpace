import datetime
import requests
import os

NUTRITIONIX_ID = os.environ.get("NUTRITIONIX_ID")
NUTRITIONIX_KEY = os.environ.get("NUTRITIONIX_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_KEY = os.environ.get("SHEETY_KEY")
GENDER = "male"
WEIGHT_KG = 61.3
HEIGHT_CM = 182.3
AGE = 19
TIME_NOW = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

"""Getting exercise info"""
exercises = input("Which exercises did you do today?: ")
NUTRITIONIX_PARAMS = {
    "query": exercises,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}
NUTRITIONIX_HEADERS = {
    "x-app-id": NUTRITIONIX_ID,
    "x-app-key": NUTRITIONIX_KEY,
}

response = requests.post(url=NUTRITIONIX_ENDPOINT, json=NUTRITIONIX_PARAMS, headers=NUTRITIONIX_HEADERS)
exercises = response.json()["exercises"]

"""Creating new posts to google sheet"""
for exercise in exercises:
    exercise_name = exercise["name"].title()
    exercise_duration = exercise["duration_min"]
    exercise_calories = exercise["nf_calories"]
    SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_KEY}/myWorkouts/sheet1"
    SHEETY_PARAMS = {
        "sheet1": {
            "date": TIME_NOW.split(" ")[0],
            "time": TIME_NOW.split(" ")[1],
            "exercise": exercise_name,
            "duration": exercise_duration,
            "calories": exercise_calories,
        }
    }
    SHEETY_HEADERS = {
        "Authorization": f"Bearer {os.environ.get('SHEETY_TOKEN')}"
    }
    response = requests.post(url=SHEETY_ENDPOINT, json=SHEETY_PARAMS, headers=SHEETY_HEADERS)
    print(response.json())

"""Editing posts on google sheet"""
# row_num = "7"
# SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_KEY}/myWorkouts/sheet1/{row_num}"
# SHEETY_PARAMS = {
#     "sheet1": {
#         "date": TIME_NOW.split(" ")[0],
#         "time": TIME_NOW.split(" ")[1],
#         "exercise": exercises[0]["name"].title(),
#         "duration": exercises[0]["duration_min"],
#         "calories": exercises[0]["nf_calories"],
#     }
# }
# response = requests.put(url=SHEETY_ENDPOINT, json=SHEETY_PARAMS, headers=SHEETY_HEADERS)
# print(response.text)

"""Deleting posts on google sheet"""
# row_num = "3"
# SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_KEY}/myWorkouts/sheet1/{row_num}"
# response = requests.delete(url=SHEETY_ENDPOINT, headers=SHEETY_HEADERS)
# print(response.text)

