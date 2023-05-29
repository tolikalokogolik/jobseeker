import time

import pandas as pd
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Script.JobPosition import JobPosition
from Script.func import checkPositionApply

class LinkedIn:

    def __init__(self, history:pd.DataFrame):
        # TODO: implement proxy server
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.__readUserNPass__()

        self.browser.maximize_window()
        self.__logIn__()


    def __readUserNPass__(self,
                          filename: str = "private\linkedin.txt"):
        file1 = open(filename, 'r')
        Lines = file1.readlines()
        self.username = Lines[0]
        self.password = Lines[1]

    def __logIn__(self):
        """login into account written in 'private/linkedin.txt' file
            if needed, provides extra time to do account verification"""

        self.browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        self.browser.find_element("id", "username").send_keys(self.username)
        self.browser.find_element("id", "password").send_keys(self.password)
        self.browser.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
        time.sleep(30)
        # TODO: add two cases, if it asks for verification, wait for 30 seconds, and if not just proceed

    def locateBoard(self,
                    title:str="Data Scientist",
                    location:str="European Union"):
        """locates browser to job board based on location and job title striction"""

        self.jobTitle = title
        self.jobLocation = location
        self.onBorad = True
        base_url = "https://www.linkedin.com/jobs/search/?keywords="
        link = base_url + title.replace(" ", "%20") + "&location=" + location.replace(" ", "%20")
        self.browser.get(link)
        elements = self.browser.find_elements(By.XPATH,
                                         "//li[contains(@class,'artdeco-pagination__indicator artdeco-pagination__indicator')]")
        self.pagesLimit = int(elements[len(elements)-1].text)

    def whichPage(self) -> int:
        page = self.browser.find_element(By.XPATH, f"//button[@aria-current='true']").text
        return int(page)

    def changePage(self, page: int):
        """Changes the page of the jobs board"""

        base_url = "https://www.linkedin.com/jobs/search/?keywords="
        link = base_url + self.jobTitle.replace(" ", "%20") + "&location=" + self.jobLocation.replace(" ", "%20")
        if (page > self.pagesLimit or page < 1):
            print(f"There is no page number {page}, the limit is in range [1,{self.pagesLimit}]")
        else:
            link = link + f"&start={(page-1)*25}"
            self.browser.get(link)



    def __readDataFromPage__(self, history:pd.DataFrame):
        """Reading all the data from current page
            also removes positions where already applied"""

        self.__loadAllPage__() #load all page
        ul = self.browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
        lis = ul.find_elements(By.XPATH, "li[contains(@class, 'jobs-search-results__list-item occludable-update')]")

        # going through job ads
        for li in lis:
            li.click()

            position = JobPosition(li.find_element(By.XPATH, '*//span[contains(@class, "job-card-container__primary-")]').text,
                                   li.find_element(By.XPATH, '*//a[@tabindex="0"][contains(@class, "disabled ember-view")]').text


            # collect the data and apply only if didn't apply before
            if (~position.checkPositionApply(history)):
                position.addDetails(self.browser)


    def __loadAllPage__(self):
        """Load all the pages for further data ingestion"""
        previous = 0
        names = self.browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container') \
            .find_elements(By.XPATH, '//a[@tabindex="0"][contains(@class, "disabled ember-view")]')

        while (previous < len(names)):
            previous = len(names)

            scrollable_element = self.browser.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div')
            self.browser.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scrollable_element)

            names = self.browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container') \
                .find_elements(By.XPATH, '//a[@tabindex="0"][contains(@class, "disabled ember-view")]')

