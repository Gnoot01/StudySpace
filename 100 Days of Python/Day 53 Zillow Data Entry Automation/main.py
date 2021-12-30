from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

CHROME_DRIVER_PATH = "V96_chromedriver.exe"
HEADERS = {
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
}

# I have no idea why only 9 results are returned, when clicking on the link shows 40 results in 1 page... This is why I prefer fuller control with Selenium.
response = requests.get(
    url="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
    headers=HEADERS)
content = response.text
soup = BeautifulSoup(content, "html.parser")
print(soup.prettify())
addresses = [address.getText() for address in soup.find_all(name="address", class_="list-card-addr")]
prices = [price.getText().split("/")[0].split("+")[0] for price in soup.find_all(name="div", class_="list-card-price")]
link_elements = soup.select(selector=".list-card-info a")
links = []
for link_element in link_elements:
    href = link_element.get("href")
    if "http" not in href: links.append(f"https://www.zillow.com{href}")
    else: links.append(href)


driver = webdriver.Chrome(service=webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_PATH))
for i in range(len(addresses)):
    driver.get("https://forms.gle/XcKMg4WHrYG5T5Ki6")
    time.sleep(1)
    driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(addresses[i])
    driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(prices[i])
    driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(links[i])
    driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click() # Submit
    time.sleep(1.5)
