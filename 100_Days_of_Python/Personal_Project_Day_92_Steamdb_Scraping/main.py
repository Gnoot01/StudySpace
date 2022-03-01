"""
https://steamdb.info/, put data into .csv, can analyse data from there
"""
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pandas as pd
import html
import re
import smtplib
import os

"1. Today's Top, 'Still Popular' games from launch: 24h peak ~PERCENT_DIFF% from All-Time Peak - 24hr peak, All-Time Peak, link, Name, genre(tags), Developer, Release_Date, Since_Release, rating"

CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Dev Me\Python\V96_chromedriver.exe"
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
action = webdriver.common.action_chains.ActionChains(driver)
PERCENT_DIFF = 20.00
games = []


def cal_percent_diff(all_time_peak, day_peak):
    return ((all_time_peak - day_peak)/all_time_peak) * 100


driver.get("https://steamdb.info/graph/")
driver.maximize_window()
time.sleep(2)

# Setting no. of entries on 1 page
driver.find_element("xpath", '//*[@id="table-apps_length"]/label/select').click() # Show ___ entries
time.sleep(1)
driver.find_element("xpath", '//*[@id="table-apps_length"]/label/select/option[5]').click() # 1K
# //*[@id="table-apps_length"]/label/select/option[6] # 5k
# //*[@id="table-apps_length"]/label/select/option[7] # All (slow)
time.sleep(2)
driver.find_element("xpath", '//*[@id="table-apps"]/thead/tr/th[5]').click() # 24h Peak to sort by
time.sleep(1)

for i in range(9):
    driver.execute_script("window.scrollBy(0,5000);")
    time.sleep(0.1)

rows = driver.find_elements("css selector", ".dataTable_table_wrap tbody tr td")
for i in range(0, 1000, 7):
    day_peak = int(rows[i + 4].text.replace(",", ""))
    all_time_peak = int(rows[i + 5].text.replace(",", ""))
    if cal_percent_diff(all_time_peak, day_peak) <= PERCENT_DIFF:
        # Problem: cannot hover to load on-hover data, so cannot add genres which shows 6 tags
        # Solution: 1. couldn't hover cos window was not maximised 😅, 2. ActionsChains for hover,  3. Explicit wait vs time.sleep for extracting info on hover when normally "hidden"
        # (from selenium.webdriver.support.ui import WebDriverWait + from selenium.webdriver.support import expected_conditions as EC)
        link = rows[i + 2].find_element("tag name", "a").get_attribute("href")
        game_id = link.split("/")[-3]

        action.move_to_element(rows[i + 2]).perform()
        # presence_of_all_elements_located for elements list
        game_hover_info = WebDriverWait(driver, 3).until(EC.presence_of_element_located(("id", f'js-hover-app-{game_id}'))) # Hover menu pops up
        # for &amp;
        developer = html.unescape(game_hover_info.find_element("css selector", ".hover_body b").text) # Developer:
        time.sleep(0.5) 
        genres = [genre.text for genre in game_hover_info.find_elements("css selector", ".hover_tag_row a")[:3]] # Genre Tags
        time.sleep(0.5)
        release_date = game_hover_info.find_elements("class name", "hover_body")[1].text # Publiser:/Release Date:
        time.sleep(0.5)
        if "Publisher" in release_date:
            release_date = game_hover_info.find_elements("class name", "hover_body")[2].text
            time.sleep(0.5)
        release_date = release_date.split(":")[1].strip()
        since_release = np.nan
        rating = np.nan
        if release_date != "Unknown":
            since_release = str(datetime.datetime.now() - datetime.datetime.strptime(release_date, "%d %B %Y")).split(",")[0]
            rating = game_hover_info.find_element("css selector", ".hover_review_summary span").text # Rating:
            time.sleep(0.5)
        games.append({"Name": rows[i + 2].text,
                      "Developer": developer,
                      "Genres": genres,
                      "Link": link,
                      "24h Peak": int(rows[i + 4].text.replace(",", "")),
                      "All-Time Peak": int(rows[i + 5].text.replace(",", "")),
                      "Release_Date": release_date,
                      "Since_Release": since_release,
                      "Rating": rating,
                      })
