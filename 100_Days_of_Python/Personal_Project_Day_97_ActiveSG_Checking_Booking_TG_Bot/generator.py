import os
import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Cannot dynamically gen activity ids as not found using BeautifulSoup, and also cannot implement Selenium
ACTIVITY_IDS = {"Badminton": 18, "Basketball": 468, "Floorball": 530, "Flying Disc": 561, "Futsal": 464, "Gateball": 89,
                "Gym": 1031, "Hockey": 102, "Hockey (Night)": 907, "Lawn Bowl": 113, "Netball": 522, "Open Air Fitness Corner 2021": 1033,
                "Organised Programme": 1035, "Outdoor": 1032, "Petanque": 149, "Pickleball": 153, "Sepak Takraw": 564,
                "Soccer": 207, "Soccer (Night)": 908, "Squash": 233, "Street soccer": 244, "Swim": 1030, "Table Tennis": 270,
                "Tennis": 284, "Tennis Wall": 789, "Volleyball": 293}

# Need to get FIRST_AVAIL_VENUE_ID to obtain all_avail_venue_ids, due to same issue above ^. Doesn't have to be FIRST
# available venue_id, can be any, as long as can access booking slots page. Some are None, as no working venue sites are found
FIRST_AVAIL_VENUE_IDS = {"Badminton": 292, "Basketball": 310, "Floorball": None, "Flying Disc": None, "Futsal": 1039,
                         "Gateball": None, "Gym": 1016, "Hockey": 1043, "Hockey (Night)": 1043, "Lawn Bowl": 583,
                         "Netball": 208, "Open Air Fitness Corner 2021": None, "Organised Programme": 1119, "Outdoor": 1083,
                         "Petanque": 197, "Pickleball": 296, "Sepak Takraw": None, "Soccer": 540, "Soccer (Night)": 255,
                         "Squash": 294, "Street soccer": None, "Swim": 124, "Table Tennis": 292, "Tennis": 150,
                         "Tennis Wall": 300, "Volleyball": 310}

TIME_SLOTS_NUM = {"Badminton": 15, "Basketball": 15, "Floorball": None, "Flying Disc": None, "Futsal": 15,
                  "Gateball": None, "Gym": 8, "Hockey": 12, "Hockey (Night)": 3, "Lawn Bowl": 15,
                  "Netball": 15, "Open Air Fitness Corner 2021": None, "Organised Programme": 10, "Outdoor": 7,
                  "Petanque": 7, "Pickleball": 15, "Sepak Takraw": None, "Soccer": 6, "Soccer (Night)": 1,
                  "Squash": 15, "Street soccer": None, "Swim": 11, "Table Tennis": 15, "Tennis": 15,
                  "Tennis Wall": 15, "Volleyball": 15}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
           "Accept-Language": "en-US,en;q=0.9",
           "Accept-Encoding": "gzip, deflate"}

CHROME_DRIVER_PATH = r"C:\Users\Andrew\Desktop\Dev Me\Python\V96_chromedriver.exe"
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


def gen_all_activities() -> list:
    """Generates all activity names"""
    return [activity.lower() for activity in ACTIVITY_IDS.keys()]


def get_time_from(date: str = None) -> int and str:
    """time_from in url calculates seconds from 1 Jan 1970 00:00:00 UTC. Hence, this converts a date to SGT(UTC+8)"""
    if date is None: date = datetime.datetime.now().strftime("%d %m %Y")
    date_split = date.split(" ")
    to_rtn1, to_rtn2 = (int(str(datetime.datetime(int(date_split[2]), int(date_split[1]), int(date_split[0])) - datetime.datetime(1970, 1, 1)).split(" ")[0]) * 24 * 60 * 60) - 28800, date
    return to_rtn1, to_rtn2


def cvt_date_to_day(date: str) -> str:
    """Converts a date to the day of the week, by datetime"""
    return datetime.datetime.strptime(date, "%d %m %Y").strftime("%a")


def __gen_day_capacity(start: int, end: int, day_capacity_data: list) -> str:
    """Formats into time: capacity%"""
    result = ""
    for i in range(start, end - 1):
        if i < 10:
            result += f"*0{i}AM*: {'{:.1f}'.format(day_capacity_data[i])}% | "
        elif i < 12:
            result += f"*{i}AM*: {'{:.1f}'.format(day_capacity_data[i])}% | "
        elif i == 12:
            result += f"*{i}PM*: {'{:.1f}'.format(day_capacity_data[i])}% | "
        else:
            result += f"*0{i % 12}PM*: {'{:.1f}'.format(day_capacity_data[i])}% | "
    result += f"*0{(end - 1) % 12}PM*: {'{:.1f}'.format(day_capacity_data[end - 1])}%"
    return result


