import os
from time import sleep
from timeit import timeit
from decouple import config
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class CCB_Robot:

    def __init__(self,**kwargs):
        self.download_path = config("DOWNLOAD_PATH")
        options = Options()
        # options.add_argument("--headless")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": 
                    self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
            },
        )
        try:
            self.driver = Chrome("chromedriver.exe", options=options)
        except:
            self.driver = Chrome(kwargs.get("drive"), options=options)
        self.wait = WebDriverWait(self.driver,5)
        # LOG INIT
        print("Driver Inicialized")
                            

    def login(self):
        USER = config("USER")
        PASSWORD = config("PASSWORD")

        LOGIN_XPATH = config("LOGIN_XPATH")
        PASSWORD_XPATH = config("PASSWORD_XPATH")
        LOGIN_BT_XPATH = config("LOGIN_BT_XPATH")
        URL = config("URL")
        self.driver.get(URL)

        login = self.driver.find_element_by_xpath(LOGIN_XPATH)
        password = self.driver.find_element_by_xpath(PASSWORD_XPATH)
        login.send_keys(USER)
        password.send_keys(PASSWORD)
        self.driver.find_element_by_xpath(LOGIN_BT_XPATH).click()
        
    
    def navigate_ccb_query_page(self):
        MENU1_XPATH = config("MENU1_XPATH")
        MENU2_XPATH = config("MENU2_XPATH")

        menu1 = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,MENU1_XPATH)
                )
        )
        menu2 = self.driver.find_element_by_xpath(MENU2_XPATH)
        action = ActionChains(self.driver)
        action.move_to_element(menu1).perform()
        action.move_to_element(menu2).perform()
        menu2.click()
