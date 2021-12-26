"""
An idea at 5am on Christmas I just had to automate since cooldown cut to 15 mins vs usual 1hr LOL.
Can be improved further (Eg. Requirements 2 & 3 by checking name of channel/chat instead)
Requirements:
1. join https://discord.gg/qkpcGXKHCQ
2. By default, newly added channels shld be first channel. If not, move it up.
3. (For ready_alts()) Alt Bot chat shld be first chat. If not, move it up.

Can't automate roblox accounts logging in & changing pass since roblox ALWAYS asks to verify via captchas, but at least can
automate inputting fields & changing pass inhumanly fast. Besides that, still not really hands-off either as I want to
add a number beside their names, to make it look like it's not a throwaway but Roblox has weird policies about disallowing names
containing ss, 420, 69, 1553(???) and that requires regex so...

Because I use Brave and not Chrome, wanted to directly import passwords from driver Chrome->Brave. BUT
1. Requires .csv file properly formatted (aka need to be directly from Chrome exported to import into Brave). I know this
because I tried using a pandas-created .csv but that has a COMMA in the first column for index eg. ,name,url,user,pass.
Not sure how to get rid of comma column to make this happen.
2. Can't simply edit that file anyway & copy-paste to replace comma column then import into Brave, as Brave rejects it.
3. Can't manually type/copy-paste my .txt with appropriate headers & create a csv also, as Brave rejects it.
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random

CHROME_DRIVER_PATH = "V96_chromedriver.exe"
DISCORD_EMAIL = ...
DISCORD_PASS = ...
RBLX_CHANGE_PASS_TO = ...

def get_alts():
    while True:
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
        driver.get("https://discord.com/login")
        time.sleep(3)

        # Log in to Discord
        email = driver.find_element("xpath", '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input')
        email.send_keys(DISCORD_EMAIL)
        time.sleep(1)
        password = driver.find_element("xpath", '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input')
        password.send_keys(DISCORD_PASS)
        password.send_keys(webdriver.Keys.ENTER)
        time.sleep(4)
        driver.find_element("class name", 'blobContainer-tHk012').click() # Channel click
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="channels"]/div/div[11]/div/div/a/div[2]/div').click() # Channel chat click
        time.sleep(2)
        input = driver.find_element("xpath", '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')
        input.click()
        input.send_keys("!gen") # to generate alt
        input.send_keys(webdriver.Keys.ENTER)
        time.sleep(2)
        # Can add hovering to delete message ActionChains submenu
        driver.quit()
        # timer for 1 hr starts
        time.sleep(random.randint(3610, 3620))

def ready_alts():
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
    driver.get("https://discord.com/login")
    time.sleep(3)

    # Log in to Discord
    email = driver.find_element("xpath", '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input')
    email.send_keys(DISCORD_EMAIL)
    time.sleep(1)
    password = driver.find_element("xpath", '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input')
    password.send_keys(DISCORD_PASS)
    password.send_keys(webdriver.Keys.ENTER)
    time.sleep(4)

    # Use to log into roblox accs, change display_names+passwords
    driver.find_element("xpath", '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/nav/div[2]/div/a[2]/div').click() # Open DMs chat
    # Scrolling to load
    document_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(2, 6):
        driver.execute_script(f"window.scrollTo({document_height}, {document_height / i});")
        time.sleep(1.5)
    data = driver.find_elements("css selector", ".embedFieldValue-nELq2s")
    time.sleep(4)
    no_of_accounts = int(len(data))
    users = [data[i].text for i in range(0, no_of_accounts, 3)]
    passwords = [data[i].text for i in range(1, no_of_accounts, 3)]
    print(users)
    print(passwords)
    # Can insert own list of desired display_names here
    display_names = ["Amber", "Ambrosia", "Amdis", "Celeste", "Dawn", "Drusilla", "Elena", "Elisabeta", "Katherine",
                     "Lenora", "Lilith", "Lucinda", "Miriam", "Jezebel", "Thana", "Victoria", "Alaric", "Blade",
                     "Damien", "Darren", "Drake", "Kieran", "Lazarus", "Louis", "Luther", "Orpheus", "Raul",
                     "Rodolfo", "Sebastien", "Serafino", "Silas", "Vladamir"]

    driver.get("https://www.roblox.com/my/account?nl=true#!/info")
    time.sleep(2)
    for i in range((no_of_accounts)):
        driver.find_element("xpath", '//*[@id="login-username"]').send_keys(users[i])
        password = driver.find_element("xpath", '//*[@id="login-password"]')
        password.send_keys(passwords[i])
        password.send_keys(webdriver.Keys.ENTER)
        time.sleep(15) # Human to solve
        # In case Human takes too long to solve and driver continues on, give 10 more secs. HURRY HUMAN!! 🧠
        try:
            driver.find_element("link text", 'I AGREE').click()  # I AGREE to terms of use changed
            time.sleep(1)
        except NoSuchElementException:
            time.sleep(10)
            driver.find_element("link text", 'I AGREE').click()  # I AGREE to terms of use changed
            time.sleep(1)
        driver.find_element("xpath", '//*[@id="settings-container"]/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/span[3]').click() # Display Name Change
        time.sleep(2)
        name = driver.find_element("xpath", '//*[@id="change-display-name-modal"]/form/div[1]/div/input')
        name.send_keys(webdriver.Keys.CONTROL + "a")
        name.send_keys(webdriver.Keys.DELETE)
        name.send_keys(f"{random.choice(display_names)}{random.randint(235,4199)}")
        time.sleep(1.5)
        name.send_keys(webdriver.Keys.ENTER)
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="settings-container"]/div[2]/div[2]/div/div[1]/div[3]/div/div[3]/span[4]').click() # Password Change
        time.sleep(1.5)
        driver.find_element("xpath", '//*[@id="old-password-text-box"]').send_keys(passwords[i])
        driver.find_element("xpath", '//*[@id="new-password-text-box"]').send_keys(RBLX_CHANGE_PASS_TO)
        time.sleep(1.5)
        driver.find_element("xpath", '//*[@id="confirm-password-text-box"]').send_keys(RBLX_CHANGE_PASS_TO)
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="confirm-password-text-box"]').send_keys(webdriver.Keys.ENTER)
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="rbx-body"]/div[1]/div/div/div/div[3]/button[2]').click() # OK
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="nav-settings"]').click() # Settings menu
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="settings-popover-menu"]/li[4]/a').click() # Log out
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="rbx-body"]/div[22]/div[2]/div/div/div[3]/div/button[2]').click()  # Skip, Log out anyway
        time.sleep(2.5)
        with open("rblx_accounts.txt", "a") as handle: handle.write(f"{users[i]} {RBLX_CHANGE_PASS_TO}\n")

