from selenium import webdriver
import pandas
import time

MY_ISP = "StarHub-Ltd-NGNBN-Services"

class SpeedCheck:
    def __init__(self, CHROME_DRIVER_PATH):
        self.MY_ISP_avg_dl_speed = 0
        self.MY_ISP_avg_ul_speed = 0
        self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
        self.get_data()


    def get_data(self):
        self.driver.get("http://www.speedtest.com.sg/latest_result_starhub.php")
        time.sleep(2)
        # Scrolling to load
        document_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(6, 0, -1):
            self.driver.execute_script(f"window.scrollTo(0, {document_height / i});")
            time.sleep(1.25)

        data = self.driver.find_elements("xpath", "//*[name()='td' and @valign='top']")  # All columns
        time.sleep(2)

        # isps created separately due to some data eg. 116.893.242.254\nStarHub Cable Vision Ltd\nSG & StarHub Cable Vision Ltd\nSG
        isps = []
        for i in range(1, len(data), 5):
            split_items = data[i].text.split("\n")
            first_part = split_items[0]
            second_part = split_items[1]
            # 15 is the magic number that excludes ip addresses in above eg.
            if len(first_part) > 15: isps.append(first_part)
            elif len(second_part) > 15: isps.append(second_part)
        pandata = {
            "ISP": isps,
            "Download(Mb/s)": [float(data[i].text.split()[0]) for i in range(2, len(data), 5)],
            "Upload(Mb/s)": [float(data[i].text.split()[0]) for i in range(3, len(data), 5)],
            "OS": [data[i].text.split()[0].split(";")[0].split("(")[1] for i in range(4, len(data), 5)],
        }
        pandas.DataFrame(pandata).to_csv("ISP_speeds.csv")
        pandata = pandas.read_csv("ISP_speeds.csv")

        # Fair comparison between same ISPs and OS (mobile usually has lower dl/up speeds)
        MY_ISP_DL_speeds = [row["Download(Mb/s)"] for index, row in pandata.iterrows() if row["ISP"] == MY_ISP and row["OS"] in ["Windows", "Linux", "Macintosh"]]
        self.MY_ISP_avg_dl_speed = sum(MY_ISP_DL_speeds) / len(MY_ISP_DL_speeds)
        MY_ISP_UL_speeds = [row["Upload(Mb/s)"] for index, row in pandata.iterrows() if row["ISP"] == MY_ISP and row["OS"] in ["Windows", "Linux", "Macintosh"]]
        self.MY_ISP_avg_ul_speed = sum(MY_ISP_UL_speeds) / len(MY_ISP_UL_speeds)

        self.driver.quit()
