import smtplib
import requests
from bs4 import BeautifulSoup
import os

# Some websites like Amazon block requests for web scraping, so additional info from browser need to be passed via request HEADERS. Check with http://myhttpheader.com/, minimally need the below 2
# Otherwise, just proxy/rotating IP Address, etc
URL = "https://www.amazon.com/dp/B00X9JNWGS/ref=sbl_dpx_kitchen-electric-cookware_B08GC6PL3D_0"
HEADERS = {
    "User-Agent": "https://www.amazon.com/dp/B00X9JNWGS/ref=sbl_dpx_kitchen-electric-cookware_B08GC6PL3D_0",
    # User-Agent first check to identify sus requests. If numerous & identical, seems like bot activity so blocked
    "Accept-Language": "https://www.amazon.com/dp/B00X9JNWGS/ref=sbl_dpx_kitchen-electric-cookware_B08GC6PL3D_0",
    # Ensures set languages are in accordance with the data-target domain and user’s IP location. If same user yet multiple languages, blocked
    # Accept-Encoding: "gzip, deflate" [compresses data & reduces traffic volume]
    # Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8" [to configure accordingly to the web server’s accepted format, so more organic communication]
    # Referer: "www.google.com" (random address) [Provides previous web page’s address to server, so seems more random & organic.]
    # Cookie:
}
BUY_PRICE = 400

response = requests.get(url=URL, headers=HEADERS)
content = response.text

soup = BeautifulSoup(content, "html.parser")
price = soup.find(name="span", class_="a-offscreen").getText().split("$")[1]
product = soup.find(name="span", id="productTitle").getText().strip()

if float(price) <= BUY_PRICE:
    my_email = "pythontestosterone@gmail.com"
    PASSWORD = os.environ.get("PASSWORD")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=PASSWORD)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject:Amazon Price Alert!\n\n{product} is now ${price}\n{URL}")
