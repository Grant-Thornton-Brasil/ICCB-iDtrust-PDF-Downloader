import os
import logging
import argparse
from tqdm import tqdm
from time import sleep
from timeit import timeit
from decouple import config
from multiprocessing import Process
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class CCB_Robot:
    def __init__(self):
        # LOAD STRINGS FROM SETTINGS.INI
        self.DOWNLOAD_PATH = config("DOWNLOAD_PATH")
        self.URL = config("URL")
        self.USER = config("USER")
        self.PASSWORD = config("PASSWORD")
        self.LOGIN_XPATH = config("LOGIN_XPATH")
        self.PASSWORD_XPATH = config("PASSWORD_XPATH")
        self.LOGIN_BT_XPATH = config("LOGIN_BT_XPATH")
        self.MENU1_XPATH = config("MENU1_XPATH")
        self.MENU2_XPATH = config("MENU2_XPATH")
        self.DATA_INICIAL = config("DATA_INICIAL")
        self.DATA_FINAL = config("DATA_FINAL")
        self.CCB_FIELD = config("CCB_FIELD")
        self.SEARCH_BT = config("SEARCH_BT")
        self.DOWNLOAD_PDF_BT = config("DOWNLOAD_PDF_BT")
        # LOG LEVEL
        LOGGER.setLevel(logging.WARNING)
        # OPTIONS
        options = Options()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.DOWNLOAD_PATH,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
            },
        )
        # INIT
        self.lines = []
        self.driver = Chrome("chromedriver.exe", options=options)
        self.wait = WebDriverWait(self.driver, 0.75)
        # LOG INIT
        os.system("cls")
        print(f"Object inicialized with in queue!")
    
    def add_to_queue(self,line):
        self.lines.append(line.strip().split(";"))
        

    def login(self):
        self.driver.get(self.URL)
        login = self.driver.find_element_by_xpath(self.LOGIN_XPATH)
        password = self.driver.find_element_by_xpath(self.PASSWORD_XPATH)
        login.send_keys(self.USER)
        password.send_keys(self.PASSWORD)
        self.driver.find_element_by_xpath(self.LOGIN_BT_XPATH).click()

    def navigate_ccb_query_page(self):
        try:
            menu1 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, self.MENU1_XPATH))
            )
            menu2 = self.driver.find_element_by_xpath(self.MENU2_XPATH)
            action = ActionChains(self.driver)
            action.move_to_element(menu1).perform()
            action.move_to_element(menu2).perform()
            menu2.click()
        except:
            self.navigate_ccb_query_page()

    def search_n_download(self):
        total = len(self.lines)
        if total > 0:
            print(f"Downloading {total} PDFs files...")
            for ccb_number, date in tqdm(self.lines):
                try:
                    inicial_date = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, self.DATA_INICIAL))
                    )
                    final_date = self.driver.find_element_by_xpath(self.DATA_FINAL)
                    ccb_field = self.driver.find_element_by_xpath(self.CCB_FIELD)
                    search_bt = self.driver.find_element_by_xpath(self.SEARCH_BT)
                    # CLEAR FIELDS
                    inicial_date.clear()
                    final_date.clear()
                    ccb_field.clear()
                    # FIll INFO AND GO
                    inicial_date.send_keys(date + " 00:00:00")
                    final_date.send_keys(date + " 23:59:59")
                    ccb_field.send_keys(ccb_number)
                    search_bt.click()
                    # sleep(0.2)
                    pdf = self.wait.until(
                        EC.visibility_of_element_located((By.XPATH, self.DOWNLOAD_PDF_BT))
                    )
                    pdf.click()
                except:
                    pass
    
    def run(self):
        self.login()
        self.navigate_ccb_query_page()
        self.search_n_download()


if __name__ == "__main__":
    robot = CCB_Robot()
    with open("download_list_1.csv") as csv:
        for line in csv.readlines():
            robot.add_to_queue(line)
    robot.run()





        


            
