from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
#from func import readUserNPass
from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
username, password = readUserNPass()
position_name = "Data Scientist"
position_location = "European Union"



browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
browser.maximize_window()
browser.find_element("id", "username").send_keys(username)
browser.find_element("id", "password").send_keys(password)
browser.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
time.sleep(30)


base_url = "https://www.linkedin.com/jobs/search/?keywords="
link = base_url + position_name.replace(" ", "%20") + "&location=" + position_location.replace(" ", "%20")
browser.get(link)

previous = 0
names = browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')\
    .find_elements(By.XPATH, '//a[@tabindex="0"][contains(@class, "disabled ember-view")]')

while (previous < len(names)):
    previous = len(names)

    scrollable_element = browser.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div')
    browser.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scrollable_element)

    names = browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')\
        .find_elements(By.XPATH, '//a[@tabindex="0"][contains(@class, "disabled ember-view")]')

names = [n.text for n in names]

time.sleep(120)
#//*[@id="ember529"]
