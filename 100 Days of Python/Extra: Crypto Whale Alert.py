import requests
import datetime
from twilio.rest import Client
import smtplib
import time

# Crypto Whale Alert, maybe can expand to post on social media (Twitter)?
TICKER = "IOTX"
SYMBOL = "UP" # Because UnicodeEncodeError: 'ascii' codec can't encode character '\U0001f53b' in position 31: ordinal not in range(128)

CRYPTO_API_KEY = "..."
CRYPTO_URL = "https://www.alphavantage.co/query"
CRYPTO_PARAMS = {
    "function": "CRYPTO_INTRADAY",
    "symbol": TICKER,
    "market": "USD",
    "interval": "1min",
    "apikey": CRYPTO_API_KEY,
}
NEWS_API_KEY = "..."
NEWS_URL = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "apiKey": NEWS_API_KEY,
    "q": "bitcoin AND btc", # cos of macroeconomic effect (not sure I'm using this term correctly 😅
    "language": "en",
    "from": datetime.datetime.now() - datetime.timedelta(hours=6), #  6-hourly data refresh
    # "domains": "reuters.com,bloomberg.com,etc",
    # "sortBy": "popularity",
}
while True:
    response = requests.get(url=CRYPTO_URL, params=CRYPTO_PARAMS)
    response.raise_for_status()
    data = [value for key, value in response.json()["Time Series Crypto (1min)"].items()]
    print(data)
    latest_price = float(data[0]["4. close"])
    latest_volume = int(data[0]["5. volume"])
    earlier_price = float(data[1]["4. close"])
    earlier_volume = int(data[1]["5. volume"])
    volume_percentage_diff = "{:.5f}".format(((latest_volume - earlier_volume)/earlier_volume) * 100)
    price_percentage_diff = "{:.5f}".format((abs(latest_price - earlier_price)/earlier_price) * 100)
    if float(volume_percentage_diff) >= 50 and float(price_percentage_diff) >= 1:  # Adjust sensitivity of whale action depending on ticker's marketcap
        if latest_price < earlier_price: SYMBOL = "DOWN"
        response = requests.get(url=NEWS_URL, params=NEWS_PARAMS)
        response.raise_for_status()
        articles = response.json()["articles"]
        msg = ""
        for article in articles:
            # \033[1m: start of bold, \033[0m: end of bold
            # Problematic UnicodeEncodeError converting u/2018 (') using ASCII. Tried googling, but comes with other issues like byte b'...' that cannot be
            # converted back into string to split and etc. BUT the general gist is here. If I really need to brute force it, guess I can use a list or sth.
            msg += f"\033[1mHeadline\033[0m: {article['title']}\n\033[1mBrief\033[0m: {article['description']}\n" \
                   f"\033[1mLink\033[0m: {article['url']}\n\033[1mTime\033[0m: {article['publishedAt']}\n\n"
        # TWILIO_ACC_SID = "..."
        # TWILIO_API_KEY = "..."
        # client = Client(TWILIO_ACC_SID, TWILIO_API_KEY)
        # message = client.messages.create(
        #     body=f'\n❗❗WHALE ALERT❗❗\n{TICKER}: $({SYMBOL}{price_percentage_diff}%), Volume(🔺{volume_percentage_diff}%)\n{msg}',
        #     from_='+15304894584',
        #     to='...(must be verified in account first!)...'
        # )
        my_email = "pythontestosterone@gmail.com"
        password = "..."
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="...",
                msg=f"Subject:WHALE ALERT\n\n{TICKER}: $({SYMBOL} {price_percentage_diff}%), Volume(UP {volume_percentage_diff}%)\n{msg}")
    time.sleep(60) # minute trader

# Eg of what text msg/mail looks like
    """
    WHALE ALERT
    IOTX: $(DOWN 2.99%), Volume(UP 26.31%)
    Headline[BOLD]:Bitcoin, Southwest Airlines, Snap Inc, Moderna, SM Energy - Reuters
    Brief[BOLD]: U.S. stock indexes rose on Friday after data showed consumer prices rose largely in line with estimates last month, taking some pressure off investors concerned about the Federal Reserve's aggressive tightening of its monetary policy.
    Link[BOLD]: https://www.reuters.com/markets/asia/tesla-southwest-airlines-snap-inc-moderna-sm-energy-2021-12-10/
    Time: 00:43:28 SGT (ideally)
    ...
    """
