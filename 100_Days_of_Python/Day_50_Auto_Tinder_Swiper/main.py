"""
I actually created a Tinder account for this purpose... Call it dedication. I'll delete my account after though.
P.S I feel bad for cat (or rather dog) fishing people using https://www.thispersondoesnotexist.com/ & my fav doggo... YIKess
Works well, except only 8 swipes before getting detected by Tinder from network traffic & getting browser auto closed
https://stackoverflow.com/questions/56528631/is-there-a-version-of-selenium-webdriver-that-is-not-detectable
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import random

CHROME_DRIVER_PATH = "V96_chromedriver.exe"
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))

"""
Solution 1: Downloading VPN extension first because for some reason, can't access Tinder.com... My ISP blocks it 🙄 :/
Doesn't work cos aft adding extension, can't get Selenium to click & enable it
"""
# driver.get("https://chrome.google.com/webstore/detail/touch-vpn-secure-and-unli/bihmplhobchoageeokmgbdihknkjbknd")
# driver.find_element("xpath", "/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div").click() # Add to Chrome
# driver.find_element("tag name", "html").send_keys(webdriver.Keys.ARROW_LEFT) # To move to 'Add Extension'
# driver.find_element("tag name", "html").send_keys(webdriver.Keys.ENTER) # Add Extension
# time.sleep(2)
# driver.close() # Closes auto-opened extension tab

"""
Solution 2: Getting Selenium to automate by adding .crx file upon browser launch.
Doesn't work, tried googling for solution, other extensions work, but not this vpn one, and is unsolved online sooooo 🤷‍♂️
"""
# driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH), options=webdriver.ChromeOptions().add_extension("vpn_extension.crx"))
# driver.get('http://www.tinder.com') 

"""
Solution 3: From personal experience, I know using mobile data works for bypassing ISP-blocked websites. Should have thought of this sooner...
I know right, what a non-codable ingenious solution!
"""
driver.get("https://tinder.com/")
driver.maximize_window()
time.sleep(2)
driver.find_element("xpath", '//*[@id="o-1556761323"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a').click() # Log in
time.sleep(2)
driver.find_element("xpath", '//*[@id="o-1335420887"]/div/div/div[1]/div/div[3]/span/div[2]/button').click() # LOG IN WITH FACEBOOK

time.sleep(3)
# Separate FB window pops up
# window_handles is a list of all windows popped up, with later windows further down in sequence, so switch_to latest window ([-1])
driver.switch_to.window(driver.window_handles[-1])
# Ensuring current window to use is Facebook
if driver.title == "Facebook":
    email = driver.find_element("xpath", '//*[@id="email"]')
    if email.text == "": email.send_keys("...")
    password = driver.find_element("xpath", '//*[@id="pass"]')
    password.send_keys("...")
    password.send_keys(webdriver.Keys.ENTER)
    time.sleep(3)

driver.switch_to.window(driver.window_handles[0])
time.sleep(5)
driver.find_element("xpath", '//*[@id="o-1335420887"]/div/div/div/div/div[3]/button[1]').click() # Allow Location pop-up
time.sleep(2)
driver.find_element("xpath", '//*[@id="o-1335420887"]/div/div/div/div/div[3]/button[2]').click() # Disallow Notification pop-up
time.sleep(2)
driver.find_element("xpath", '//*[@id="o-1556761323"]/div/div[2]/div/div/div[1]/button').click() # I Accept Cookies
time.sleep(2)



# Tinder free tier only allows 100 "Likes" per day. If you have a premium account, feel free to change to a while loop.
for _ in range(100):
    time.sleep(1)
    no_of_pics = 0
    
    # If profile has more pics to see, see all pics
    try:
        # first bar is bullet-active, checks how many bars(pics) there are
        no_of_pics = int(driver.find_elements("css selector", ".tappable-view .bullet--active .Hidden")[1].text.split("/")[1])
        # Click > Next no_of_pics-1 times to see all pics
        for _ in range(no_of_pics-1):
            time.sleep(random.randint(2, 5))
            """
            Tried many methods to click on svg icon. but always some exception
            1. Not this cos this always never gets/gets the wrong one
            # driver.find_element("xpath", '//*[@id="o-1556761323"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/svg[2]').click()
            2. Self-constructed xpath for svg using Youtube vids. This works. But I didn't know the issue was with cursor click offset, so I tried 3.
            # driver.find_elements("xpath", '//*[name()="svg"]')[7].click()
            3. Not click on path, click on svg. Don't need so specific anyways (<path class d="...">)
            # driver.find_elements("xpath", '//*[name()="path" and @d="M13.98 20.717a1.79 1.79 0 0 0 2.685 0 1.79 1.79 0 0 0 0-2.684l-7.158-6.62 7.158-6.8a1.79 1.79 0 0 0 0-2.684 1.79 1.79 0 0 0-2.684 0L5.929 9.98a1.79 1.79 0 0 0 0 2.684l8.052 8.052z"]')[1].click()
            2 with cursor click offset. Clicks on tip of > instead of clicking in middle which throws ElementClickInterceptedException.
            # Would be great to learn something that shows current cursor position, but selenium doesn't actually control the cursor. 
            # 1 way to get it to show is to ....context_click().perform() which right clicks so can kinda see where it's clicking
            # ActionChains .perform() is a 'dumber' click than webdriver .click() as the latter checks preconditions.
            # .perform() fires events in the order they are queued up (so can -> chain move_to_element(menu).click(hidden_submenu).perform())
            # ....build().perform()?
            """
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(driver.find_elements("xpath", '//*[name()="svg"]')[7], 2, 0).click().perform()
        time.sleep(3)
    except NoSuchElementException:
        pass
    except ElementClickInterceptedException:
        pass
    except IndexError:
        driver.find_element("xpath", '//*[@id="o-1556761323"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[5]/div/div[4]/button').click()
        time.sleep(random.randint(3, 7))
        break
    while True:
        # For some reason 1st 'Like' is a diff xpath from 2nd 'Like'. methinks it's to store like history
        try:
            driver.find_element("xpath", '//*[@id="o-1556761323"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[4]/div/div[4]/button').click()
            time.sleep(random.randint(3, 7))
            break
        except NoSuchElementException or ElementClickInterceptedException:
          # After 1st 'Like'
            try:
                # 'Like' button
                driver.find_element("xpath", '//*[@id="o-1556761323"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[5]/div/div[4]/button').click()
                # Random delay between likes so doesn't seem sus bot behaviour
                time.sleep(random.randint(3, 7))
                break
            # While waiting for people to load up on Tinder, 'Like' button not reachable, so wait
            except NoSuchElementException:
                time.sleep(5)
                print("Loading people")
                continue
            # It's a Match!, 'Like' button hidden behind pop-up, Click 'Back to Tinder' to dismiss
            except ElementClickInterceptedException:
                time.sleep(3)
                print("Matched with someone! Lucky fella!")
                time.sleep(1)
                # If below doesn't work, use this
                # action.move_to_element_with_offset(driver.find_element("xpath", '//*[name()="button" and @class="Bdc($c-bluegray):h"]'), X, Y).click().perform()
                driver.find_element("css selector", 'div .Bdc($c-bluegray):h').click()
                break

driver.quit()




