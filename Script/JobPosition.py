import pandas as pd
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By


class JobPosition:
    def __init__(self,
                 company: str,
                 position: str):
        self.company = company
        self.position = position

    @staticmethod
    def checkPositionApply(history: pd.DataFrame) -> bool:
        history = history.query("Workplace == @self.company and Position == @self.position")

        if (history.shape[0] == 0):
            return False
        else:
            return True

    def addDetails(self,
                   browser: webdriver):
        self.browser = browser
        self.size_area = browser.find_elements(By.XPATH, '//li[contains(@class, "jobs-unified-top-card")]/span')[1].text
        self.size_area = self.size_area.split(" · ")
        self.size_area[0] = self.size_area[0].replace(" employees", "").replace(",", " ")
        link = self.browser.current_url
        positionDesc = self.browser.find_element(By.XPATH,
                                                 '//article[contains(@class, "jobs-description__container")]').text


    def checkEasyApply(self) -> bool:
        self.apply_button = self.browser.find_element(By.XPATH,
                                            '//button[contains(@class, "jobs-apply-button artdeco-button artdeco-button")]')
        apply_type = self.apply_button.text

        if (apply_type == 'Apply'):
            self.easyApply = True
        else:
            self.easyApply = False

        return self.easyApply

    def apply(self):
        pass

    # TODO : add cover letter creation script
    def writeCover(self):
        pass