import os
from time import sleep
from timeit import timeit
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
# options.add_argument("--headless")
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": r"C:\Users\ata.revisor\Desktop\Python Marcelo CCB\PDFs",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    },
)

driver = Chrome("chromedriver.exe", options=options)


driver.get("https://iccb.idtrust.com.br")


# login
login = driver.find_element_by_xpath('//*[@id="username"]')
password = driver.find_element_by_xpath('//*[@id="password"]')
login.send_keys("43476556816")
password.send_keys("92hs4oxi")
driver.find_element_by_xpath('//*[@id="bt-login"]').click()


wait = WebDriverWait(driver, 3)


# Consulta CCB
menu1 = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/form/div/ul/li[1]/a/span[2]")
    )
)
menu2 = driver.find_element_by_xpath('//*[@id="menuForm:j_idt17"]/ul/li[1]/ul/li[3]/a')

action = ActionChains(driver)
action.move_to_element(menu1).perform()
action.move_to_element(menu2).perform()

menu2.click()


# Form
# explict wait for datai to be found
datai = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt35_input"]'))
)
dataf = driver.find_element_by_xpath('//*[@id="form:j_idt37_input"]')
ccb = driver.find_element_by_xpath('//*[@id="form:j_idt41"]')
filterbt = driver.find_element_by_xpath('//*[@id="form:j_idt48"]')


def run(data, ccb_n):
    # test
    datai = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt35_input"]'))
    )
    dataf = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt37_input"]'))
    )
    ccb = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt41"]'))
    )
    filterbt = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form:j_idt48"]'))
    )

    ccb.clear()
    datai.clear()
    dataf.clear()
    datai.send_keys(f"{data} 00:00:00")
    dataf.send_keys(f"{data} 23:59:59")
    ccb.send_keys(ccb_n)
    filterbt.click()
    # explict wait for CCB to be found
    # Download
    sleep(2)
    try:
        pdf = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="form:tableCcbs:0:j_idt78"]')
            )
        )
        pdf.click()
    except BaseException:
        pdf = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="form:tableCcbs:0:j_idt78"]')
            )
        )
        pdf.click()


ccbs = None
dates = None
with open("C:\\Users\\ata.revisor\\Desktop\\Python Marcelo CCB\\CCBs.txt") as txt:
    ccbs = txt.read().split("\n")
with open("C:\\Users\\ata.revisor\\Desktop\\Python Marcelo CCB\\datas.txt") as txt:
    dates = txt.read().split("\n")
len(ccbs) == len(dates)


total = len(ccbs)
for x, (ccb_n, date) in enumerate(zip(ccbs, dates), 1):
    print(f"{x}/{total} Getting {ccb_n} - {date} ")
    run(date, ccb_n)


driver.quit()
