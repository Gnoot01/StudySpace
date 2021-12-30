"""
Instructions for automating easy-apply jobs:
1. LinkedIn account Me>Settings & Privacy>Data Privacy>Job Seeking Preferences>Job Application Settings>Submit Resume
2. Jobs tab>Fill in desired job & location>Easy Apply filter
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Python\V96_chromedriver.exe" # V no. must match Chrome V no. See notes for exact help.
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
UNTIL_PAGE = 5
HP_NUM = "12345678"
EMAIL = "..."
PASS = "..."

def start(HP_NUM: str):
    # Enable scroll to bottom to load max results, otherwise only 8
    document_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(4, 0, -1):
        driver.execute_script(f"window.scrollTo(0, {document_height / i});")
        time.sleep(1.5)

    jobs = driver.find_elements("css selector", ".jobs-search-results__list .jobs-search-results__list-item .job-card-list__title")
    job_links = [job.get_attribute("href") for job in jobs]
    success = 0
    for job_link in job_links:
        while True:
            time.sleep(1.5)
            driver.get(job_link)
            time.sleep(1)
              
            # If not comfortable applying yet, simply save posting & follow company
            # try:
            #     driver.find_element("class name", "jobs-save-button").click() # Save
            #     driver.find_element("tag name", "html").send_keys(webdriver.Keys.PAGE_DOWN) # To load Follow
            #     time.sleep(1.5)
            #     driver.find_element("css selector", ".jobs-company__box .follow").click() # Follow
            #     break
            #     # Self-discovered, thrown when trying to click an area blocked by something else (not clickable at ...)
            # except ElementClickInterceptedException:
            #     driver.find_elements("class name","msg-overlay-bubble-header__control--new-convo-btn")[1].click()  # minimize default-opened messaging window on half-sized browser window
            #     driver.find_element("css selector", ".jobs-company__box .follow").click()  # Follow
            #     break
            # except NoSuchElementException:
            #     break
            
            # Direct apply with Easy-Apply filter
            try:
                driver.find_element("css selector",".jobs-apply-button--top-card .jobs-apply-button").click()  # Apply now
                time.sleep(1)

                # Clearing the field before inputting
                driver.find_element("css selector", ".fb-single-line-text .fb-single-line-text__input").send_keys(webdriver.Keys.CONTROL + "a")
                driver.find_element("css selector", ".fb-single-line-text .fb-single-line-text__input").send_keys(webdriver.Keys.DELETE)
                driver.find_element("css selector", ".fb-single-line-text .fb-single-line-text__input").send_keys(HP_NUM)
                # OR
                # phone = driver.find_element("css selector", ".fb-single-line-text .fb-single-line-text__input")
                # if phone.text == "": phone.send_keys(HP_NUM)
                time.sleep(2)

                driver.find_element("css selector", "footer div button").click()  # Next
                time.sleep(2)
                driver.find_element("css selector", "footer div .artdeco-button--primary").click()  # Next if got additional form. Else, Review
                time.sleep(2)
                try: # Skipping complex multi-step application identified by extra form section
                    driver.find_element("css selector", "form")
                    break
                except NoSuchElementException: # thrown if no extra form section = easy application, so submit
                    driver.find_element("css selector", "footer div .artdeco-button--primary").click()  # Submit
                    time.sleep(2)
                    success += 1
                    print(f"{success} out of {len(job_links)} successful!")
                    break
            except NoSuchElementException:
                break

driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=101174742&keywords=python&location=Canada")
time.sleep(1)
driver.find_element("link text", "Sign in").click()
time.sleep(1)
email = driver.find_element("name", "session_key")
email.send_keys(EMAIL)
password = driver.find_element("name", "session_password")
password.send_keys(PASS)
driver.find_element("css selector", ".login__form_action_container button").click()
# OR
# password.send_keys(webdriver.Keys.ENTER)


# Does entire UNTIL_PAGE, ends at UNTIL_PAGE+1
for i in range(UNTIL_PAGE):
    start(HP_NUM)
    driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=101174742&keywords=python&location=Canada")
    time.sleep(2)
    pages = driver.find_elements("css selector", ".artdeco-pagination__pages li")[1:8]
    # cos linkedIn's buttons don't update everytime +1. Once page 8 reached, need to press ... to reveal 3 more (9-11)
    # Would need to account for this edge case in future if UNTIL_PAGE > 8
    print(len(pages))
    pages[i].click() # clicks on page i+1

driver.quit()
