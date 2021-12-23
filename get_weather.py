"""
dependency
pip install beautifulsoup4
pip install selenium
pip install webdriver-manager
"""
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

temperature_keywords = {"氣溫", "溫度", "查詢溫度", "查詢氣溫", "目前溫度", "目前氣溫"}
weather_keywords = {"天氣", "氣象", "查詢天氣", "查詢氣象", "目前天氣"}
cities = {"基隆","台北","臺北",	"新北", "桃園", "新竹", "苗栗", 
"台中", "臺中", "彰化", "南投", "雲林"
"嘉義", "台南", "臺南", "高雄", "屏東", 
"宜蘭", "台東", "臺東", "花蓮",
"澎湖", "金門", "連江"}
other_interpretations = {"台北":"臺北", "台中":"臺中", "台南":"臺南", "台東":"臺東"}

def get_website():
    #get website info
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.cwb.gov.tw/V8/C/W/OBS_Map.html")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup

def get_weather(city):
    #get weather info
    soup = get_website()
    city_name = city
    full_name = "請點此進入 " + city_name + " 觀測資訊"
    cities_info = soup.find("ol",id="town")
    city_info = cities_info.find("a", title = full_name)
    weather = city_info.find("span", class_="weather").img['alt']
    return weather

def get_temperature(city):
    #get temperature info
    soup = get_website()
    city_name = city
    full_name = "請點此進入 " + city_name + " 觀測資訊"
    cities_info = soup.find("ol",id="town")
    city_info = cities_info.find("a", title = full_name)
    temperatue = city_info.find("span", class_="tem-C is-active").string
    return temperatue