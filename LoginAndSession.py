from telethon.sync import TelegramClient
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui as pg
from colorama import Fore
import time
import traceback

INTERVAL = 1
MESSAGE_PATH = 'C:\\Users\\Guy Buky\\Desktop\\code.txt'
CARDS_PATH = 'C:\\Users\\Guy Buky\\Desktop\\new_list.py'


class Sim:
    def __init__(self, ID, access_hash, phone, name):
        self.ID = ID
        self.access_hash = access_hash
        self.phone = phone
        self.name = name


def AddToFile(s: Sim):
    file = open(file = CARDS_PATH, mode = 'a')
    file.write(str(s.ID) + ',' + s.access_hash + ',' + s.phone + ',' + s.name + '\n')
    file.close()


def ClickIfVisible(image):
    button = pg.locateCenterOnScreen(image, grayscale = True)
    if button is not None:
        pg.click(button)
        return True
    return False


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
        time.sleep(0.5)
        ClickIfVisible('copy.PNG')  # copy the message

        # paste message in my telegram and keep only the code
        mt.maximize_window()
        time.sleep(4)
        pg.click(x = 942, y = 480)
        time.sleep(0.5)
        pg.hotkey('ctrl', 'v')  # paste the message
        time.sleep(0.5)
        pg.press('backspace', presses = 265)
        time.sleep(0.5)
        pg.press('left', presses = 11)
        time.sleep(0.5)
        pg.press('backspace', presses = 265)
        mt.find_element_by_xpath("//button[text()='Sign In']").click()

        # click on API development tools button
        time.sleep(3)
        mt.find_element_by_xpath("//a[text()='API development tools']").click()
        time.sleep(3)

        # fill in long and short title and go to id/hash page
        mt.find_element_by_id("app_title").send_keys(name)
        mt.find_element_by_id("app_shortname").send_keys("TESTING")
        mt.find_element_by_id("app_save_btn").click()
        time.sleep(2)
        while ClickIfVisible('error.PNG'):
            mt.find_element_by_id("app_save_btn").click()
            pg.moveTo(x = 837, y = 705)  # blocking the error icon
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


def PasteMessageInFile():
    pg.click(x = -1103, y = 290)
    time.sleep(0.5)
    pg.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pg.hotkey('ctrl', 's')


def GetPhone():
    ClickIfVisible('phone.PNG')
    time.sleep(INTERVAL)
    ClickIfVisible('smalller_copy.PNG')
    PasteMessageInFile()
    file = open(MESSAGE_PATH, mode = 'r')
    p = file.read()
    file.close()
    DeleteContentInFile()
    return p


def GetName():
    ClickIfVisible('at_sign.PNG')
    time.sleep(INTERVAL)
    ClickIfVisible('copy_link.PNG')
    PasteMessageInFile()
    file = open(MESSAGE_PATH, mode = 'r')
    n = file.read().split('/')[-1]
    file.close()
    DeleteContentInFile()
    return n


def LogOut():
    GotoSettings()
    pg.scroll(-7000)
    time.sleep(2)
    ClickIfVisible('dots.PNG')
    time.sleep(0.5)
    pg.click()
    time.sleep(0.5)
    pg.scroll(-7000)
    time.sleep(2)
    ClickIfVisible('logout.PNG')
    time.sleep(2)
    ClickIfVisible('disconnect.PNG')


def GotoSettings():
    ClickIfVisible('hamburger.PNG')
    time.sleep(INTERVAL)
    ClickIfVisible('menu_icon.PNG')
    time.sleep(INTERVAL)
    ClickIfVisible('cog_wheel.PNG')
    time.sleep(INTERVAL)


def DeleteContentInFile():
    file = open(MESSAGE_PATH, mode = 'w')
    file.close()


def GetCodeFromFile():
    message_file = open(MESSAGE_PATH, mode = 'r')
    for line in message_file.readlines():
        for word in line.split():
            if word.strip('.').isdigit():
                message_file.close()
                return word.replace('.', '')


def CopyMessageToClipboard():
    pg.click(x = 350, y = 239)  # press telegram convo
    time.sleep(1)
    pg.mouseDown(x = 222, y = 763)
    time.sleep(1)
    pg.mouseUp()
    time.sleep(0.5)
    ClickIfVisible('copy.PNG')  # copy the message


def CreateSessionFile(s: Sim):
    client = TelegramClient('sessions\\' + s.phone, s.ID, s.access_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(sim.phone)
        time.sleep(0.5)
        CopyMessageToClipboard()
        time.sleep(0.5)
        PasteMessageInFile()
        code = GetCodeFromFile()
        client.sign_in(phone = sim.phone, code = code)
        print(Fore.GREEN + f"Created {sim.name} session file! Logging out..")
        client.disconnect()
    else:
        print(Fore.RED + f"{sim.name} already exist! skipping")
        client.disconnect()


if __name__ == '__main__':
    while not ClickIfVisible('your_phone.PNG'):
        GotoSettings()
        phone, name = GetPhone(), GetName()
        pg.scroll(-7000)
        time.sleep(INTERVAL)
        ClickIfVisible('back.PNG')
        sim = Login(phone, name)
        AddToFile(sim)
        CreateSessionFile(sim)
        LogOut()
        time.sleep(2)
    print(
        Fore.MAGENTA + "FINISHED CREATING ALL USERS! \nDon't forget to move all files from the sessions folder \n "
                       "Move the files to the desired project folder and rename new_list to your new Group!")
