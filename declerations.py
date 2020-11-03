import pyautogui as pg
import time
from colorama import Fore
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

path = 'C:\\Users\\Guy Buky\\Desktop\\new_list.py'
COUNTRY_CODE = "+62"
INTERVAL = 0.2
COUNTRY = "Индонезия"  # Indonesia


def NameList():
    file = open("Names.csv", 'r')
    name_list = [n.rstrip().split(',') for n in file.readlines()]
    name_list.remove(name_list[0])  # delete first name
    file.close()
    return name_list


def ClickIfVisible(image):
    button = pg.locateCenterOnScreen(image, grayscale = True)
    if button is not None:
        pg.click(button)
        return True
    return False


class Sim:
    def __init__(self, ID, access_hash, phone, name):
        self.ID = ID
        self.access_hash = access_hash
        self.phone = phone
        self.name = name


def AddToFile(s: Sim):
    file = open(file = path, mode = 'a')
    file.write(str(s.ID) + ',' + s.access_hash + ',' + s.phone + ',' + s.name + '\n')
    file.close()


def ReturnToMainPage():
    ClickIfVisible('back.PNG')
    time.sleep(1)
    pg.click(x = 659, y = 367)
    time.sleep(INTERVAL)
    pg.press('backspace', presses = 30)


def GetPhoneAndCode():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:\\Users\\Guy Buky\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        driver = webdriver.Chrome(executable_path = "chromedriver.exe", options = options)
        driver.get("https://www.simsms.org/")
        driver.maximize_window()
        time.sleep(4)

        ## pressing Country button
        for country in driver.find_elements_by_tag_name('b'):
            if country.text == COUNTRY:
                country.click()
                break

        ## pressing the Telegram button
        titles = driver.find_elements_by_class_name(name = "title")
        for title in titles:
            if title.text == "Telegram":
                title.click()
                break

        button_list = driver.find_elements_by_id("get-phone")
        for button in button_list:
            if button.is_displayed():
                button.click()
                break

        ## retrieve phone number from simSMS
        time.sleep(5)
        phone_number = driver.find_element_by_xpath("//button[@title='Скопировать номер без кода страны']").text
        driver.minimize_window()

        # first, locate the mouse on the phone number text field
        # x,y coordinates change based on bluestack location and pc
        time.sleep(1)
        pg.click(x = 158, y = 366)
        time.sleep(INTERVAL)
        pg.typewrite(message = COUNTRY_CODE + '\t', interval = INTERVAL)
        pg.typewrite(message = phone_number + '\n', interval = INTERVAL)

        ## retrieving the code and finish signing up
        code = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//button[@title='Скопировать код из СМС']"))
        )
        code_text = code.text

        driver.quit()
        return COUNTRY_CODE + phone_number, code_text

    except TimeoutException:
        print(Fore.RED + "Code TIMED OUT! Trying again..")
        ReturnToMainPage()
        driver.quit()
        return None, None
