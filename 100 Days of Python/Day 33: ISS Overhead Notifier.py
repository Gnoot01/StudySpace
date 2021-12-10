import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 1.352083
MY_LONG = 103.819839
email = "pythontestosterone@gmail.com"
password = "-----"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

iss_latitude = float(response.json()["iss_position"]["latitude"])
iss_longitude = float(response.json()["iss_position"]["longitude"])


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
sunrise = int(response.json()["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(response.json()["results"]["sunset"].split("T")[1].split(":")[0])
hour_now = datetime.now().hour

while True:
    time.sleep(60) # check every min                                         # when it's dark
    if abs(MY_LAT-iss_latitude) <= 5 and abs(MY_LONG-iss_longitude) <= 5 and sunset <= hour_now <= sunrise:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs="honourandrespect81@gmail.com",
                msg="Subject:LOOK UP!\n\nISS above ya")