if len(games) != 0: pd.DataFrame(games).to_csv("still_popular_from_launch_games.csv")
else: print(f"Found no games with 24h Peak {PERCENT_DIFF}% down from All-Time Peak, adjust PERCENT_DIFF!")
driver.quit()
####################################################################################################################################################################################################
"""
2. Downfall of games: 24h peak (>=10000) ~80% from All-Time Peak
The initial method I used for 1. before learning about hover functionality and changing my method
"""

# CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Dev Me\Python\V96_chromedriver.exe"
# driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
# PERCENT_DIFF = 80.00
# THRESHOLD = 10000
# games = []
#
#
# def cal_percent_diff(all_time_peak, day_peak):
#     return ((all_time_peak - day_peak)/all_time_peak) * 100
#
#
# driver.get("https://steamdb.info/graph/")
# time.sleep(2)
#
# # Setting no. of entries on 1 page
# driver.find_element("xpath", '//*[@id="table-apps_length"]/label/select').click() # Show ___ entries
# time.sleep(1)
# driver.find_element("xpath", '//*[@id="table-apps_length"]/label/select/option[5]').click() # 1K
# # //*[@id="table-apps_length"]/label/select/option[6] # 5k
# # //*[@id="table-apps_length"]/label/select/option[7] # All (slow)
# time.sleep(2)
# driver.find_element("xpath", '//*[@id="table-apps"]/thead/tr/th[5]').click() # 24h Peak to sort by
# time.sleep(1)
#
# for i in range(9):
#     driver.execute_script("window.scrollBy(0,5000);")
#     time.sleep(0.1)
#
# rows = driver.find_elements("css selector", ".dataTable_table_wrap tbody tr td")
# for i in range(0, 1000, 7):
#     day_peak = int(rows[i+4].text.replace(",", ""))
#     all_time_peak = int(rows[i+5].text.replace(",", ""))
#     if cal_percent_diff(all_time_peak, day_peak) >= PERCENT_DIFF and day_peak >= THRESHOLD:
#         games.append({"Name": rows[i + 2].text,
#                       "Developer": "",
#                       "Link": rows[i + 2].find_element("tag name", "a").get_attribute("href"), # To find element within an element
#                       "24h Peak": int(rows[i + 4].text.replace(",", "")),
#                       "All-Time Peak": int(rows[i + 5].text.replace(",", "")),
#                       })
# if len(games) != 0:
#     for game in games:
#         driver.get(game['Link'])
#         time.sleep(1)
#         # Some game pages have an extra row "Store Name", so checks if "Store Name" or "Developer"
#         if driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[3]/td[1]').text == "Store Name":
#             # for &amp;
#             game["Developer"] = html.unescape(driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[4]/td[2]/a').text) # Developer|
#             time.sleep(0.5)
#             try:
#                 # As sometimes, 10 September 2021 – 04:00:00 UTC (5 months ago) & 18 October 2012 (9 years ago)
#                 game["Release_Date"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[9]/td[2]').text.split("(")[0].split("–")[0].strip() # Release Date|
#                 time.sleep(0.5)
#                 game["Since_Release"] = str(datetime.datetime.now() - datetime.datetime.strptime(game["Release_Date"], "%d %B %Y")).split(",")[0]
#                 game["Rating"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/div[2]/a[1]/div').text
#                 time.sleep(0.5)
#             except NoSuchElementException:
#                 # For some reason, game = {} still writes, excluding Release_Date onwards vs games[games.index(game)] = {} writes ,,,,,,,, instead
#                 pass
#         else:
#             game["Developer"] = html.unescape(driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[3]/td[2]/a').text)
#             time.sleep(0.5)
#             try:
#                 game["Release_Date"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[8]/td[2]').text.split("(")[0].split("–")[0].strip()
#                 time.sleep(0.5)
#                 game["Since_Release"] = str(datetime.datetime.now() - datetime.datetime.strptime(game["Release_Date"], "%d %B %Y")).split(",")[0]
#                 game["Rating"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/div[2]/a[1]/div').text
#                 time.sleep(0.5)
#             except NoSuchElementException:
#                 pass
#
#     pd.DataFrame(games).to_csv("downfall_games.csv")
#
# else: print(f"Found no games with 24h Peak of at least {THRESHOLD} players and {PERCENT_DIFF}% down from All-Time Peak, adjust THRESHOLD and PERCENT_DIFF!")
# driver.quit()
####################################################################################################################################################################################################
"""
3. Top Discounted Games: New Historical Low - Steam Sale Counter, Link, Release_Date, Since_Release, Rating, Prices, Date_Checked, Sale_Event: (anything b4 & including 'year/sale/event/festival') saved in SQL db, to deduce patterns
Regex help <3 from 
Regex Generator: https://regex-generator.olafneumann.org/?sampleText=2020-03-12T13%3A34%3A56.123Z%20INFO%20%20%5Borg.example.Class%5D%3A%20This%20is%20a%20%23simple%20%23logline%20containing%20a%20%27value%27.&flags=i&onlyPatterns=false&matchWholeLine=false&selection=
Regex Checker: https://regexr.com/
Note: SQL will be implemented later when I've learnt more about it, and use MySQL. Right now, I only know sqlite (and hence need to know sql commands) and flask-sqlalchemy
"""

# CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Dev Me\Python\V96_chromedriver.exe"
# driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
# historical_cheap_games = []
# DEFAULT_CURR_NAME = "Singapore Dollar"
# DEFAULT_CURR_CODE = "SGD"
# DEFAULT_CURR_SYMBOL = "$"
# # Using ISO 4217 codes for currency: https://assemblysys.com/iso-4217-currency-codes/
# CURR_CODE = input("Input currency to view prices in (ISO 4217 code: https://assemblysys.com/iso-4217-currency-codes/): ")
# """
# Problem: Steamdb website is messed up - some currencies don't exist, inconsistency with symbols and currency displayed, etc
#          Even if only CURR_SYMBOLS used, some like CNY & JPY use ¥, many use $, aka the same symbols which will only
#          match the first one found, since we're comparing in order
# Solution: use CURR_NAME to match website's exact name, compare, then convert and display the final using CURR_SYMBOLS, default: DEFAULT_SYMBOL
# """
# CURR_NAMES = {"ARS": "Argentine Peso", "TRY": "Turkish Lira", "RUB": "Russian Ruble", "BRL": "Brazilian Real",
#              "KZT": "Kazakhstani Tenge", "INR": "Indian Rupee", "COP": "Colombian Peso",
#              "IDR": "Indonesian Rupiah", "UYU": "Uruguayan Peso", "ZAR": "South African Rand",
#              "VND": "Vietnamese Dong", "CLP": "Chilean Peso", "MXN": "Mexican Peso", "UAH": "Ukrainian Hryvnia",
#              "MYR": "Malaysian Ringgit", "THB": "Thai Baht", "PHP": "Philippine Peso", "PEN": "Peruvian Sol",
#              "CNY": "Chinese Yuan", "SAR": "Saudi Riyal", "KWD": "Kuwaiti Dinar",
#              "TWD": "Taiwan Dollar", "HKD": "Hong Kong Dollar", "QAR": "Qatari Riyal", "CRC": "Costa Rican Colon",
#              "AED": "U.A.E. Dirham", "NOK": "Norwegian Krone", "NZD": "New Zealand Dollar",
#              "KRW": "South Korean Won", "PLN": "Polish Zloty", "JPY": "Japanese Yen", "CAD": "Canadian Dollar",
#              "EUR": "Euro", "GBP": "British Pound", "USD": "U.S. Dollar", "AUD": "Australian Dollar",
#              "CHF": "Swiss Franc", "ILS": "Israeli New Shekel"}
# CURR_SYMBOLS = {"TRY": "₺", "RUB": "₽", "BRL": "R$", "KZT": "₸", "INR": "₹", "IDR": "Rp", "ZAR": "R", "VND": "₫",
#                 "UAH": "₴", "MYR": "RM", "THB": "฿", "PHP": "₱", "PEN": "S/.", "CNY": "¥", "SAR": "ر.س",
#                 "KWD": "د.ك", "QAR": "ر.ق", "CRC": "₡", "AED": "د.إ", "NOK": "kr", "KRW": "₩", "PLN": "zł",
#                 "JPY": "¥", "EUR": "€", "GBP": "£", "CHF": "Fr", "ILS": "₪"}
# CHOSEN_CURR_NAME = CURR_NAMES.get(CURR_CODE, DEFAULT_CURR_NAME)
# CHOSEN_CURR_SYMBOL = CURR_SYMBOLS.get(CURR_CODE, DEFAULT_CURR_SYMBOL)
#
# driver.get("https://steamdb.info/sales/")
# driver.maximize_window()
# time.sleep(2)
#
#
# # Setting no. of entries on 1 page
# driver.find_element("xpath", '//*[@id="DataTables_Table_0_length"]/label/select').click() # Show ___ entries
# time.sleep(1)
# driver.find_element("xpath", '//*[@id="DataTables_Table_0_length"]/label/select/option[7]').click() # All (slow)
# time.sleep(3)
# driver.find_element("xpath", '//*[@id="DataTables_Table_0"]/thead/tr/th[4]').click() # % (Discount Percentage) to sort by ⬇ to ⬆
# time.sleep(1)
# driver.find_element("xpath", '//*[@id="DataTables_Table_0"]/thead/tr/th[4]').click() # % (Discount Percentage) to sort by ⬆ to ⬇
# time.sleep(1)
#
# sale_countdown = driver.find_element("id", "js-sale-countdown").text.strip() # Eg. Steam Lunar New Year Sale 2022 ends on February 3rd
# sale_name = re.search(r"^(.*[2][0-9][0-9][0-9]|Sale|Event|Fest)", sale_countdown).group()
#
# for i in range(19):
#     driver.execute_script("window.scrollBy(0,7500);")
#     time.sleep(0.1)
#
#
# rows = driver.find_elements("css selector", "tbody tr")
# for row in rows:
#     try:
#         row.find_element("class name", "price-discount-major") # New Historical Low
#         historical_cheap_games.append({"Name": row.find_element("class name", "b").text,
#                                        "Developer": "",
#                                        "Link": row.find_element("class name", "b").get_attribute("href"),
#                                        })
#     except NoSuchElementException:
#         pass
#
# for game in historical_cheap_games:
#     driver.get(game['Link'])
#     time.sleep(1)
#     # Some game pages have an extra row "Store Name", so checks if "Store Name" or "Developer"
#     if driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[3]/td[1]').text == "Store Name":
#         # for &amp;
#         game["Developer"] = html.unescape(driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[4]/td[2]/a').text) # Developer|
#         time.sleep(0.5)
#         try:
#             # As sometimes, 10 September 2021 – 04:00:00 UTC (5 months ago) & 18 October 2012 (9 years ago)
#             game["Release_Date"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[9]/td[2]').text.split("(")[0].split("–")[0].strip() # Release Date|
#             time.sleep(0.5)
#             game["Since_Release"] = str(datetime.datetime.now() - datetime.datetime.strptime(game["Release_Date"], "%d %B %Y")).split(",")[0]
#             game["Rating"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/div[2]/a[1]/div').text
#             time.sleep(0.5)
#         except NoSuchElementException:
#             # For some reason, game = {} still writes, excluding Release_Date onwards vs games[games.index(game)] = {} writes ,,,,,,,, instead
#             pass
#     else:
#         game["Developer"] = html.unescape(driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[3]/td[2]/a').text)
#         time.sleep(0.5)
#         try:
#             game["Release_Date"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[8]/td[2]').text.split("(")[0].split("–")[0].strip()
#             time.sleep(0.5)
#             game["Since_Release"] = str(datetime.datetime.now() - datetime.datetime.strptime(game["Release_Date"], "%d %B %Y")).split(",")[0]
#             game["Rating"] = driver.find_element("xpath", '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/div[2]/a[1]/div').text
#             time.sleep(0.5)
#         except NoSuchElementException:
#             pass
#
#         driver.find_element("xpath", '//*[@id="js-currency-selector"]').click() # Set your currency
#         time.sleep(0.5)
#         currency_buttons = driver.find_elements("css selector", ".currency-selector button") # Finding CHOSEN_CURR
#         for button in currency_buttons:
#             if button.text.strip() == CHOSEN_CURR_NAME:
#                 button.click()
#                 time.sleep(1)
#                 break
#
#         driver.execute_script("window.scrollBy(0,750);")
#         price_rows = driver.find_elements("css selector", ".table-prices tbody tr")
#         time.sleep(1)
#         prices = []
#         for price_row in price_rows:
#             price_row_name = price_row.find_element("tag name", "td").text.strip()
#             time.sleep(1)
#             if price_row_name != CHOSEN_CURR_NAME:
#                 price = price_row.find_element('class name', 'table-prices-converted').text
#             else:
#                 # if price_row_name == CHOSEN_CURR_NAME, there's no element under table-prices-converted since no conversion
#                 price = price_row.find_elements('tag name', 'td')[2].text
#             time.sleep(0.5)
#             try:
#                 price = re.search(r"\d*[.,]*\d\d", price).group()
#                 time.sleep(1)
#                 prices.append(f"In {price_row_name}: {price}{CHOSEN_CURR_SYMBOL}")
#             # field is N/A (doesn't match)
#             except AttributeError:
#                 pass
#         game["Prices"] = prices
#         game["Date_Checked"] = datetime.datetime.now().strftime("%d %b %Y")
#         game["Sale_Event"] = sale_name
#
#     pd.DataFrame(historical_cheap_games).to_csv(f"historical_cheap_games_in_{CHOSEN_CURR_NAME}.csv")
#
# driver.quit()
############################################################################################################################################################################################
"""
Simple program to sign in with Steam to filter wishlist, scrape and notify (via mail) if any wishlisted < DESIRED_PRICE/new historical low discount
Couldn't continue further due to some network congestion issues, but outline of program is as such:
1. Sign in to Steam to retrieve wishlisted games data
2. Tick "Show only wishlisted" checkbox on https://steamdb.info/sales/ to filter out games
3. Scrape and notify (via mail(smtplib)) if any wishlisted < DESIRED_PRICE/new historical low discount
OR
1. Simply input any game names to wishlist in wishlist = []
2. for game in wishlist: searchbox.send_keys(game)
3. Scrape and notify (via mail(smtplib)) if any wishlisted < DESIRED_PRICE/new historical low discount
"""

# CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Dev Me\Python\V96_chromedriver.exe"
# driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
# DESIRED_PRICE = 4.29
# STEAM_USERNAME = os.environ.get("STEAM_USERNAME")
# STEAM_PASSWORD = os.environ.get("STEAM_PASSWORD")
#
# driver.get("https://steamdb.info/login/?page=sales")
# driver.maximize_window()
#
# WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="js-sign-in"]'))).click() # Sign in through Steam Button
# WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="steamAccountName"]'))).send_keys(STEAM_USERNAME) # Steam username
# WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="steamPassword"]'))).send_keys(STEAM_PASSWORD) # Password




