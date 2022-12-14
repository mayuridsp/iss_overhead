import requests
from datetime import datetime
import smtplib
import time
import os

MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')

MY_LAT = float(input("What's your latitude?\nE.g.: 41.232861\n"))
MY_LONG = float(input("What's your longitude?\nE.g.: -8.621570\n"))
EMAIL_ADDRESS = input("What's your e-mail address?\n E.g.: maydsp1993@gmail.com\n")


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.mail.yahoo.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=EMAIL_ADDRESS,
            msg=f"Subject:Look up!\n\nLook up, the ISS is above you in the sky."
        )
    connection = smtplib.SMTP("smtp.mail.yahoo.com")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=EMAIL_ADDRESS,
        msg=f"Subject:No luck...\n\nThe ISS is not over your head."
    )
