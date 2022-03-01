from selenium import webdriver
import time
from selenium.common.exceptions import ElementClickInterceptedException

CHROME_DRIVER_PATH = "V96_chromedriver.exe"
SIMILAR_ACC = "chefsteps"
USER = "..."
PASS = "..."



class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(1.5)
        self.driver.find_element("name", "username").send_keys(USER)
        self.driver.find_element("name", "password").send_keys(PASS)
        time.sleep(1.5)
        self.driver.find_element("xpath", '//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(4)

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACC}/")
        time.sleep(1.5)
        self.driver.find_element("xpath", '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click() # on 'followers'
        time.sleep(1.5)
        followers_window = self.driver.find_element("class name", "isgrP") # 'followers' pop-up window
        # Scrolling to end in followers window
        last_result = None
        new_result = 0
        while last_result != new_result:
            last_result = new_result
            # arguments[0] = followers_window
            # Then we're using JS to "scroll the top of the pop-up window by the height of the pop-up window"
            new_result = self.driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight", followers_window)
            time.sleep(1.5)

    def follow(self):
        followers = self.driver.find_elements("class name", "sqdOP")
        for follower in followers:
            try:
                follower.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                time.sleep(1)
                self.driver.find_element("class name", "HoLwm").click() # Cancel
                time.sleep(1)

