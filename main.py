from datetime import datetime
import requests
import os


APP_ID = os.environ["ENV_APP_ID"]
API_KEY = os.environ["ENV_API_KEY"]

GENDER = "male"
WEIGHT_KG = "60"
HEIGHT_CM = "163"
AGE = "32"

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]
exercise_text = input("What exercise did you do? ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=nutritionix_endpoint, json=parameters, headers=headers)
result = response.json()


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")


for entry in result["exercises"]:
    sheety_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": entry["name"].title(),
            "duration": entry["duration_min"],
            "calories": entry["nf_calories"]
        }

    }

    bearer_auth = {
        "Authorization": f"Bearer {os.environ['ENV_AUTH']}",
    }
    response = requests.post(
        url=sheety_endpoint,
        json=sheety_input,
        headers=bearer_auth
    )