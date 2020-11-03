from selenium import webdriver
from colorama import Fore
import traceback
import random
from declerations import NameList, ClickIfVisible, Sim, GetPhoneAndCode, INTERVAL
import time
import pyautogui as pg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""PNGs and coordinates change based on PC and bluestacks"""


NAMES = NameList()


def SignUp():
    try:
        phone, code = GetPhoneAndCode()
        while not code:  # if code times out, try again
            time.sleep(1)
            phone, code = GetPhoneAndCode()

        pg.click(x = 326, y = 531)
        time.sleep(0.5)
        pg.typewrite(code, interval = INTERVAL)

        # fill in name and sign up
        time.sleep(3)
        name = random.choice(NAMES)
        pg.typewrite(name[0] + ' ' + name[1] + '\n\n', interval = INTERVAL)
        time.sleep(1)
        ClickIfVisible('accept.PNG')

        # click on the 'Never' button
        time.sleep(1)
        ClickIfVisible('never.PNG')

        print(Fore.GREEN + f"Successfully created {name[0]} {name[1]}. Logging In...")
        return phone, name[0] + name[1]

    except:
        traceback.print_exc()
        exit(-1)


def Login(phone: str, name: str):
    try:
        # open my telegram
        mt = webdriver.Chrome(executable_path = 'chromedriver.exe')
        mt.get("https://my.telegram.org/auth/")

        # enter phone number in text field
        text_field_mt = WebDriverWait(mt, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        text_field_mt.send_keys(phone)
        text_field_mt.submit()
        mt.minimize_window()

        # retrieve login code message from Bluestacks
        time.sleep(1)
        pg.click(x = 350, y = 239)  # press telegram convo
        time.sleep(1)
        pg.mouseDown(x = 222, y = 763)
        time.sleep(1)
        pg.mouseUp()
        time.sleep(INTERVAL)
        ClickIfVisible('copy.PNG')  # copy the message

        # paste message in my telegram and keep only the code
        mt.maximize_window()
        time.sleep(4)
        pg.click(x = 942, y = 480)
        time.sleep(INTERVAL)
        pg.hotkey('ctrl', 'v')  # paste the message
        time.sleep(INTERVAL)
        pg.press('backspace', presses = 315)
        time.sleep(INTERVAL)
        pg.press('left', presses = 11)
        time.sleep(INTERVAL)
        pg.press('backspace', presses = 200)
        mt.find_element_by_xpath("//button[text()='Sign In']").click()

        # click on API development tools button
        time.sleep(3)
        mt.find_element_by_xpath("//a[text()='API development tools']").click()
        time.sleep(3)

        # fill in long and short title and go to id/hash page
        mt.find_element_by_id("app_title").send_keys("Testing simSMS")
        mt.find_element_by_id("app_shortname").send_keys("TESTING")
        mt.find_element_by_id("app_save_btn").click()
        time.sleep(2)
        while ClickIfVisible('error.PNG'):
            mt.find_element_by_id("app_save_btn").click()
            pg.moveTo(x=837, y=705)  # blocking the error icon
            time.sleep(2)

        # retrive ID and HASH combination
        time.sleep(5)
        ID = int(mt.find_elements_by_tag_name('span')[0].text)
        HASH = mt.find_elements_by_tag_name('span')[2].text

        # return the new sim object
        mt.quit()
        return Sim(ID, HASH, phone, name)

    except:
        traceback.print_exc()
        mt.quit()
        exit(0)


def NewAccount():
    # return to main page
    time.sleep(2)
    ClickIfVisible('back.PNG')

    # click on hamburger icon
    time.sleep(2)
    ClickIfVisible('hamburger.PNG')

    # click on the drop down menu icon if it's open
    time.sleep(2)
    ClickIfVisible('menu_icon.PNG')

    # click on settings
    time.sleep(2)
    ClickIfVisible('cog_wheel.PNG')

    # click on three dots and log out
    time.sleep(2)
    pg.scroll(-7000)  # scroll down to see the icon
    time.sleep(2)
    ClickIfVisible('dots.PNG')
    time.sleep(INTERVAL)
    pg.click()

    # click on new account
    time.sleep(2)
    ClickIfVisible('new_account.PNG')

    # clean up before new iteration
    time.sleep(2)
    pg.click(x = 755, y = 376)
    pg.press('backspace', presses = 50)
