import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import requests


CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Dev Me\Python\V96_chromedriver.exe"
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PIN = os.environ.get("PIN")
# For Captcha Bypass Method 2
API_KEY = os.environ.get("API_KEY")
SUBMIT_URL = "http://2captcha.com/in.php"
RETRIEVE_URL = "http://2captcha.com/res.php"

venue_ans = input("What venue? t/pr: ").lower()
VENUES = {"t": 900, "pr": 544}
when_ans = input("When? DD MM: ")
when_split = when_ans.split(" ") # datetime.datetime.now().strftime("%d %m %Y").split(" ")
time_from = (int(str(datetime.datetime(2022, int(when_split[1]), int(when_split[0])) - datetime.datetime(1970, 1, 1)).split(" ")[0]) * 24 * 60 * 60) - 28800
PREFERRED_SLOTS = ["09:00 AM", "11:00 AM", "07:00 PM", "09:00 PM"]
TODAY = datetime.datetime.strftime(datetime.datetime.now(), "%Y %M %d").split(" ")

while True:
    # This is to ensure the bot auto verifies if it's 9AM already, instead of having to humanly verify
    if datetime.datetime.now() >= datetime.datetime(int(TODAY[0]), int(TODAY[1]), int(TODAY[2]), 9):
        start_time = time.time()

        # chrome_options = webdriver.chrome.options.Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))

        driver.get("https://members.myactivesg.com/auth")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="email"]'))).send_keys(EMAIL)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="password"]'))).send_keys(PASSWORD)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="btn-submit-login"]'))).click()

        driver.get(f"https://members.myactivesg.com/facilities/view/activity/1031/venue/{VENUES.get(venue_ans)}?time_from={time_from}")
        # Captcha Bypass Method 1
        time.sleep(3)
        # Captcha Bypass Method 2 (https://2captcha.com/)
        SUBMIT_PARAMS = {"key": API_KEY,
                         "method": "userrecaptcha",
                         "googlekey": "DATA-SITEKEY_VALUE", # Inspect Element for data-sitekey
                         "pageurl": "URL_OF_PAGE_W_CAPTCHA",
                         "json": 1
                         }
        submit_response = requests.post(SUBMIT_URL, json=SUBMIT_PARAMS)
        time.sleep(15)
        # response is captcha id (success) / error code (error)
        # Handle errors: https://2captcha.com/2captcha-api#in_errors
        if type(submit_response.json().get("request")) is int:
            RETRIEVE_PARAMS = {"key": API_KEY,
                               "action": "get",
                               "id": submit_response,
                               "json": 1,
                               }
            while requests.get(RETRIEVE_URL, params=RETRIEVE_PARAMS).json().get("request") == "CAPCHA_NOT_READY":
                time.sleep(5)
            retrieve_response = requests.get(RETRIEVE_URL, params=RETRIEVE_PARAMS).json().get("request")
            driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{retrieve_response}";')
            # Then need to refresh or do anything to submit, since we're submitting by javascript..?
            # If so, driver.get(f"https://members.myactivesg.com/facilities/view/activity/1031/venue/{VENUES.get(venue_ans)}?time_from={time_from}")
            # or simply, use their library (https://github.com/2captcha/2captcha-python)

        all_slots = driver.find_elements("css selector", ".timeslot-grid div")
        avail_slots = [slot for slot in all_slots if slot.find_element("tag name", "input").get_attribute("id")]
        for avail_slot in avail_slots:
            avail_slot_split = avail_slot.text.split(" ")
            slot_time = " ".join(avail_slot_split[:2])
            slots_left = " ".join(avail_slot_split[2:])
            if slot_time in PREFERRED_SLOTS:
                avail_slot.click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="addtocartbtn"]'))).click() # Add to cart
                time.sleep(1.5)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(("css selector", '.modal-footer .bootbox-accept'))).click()  # Ok
                time.sleep(1)
                for i in range(len(PIN)):
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", f'//*[@id="formCartPayment"]/div[1]/div/div/div[1]/input[{i+1}]'))).send_keys(PIN[i])  # Pin
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="formCartPayment"]/div[2]/div/div/input'))).click() # Book
                print(f"Successfully booked for {slot_time} with {slots_left[0]} slots left, taking {'{:.2f}'.format(time.time() - start_time)}s")
                break
        break

# driver.quit()
