# Inspiration from https://jacksflightclub.com/
from notification_manager import NotificationManager
from data_manager import DataManager
from flight_search import FlightSearch

flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()
emails = [row["email"] for row in data_manager.get_users_data()]
"""Populating Google Sheet IATA codes wrt city names"""
# iata_codes = [flight_search.get_IATA_code(row["city"]) for row in data_manager.get_prices_data()]
# lowest_prices = [row["lowestPrice"] for row in data_manager.get_prices_data()]
iata_codes = ['PAR', 'BER', 'TYO', 'SYD', 'IST', 'MFM', 'NYC', 'SFO', 'CPT', 'RGN', 'HKG', 'CNX', 'BUQ', 'PNH', 'HIJ', 'PER', 'AMS', 'DPS', 'SEL', 'CAI', 'ATH', 'SZX', 'TPE']
lowest_prices = [700, 710, 550, 450, 850, 450, 700, 825, 800, 450, 246, 220, 1300, 200, 650, 450, 625, 420, 400, 620, 650, 1500, 300]
for i in range(len(iata_codes)): data_manager.edit_prices_data(i+2, iata_codes[i])

"""Checking cheapest flights from tomorrow to 6 months later for all the cities with price lower than lowest price listed in the Google Sheet
    Prices historical lows: https://www.faredetective.com/farehistory/"""
for i in range(len(iata_codes)): deals = [flight_search.search_flight(iata_codes[i], lowest_prices[i])]

"""Sending an SMS to your own number with the Twilio API."""
for deal in deals:
  # if deal is None: continue
    msg = f'Subject:LOW PRICE ALERT!\n\nOnly ${deal.price} to fly from {deal.departure_city}-{deal.departure_airport}' \
          f' to {deal.destination_city}-{deal.destination_airport}, from {deal.depart_date} to {deal.return_date}.'
    if deal.stop_overs == 0: msg += f'\nwww.google.co.uk/flights?hl=en#flt={deal.departure_airport}.{deal.destination_airport}' \
                                    f'.{deal.depart_date}*{deal.destination_airport}.{deal.departure_airport}.{deal.return_date}'
    else: msg += f'\n Flight has {deal.stop_overs} stop over, via {deal.via_city}.' \
                 f'\nwww.google.co.uk/flights?hl=en#flt={deal.departure_airport}.{flight_search.get_IATA_code(deal.via_city)}' \
                 f'.{deal.destination_airport}.{deal.depart_date}*{deal.destination_airport}.{flight_search.get_IATA_code(deal.via_city)}' \
                 f'.{deal.departure_airport}.{deal.return_date}'
    for email in emails: notification_manager.notify(msg, email)


"""Customer Acquisition Code"""
# print("Welcome to Andrew's Flight Club.\nWe find the best flight deals and email you.")
# first_name = input("What is your first name?\n").title()
# last_name = input("What is your last name?\n").title()
# email = input("What is your email?\n")
# confirm_email = input("Type your email again.\n")
# if email == confirm_email:
#     data_manager.save_users_data(first_name, last_name, email)
# else: print("Sorry, your emails did not match")