def gen_capacity(venue: str, date: str) -> str:
    """Requests ActiveSG GymTracker Website for hourly capacity data of the week"""
    day_capacity_data = []
    day_capacity = "No capacity data found"

    # Gymtracker 6 = Sunday, Datetime 0 = Sunday [SUCH A PITA WHY DO THEY NEED TO BE DIFF!!! >:(]
    day_of_week = int(datetime.datetime.strptime(date, "%d %m %Y").strftime("%w")) - 1
    if day_of_week == -1: day_of_week = 6

    capacity_data = requests.get("https://gym-tracker.data.gov.sg/data/gym-formatted-data.json").json()
    for key in capacity_data.keys():
        # Tampines, Sengkang, Woodlands, Yishun, Clementi, Bishan, Hougang
        if key == venue.lower():
            day_capacity_data = capacity_data.get(key).get("weekly_data")[day_of_week]
            break
        # Jurong East, Jurong West, Toa Payoh, Bukit Gombak, Pasir ris
        elif key == venue.lower().replace(" ", "_"):
            day_capacity_data = capacity_data.get(key).get("weekly_data")[day_of_week]
            break
    # Heartbeat @ Bedok, Yio Chu Kang, Choa Chu Kang Level 3 (Free weights), Choa Chu Kang Level 4 (Stack weights)
    if len(day_capacity_data) == 0:
        stragglers = ["Heartbeat @ Bedok", "Yio Chu Kang", "Choa Chu Kang Level 3 (Free weights)", "Choa Chu Kang Level 4 (Stack weights)"]
        corresponding = ["bedok", "yck", "cck", "cck"]
        if venue in stragglers:
            day_capacity_data = capacity_data.get(corresponding[stragglers.index(venue)]).get("weekly_data")[day_of_week]
        else:
            return day_capacity

    # Mon,Wed,Fri: 7am-10pm (7:22) | Tues,Thurs: 9am-10pm (9:22) | Sat,Sun: 9am-8pm (9:20)
    if day_of_week in [0, 2, 4]: day_capacity = __gen_day_capacity(7, 22, day_capacity_data)
    elif day_of_week in [1, 3]: day_capacity = __gen_day_capacity(9, 22, day_capacity_data)
    else: day_capacity = __gen_day_capacity(9, 20, day_capacity_data)

    return day_capacity

    # Not sure if this capacity data is updated... But if it's not, I have a solution. In fact this can grab capacity for all venues and activities, not just gym

    # Basically driver.get("https://www.google.com/maps"), driver.find_element("xpath", "SEARCH_BAR"), .send_keys(venue/venue+"ActiveSG Gym"),
    # day = cvt_date_to_day(date)
    # if driver.find_element("xpath", "DROPDOWN_DAYS").text.split("days")[0] == day:
    #   hourly_data = driver.find_elements("css selector", ".... div")[3:18] # 7am-9pm
    #   day_capacity = gen_data_capacity(hourly_data)
    # else:
    #   driver.find_element("xpath", ">_BTN").click()
    #   gen_capacity(venue, date) # RECURSE
    # return day_capacity


class Generator:
    # default None allows Generator() without any arguments, esp if just want to use static methods above
    def __init__(self, activity: str = None, date: str = None) -> None:
        """Instantiates a Generator class object"""
        if date is not None:
            # Validates the date (Normal datetime's validation + assertion validation)
            assert datetime.datetime.strptime(f"{date} 23 59 59 999999", "%d %m %Y %H %M %S %f") >= datetime.datetime.now(), "Date input is in the past"
        self.activity_id = ACTIVITY_IDS.get(activity)
        self.first_avail_venue_id = FIRST_AVAIL_VENUE_IDS.get(activity)
        self.time_from, self.date = get_time_from(date)
        self.time_slots_num = TIME_SLOTS_NUM.get(activity)
        self.all_activities = gen_all_activities()

