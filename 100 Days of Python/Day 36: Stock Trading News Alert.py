# Idea: do one for crypto
import requests
import datetime
from twilio.rest import Client

TICKER = "TSLA"
COMPANY_NAME = "Tesla"
SYMBOL = "🔺"

def get_date(date: datetime, minus_days: int) -> str:
    # This accounts for irregularities such as yyyy-12-01(m), yyyy-01-01 (y & m), leap years (Feb)
    return str(date - datetime.timedelta(days=minus_days)).split(" ")[0]

def price_percent_diff(response_data: requests, first_day: str, second_day: str) -> str:
    price_first_day = float(response_data["Time Series (Daily)"][first_day]["4. close"])
    price_second_day = float(response_data["Time Series (Daily)"][second_day]["4. close"])
    global SYMBOL
    if price_first_day < price_second_day: SYMBOL = "🔻"
    # Always compares % -/+ wrt second day
    return "{:.2f}".format((abs(price_first_day - price_second_day)/price_second_day) * 100)


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increases/decreases by 5% between yesterday and the day before then print("Get News").

STOCK_API_KEY = "..."
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": TICKER,
    "apikey": STOCK_API_KEY,
    "outputsize": "compact",
}

# checks if is weekday, since stocks don't trade on weekends, and thus stats don't exist on weekends for this API
# 0: Monday, 1: Tuesday, 6: Sunday
if datetime.datetime.now().weekday() not in [0, 1, 6]:
    # Alternatively, since most API only adds if on weekday & adds to the stack, most recent=ystd=list[0], day_before = list[1]
    # Hence, data_list = [value for key, value in response.json()["Time Series (Daily)"].items()], price_ystd = data_list[0]["4. close"]
    date_ystd = get_date(datetime.datetime.now(), 1)
    date_day_before = get_date(datetime.datetime.now(), 2)
    response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
    response.raise_for_status()
    percentage_diff = price_percent_diff(response.json(), date_ystd, date_day_before)
    if float(percentage_diff) >= 5:

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
        NEWS_API_KEY = "..."
        NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
        news_parameters = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": COMPANY_NAME,
            "language": "en",
            "from": date_ystd,
            # "domains": "reuters.com,bloomberg.com,etc",
            # "sortBy": "popularity",
        }
        response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
        response.raise_for_status()
        articles = response.json()["articles"][:3]
        msg = ""
        for article in articles:
            # \033[1m: start of bold, \033[0m: end of bold
            msg += f"\033[1mHeadline\033[0m: {article['title']}\n\033[1mBrief\033[0m: {article['description']}\n\033[1mLink\033[0m: {article['url']}\n\n"

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
        TWILIO_ACC_SID = "..."
        TWILIO_API_KEY = "..."
        client = Client(TWILIO_ACC_SID, TWILIO_API_KEY)
        message = client.messages.create(
            body=f'\n{TICKER}: {SYMBOL}{percentage_diff}%\n{msg}',
            from_='+15304894584',
            to='...(must be verified in account first!)...'
        )

# Eg of what text msg looks like
"""
TSLA: 🔻5.99%
Headline[BOLD]: Tesla, Southwest Airlines, Snap Inc, Moderna, SM Energy - Reuters
Brief[BOLD]: U.S. stock indexes rose on Friday after data showed consumer prices rose largely in line with estimates last month, taking some pressure off investors concerned about the Federal Reserve's aggressive tightening of its monetary policy.
Link[BOLD]: https://www.reuters.com/markets/asia/tesla-southwest-airlines-snap-inc-moderna-sm-energy-2021-12-10/

...
"""

