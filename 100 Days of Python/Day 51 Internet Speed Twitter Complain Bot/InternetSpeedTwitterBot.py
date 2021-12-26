from selenium import webdriver
import time

TWITTER_EMAIL = ...
TWITTER_USER = ...
TWITTER_PASS = ...

class InternetSpeedTwitterBot:
    def __init__(self, CHROME_DRIVER_PATH):
        self.current_dl_speed = 0
        self.current_ul_speed = 0
        self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))

    def check_current_dlul_speeds(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(2)
        # Change Server to NewMedia Express (where we get our avg speed data from) to compare fairly with
        self.driver.find_element("css selector", ".result-area-connection .btn-server-select").click()
        time.sleep(1.5)
        # Since data of speeds came from NewMedia Express, made sense to use the same host
        self.driver.find_element("class name", "input-button-input").send_keys("NewMedia Express")
        time.sleep(1.5)
        self.driver.find_element("xpath", '//*[@id="find-servers"]/div/div[3]/div/div/ul/li/a').click()
        time.sleep(1.5)
        # GO
        self.driver.find_element("xpath", '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]').click()
        time.sleep(50)
        self.current_dl_speed = float(self.driver.find_element("xpath", '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
        self.current_ul_speed = float(self.driver.find_element("xpath", '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text)
        time.sleep(4)

    def tweet_at_provider(self, my_ISP_avg_dl_speed: float, my_ISP_avg_ul_speed: float):
        self.driver.get("https://twitter.com/login")
        time.sleep(3)
        user = self.driver.find_element("css selector", '.r-13qz1uu input')
        user.send_keys(TWITTER_EMAIL)
        user.send_keys(webdriver.Keys.ENTER)
        time.sleep(2)
        # Because twitter has anti-bot behaviour whereby apparently if you only always input email, it asks username after...
        if self.driver.find_element("css selector", ".r-vrz42v span").text == "Enter your phone number or username":
            reenter = self.driver.find_element("css selector", '.r-13qz1uu input')
            reenter.send_keys(TWITTER_USER)
            reenter.send_keys(webdriver.Keys.ENTER)
            time.sleep(2)
            password = self.driver.find_elements("css selector", '.r-13qz1uu input')[1]
            password.send_keys(TWITTER_PASS)
            password.send_keys(webdriver.Keys.ENTER)
            time.sleep(2)
        else:
            password = self.driver.find_elements("css selector", '.r-13qz1uu input')[1]
            password.send_keys(TWITTER_PASS)
            password.send_keys(webdriver.Keys.ENTER)
            time.sleep(2)

        self.driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a').click()
        time.sleep(2)
        self.driver.find_element("class name", "public-DraftStyleDefault-block").send_keys(
            f"Hey @ Internet Provider, why is my internet speed {self.current_dl_speed}down/{self.current_ul_speed}up when I pay for {my_ISP_avg_dl_speed}down/{my_ISP_avg_ul_speed}up?")
        self.driver.find_element("xpath", '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]').click()