######################################## HELPER FUNCTIONS ##############################################################
    def __gen_venues(self) -> list:
        """Scrapes website for list of venues"""
        url = f"https://members.myactivesg.com/facilities/view/activity/{self.activity_id}/venue/{self.first_avail_venue_id}?time_from={self.time_from}"
        response = requests.get(url=url, headers=HEADERS)
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        return soup.select(selector="#facVenueSelection option")[1:]

    def __gen_gym_venue_ids(self) -> dict:
        """Generates {gym_venue: gym_venue_id}, formatted specifically nicely for gym"""
        options = self.__gen_venues()
        gym_venue_ids = {}
        for option in options:
            venue = ""
            if "ActiveSG" in option.text:
                split_text = option.text.split("ActiveSG")
                words = split_text[1].strip().split(" ")
                if len(words) > 1:
                    # ActiveSG Gym at Fernvale Square -> ["", " Gym at Fernvale Square"] -> ["Gym", "at", "Fernvale", "Square"] -> Fernvale Square
                    if "at" in words:
                        for word in words[words.index("at") + 1:]: venue += word + " "
                    # ActiveSG Hockey Village Gym @ Boon Lay -> ["", " Hockey Village Gym @ Boon Lay"] -> ["Hockey", "Village", "Gym", "@", "Boon", "Lay"] -> Boon Lay
                    elif "@" in words:
                        for word in words[words.index("@") + 1:]: venue += word + " "
                    # Choa Chu Kang ActiveSG Gym Level 3 (Free weights) -> ... -> Choa Chu Kang Level 3 (Free weights)
                    # Choa Chu Kang ActiveSG Gym Level 4 (Stack weights) -> ... -> Choa Chu Kang Level 4 (Stack weights)
                    elif "Level" in words:
                        venue = split_text[0]
                        for word in words[words.index("Level"):]: venue += word + " "
                # Tampines ActiveSG Gym -> ["Tampines ", " Gym"] -> XX -> Tampines
                else: venue = split_text[0]
            # Jurong Lake Gardens Gym -> Jurong Lake Gardens
            else: venue = option.text.replace("Gym", "").strip()
            venue = venue.strip()
            gym_venue_ids[venue] = int(option.attrs.get("value"))
        return gym_venue_ids
        # venue_ids = {'Ang Mo Kio CC': 1016, 'Fernvale Square': 048, 'Toa Payoh West CC': 1049, 'Boon Lay': 1037,
        #              'Bishan': 137, 'Bukit Batok': 1040, 'Bukit Gombak': 45, 'Choa Chu Kang Level 3 (Free weights)': 154,
        #              'Choa Chu Kang Level 4 (Stack weights)': 1130, 'Clementi': 160, 'Enabling Village': 849, 'Heartbeat @ Bedok': 896,
        #              'Hougang': 185, 'Jalan Besar': 967, 'Jurong East': 196, 'Jurong Lake Gardens': 1012, 'Jurong West': 200,
        #              'Kallang Basin': 1110, 'Pasir Ris': 544, 'Sengkang': 239, 'Senja Cashew': 1089, 'Silver Circle': 886,
        #              'Tampines': 900, 'Toa Payoh': 268, 'Woodlands': 274, 'Yio Chu Kang': 279, 'Yishun': 284}

    def __get_proper_name(self) -> str:
        """Formats into proper area names"""
        # Basketball/Volleyball (Section A)
        if self.activity_id in [468, 293]: return "Section "
        # Futsal/Hockey/Hockey (Night) (Pitch 1)
        elif self.activity_id in [464, 102, 907]: return "Pitch "
        # Soccer/Soccer (Night) (5-a-side field 1)
        elif self.activity_id in [207, 908]: return "5-a-side field 0"
        # Lawn Bowl (Lane 1)
        elif self.activity_id == 113: return "Lane "
        # Pentanque(Pcourt 1)
        elif self.activity_id == 149: return "Pcourt "
        # Table Tennis(Table 1)
        elif self.activity_id == 270: return "Table "
        # Tennis Wall(Wall 1)
        elif self.activity_id == 789: return "Wall "
        # Badminton/Netball/Organised Programme/Outdoor/Pickleball/Squash/Tennis(Court 1)
        return "Court "

    def __format_to_str(self, venue: str, avail_slots: dict) -> str:
        """Formats final Capacity + Availability data"""
        result = ""
        if self.activity_id in [1031, 1030]:
            for datee in avail_slots.keys():
                result += f"*{datee} ({cvt_date_to_day(datee)})*\n"
                data = avail_slots.get(datee)
                # If "No available slots found!"
                if type(data) is str: result += data + "\n"
                else:
                    if self.activity_id == 1031:
                        result += f"\[Capacity]:\n{gen_capacity(venue, datee)}\n"
                    result += f"\[Availability]:\n"
                    for timing in data[:-1]:
                        timing_split = timing.split(" ")
                        shorter_timing = timing_split[0].split(":")[0] + timing_split[1]
                        result += f'*{shorter_timing}*: {" ".join(timing_split[2:])} | '
                    last_timing_split = data[-1].split(" ")
                    shorter_timing = last_timing_split[0].split(":")[0] + last_timing_split[1]
                    result += f'*{shorter_timing}*: {" ".join(last_timing_split[2:])}\n'
                result += "-----------------------------------------------------------\n\n"
            # Don't want GymTracker link showing if "Swim" or "No available slots found!" to not confuse users
            if self.activity_id == 1031 and type(data) is not str:
                result += "Capacity Data Courtesy of [GymTracker](https://gym-tracker.data.gov.sg/)\n"
            return result

        for datee in avail_slots.keys():
            result += f"*{datee} ({cvt_date_to_day(datee)})*\n"
            areas = avail_slots.get(datee)
            # '11 02 2022', '12 02 2022'
            for area in areas.keys():
                area_data = areas.get(area)
                # If "No available slots found!"
                if type(area_data) is str: result += f"\[{area}]\n{area_data}\n"
                else:
                    result += f"\[{area}]\n"
                    for timing in area_data[:-1]:
                        result += f"{timing} | "
                    result += f"{area_data[-1]}\n"
            result += "-----------------------------------------------------------\n\n"
        return result

    ########################################################################################################################
    def gen_all_avail_venue_ids(self) -> dict:
        """Generates {venue: venue_id} data"""
        if self.activity_id == 1031: return self.__gen_gym_venue_ids()
        venues = self.__gen_venues()
        venue_ids = [int(venue.attrs.get("value")) for venue in venues]
        # I don't know why School and College Halls are displayed if they cannot be booked, but this is to filter them out
        avail_venues = [venue for venue in venues if "School" not in venue.text and "College" not in venue.text]
        # Edge case for Table Tennis
        if self.activity_id == 270: avail_venues = [venue for venue in venues if "Area" not in venue.text]
        return {avail_venue.text: venue_ids[venues.index(avail_venue)] for avail_venue in avail_venues}

    def gen_availability(self, venue: str, days_num: int = 0) -> str and list:
        """Generates available timeslots and dates chosen"""
        chrome_options = webdriver.chrome.options.Options()
        # Headless mode faster on average, due to not having a UI and hence loading times (also less annoying)
        # Must put specify arg window-size, as otherwise, sometimes uses mobile-size, and hence DOM of page is different from real browser
        # If cannot locate/errors with headless mode, but works without, use driver.get_screenshot_as_file("screenshot.png") at points to see what's really happening in headless mode
        # Eg. if blank page on ss, might be due to invalid SSL certificate, fix: '--ignore-certificate-errors' + '--allow-running-insecure-content'
        # Eg. or website blocks headless mode, fix: 'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36"'
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH), chrome_options=chrome_options)
        driver.get("https://members.myactivesg.com/auth")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="email"]'))).send_keys(EMAIL)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="password"]'))).send_keys(PASSWORD)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(("xpath", '//*[@id="btn-submit-login"]'))).click()

        avail_slots = {}
        venue_id = self.gen_all_avail_venue_ids().get(venue)
        # No need for try & except 1. SyntaxError due to incorrect format of date, as Filters.regex handles it in main.py for DATE
        days = [" ".join(str(datetime.datetime.strptime(self.date, "%d %m %Y") + datetime.timedelta(days=i)).split(" ")[0].split("-")[::-1]) for i in range(days_num+1)]
        if self.activity_id in [1031, 1030]:
            assert 0 <= days_num <= 3, "Only 3 days into the future allowed!"
            # Single Areas indicating (slots) left [Gym, Swim]
            for day in days:
                driver.get(f"https://members.myactivesg.com/facilities/view/activity/{self.activity_id}/venue/{venue_id}?time_from={self.time_from}")
                all_slots = driver.find_elements("css selector", ".timeslot-grid div")
                avail_slots[day] = [slot.text for slot in all_slots if slot.find_element("tag name", "input").get_attribute("id")]
                if len(avail_slots[day]) == 0: avail_slots[day] = "No available slots found!"
                self.time_from += 86400
        else:
            assert 0 <= days_num <= 15, "Only 15 days into the future allowed!"
            name = self.__get_proper_name()
            # Multiple Areas (not indicating slots left) [Everything else]
            for day in days:
                avail_slots_on_day = {}
                driver.get(f"https://members.myactivesg.com/facilities/view/activity/{self.activity_id}/venue/{venue_id}?time_from={self.time_from}")
                all_slots = driver.find_elements("css selector", ".timeslot-grid div")
                # 10 is the max no. of areas for any activity. If there isn't 10 areas, will simply give IndexError & pass over
                for area_num in range(10):
                    key = f"{name}{area_num + 1}"
                    if self.activity_id in [468, 293]: key = f"{name}{chr(area_num + 65)}"
                    try:
                        # Eg. For 15 slot areas: Court 1:[0-14]/[0-15), Court 2:[15-29], Court 3:[30-44], ...
                        slots = all_slots[area_num * self.time_slots_num: ((area_num + 1) * self.time_slots_num)]
                        if len(slots) == 0: break
                        avail_slots_on_day[key] = [slot.text for slot in slots if slot.find_element("tag name", "input").get_attribute("id")]
                        if len(avail_slots_on_day[key]) == 0:
                            avail_slots_on_day[key] = "No available slots found"
                    except IndexError:
                        pass
                if len(avail_slots_on_day) == 0: break
                avail_slots[day] = avail_slots_on_day
                self.time_from += 86400

        driver.quit()
        return self.__format_to_str(venue, avail_slots), days








