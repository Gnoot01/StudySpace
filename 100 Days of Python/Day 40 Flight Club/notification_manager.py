import smtplib
from twilio.rest import Client
from flight_data import FlightData

# TWILIO_ACC_SID = os.environ.get(TWILIO_ACC_SID)
# TWILIO_API_KEY = os.environ.get(TWILIO_API_KEY)

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details via Twilio or email
    # SMS eg:                price, departure city-departure airport IATA code, destination city-destination airport IATA code, from ... to ...
    """Low price alert! Only $41 to fly from London-STN to Berlin-SXF, from 2020-08-25 to 2020-09-10."""
    def __init__(self):
        # self.client = Client(TWILIO_ACC_SID, TWILIO_API_KEY)
        pass

    def notify(self, msg, email):
        # message = self.client.messages.create(
        #     body=f'\nLow price alert! Only ${price} to fly from {departure_city}-{departure_airport} to {destination_city}-{destination_airport}, from {depart_date} to {return_date}.',
        #     from_='+15304894584',
        #     to='...(must be verified in account first!)...'
        # )
        my_email = "pythontestosterone@gmail.com"
        PASSWORD = "thisisalongpassword~!@_+"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=PASSWORD)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=email,
                msg=msg)

