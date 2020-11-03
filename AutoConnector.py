import pyautogui as pg
import time
from declerations import ClickIfVisible
from telethon.sync import TelegramClient
from colorama import Fore

"""OPEN CODE.TXT BEFORE STARTING!"""
"""MAKE SURE TO START TELEGRAM X ON THE FIRST ACCOUNT MAIN PAGE"""

MESSAGE_PATH = 'C:\\Users\\Guy Buky\\Desktop\\code.txt'
CARDS_PATH = 'C:\\Users\\Guy Buky\\Desktop\\new_list.py'


class Sim:
    def __init__(self, ID, access_hash, phone, name):
        self.ID = ID
        self.access_hash = access_hash
        self.phone = phone
        self.name = name


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


def PasteMessageInFile():
    pg.click(x = -1103, y = 290)
    time.sleep(0.5)
    pg.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pg.hotkey('ctrl', 's')


def DeleteMessageFromFile():
    pg.click(x = -387, y = 195)
    time.sleep(0.5)
    pg.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pg.press('backspace')
    time.sleep(0.5)
    pg.hotkey('ctrl', 's')


def CreateSimList():  # opens the file and retrieve each sim as an object
    cards = []
    f = open(CARDS_PATH, 'r')
    for line in f.readlines():
        if len(line) != 1:
            sim_id, acc_hash, phone_number, sim_name = line.split(',')
            sim_name = str(sim_name).replace("\n", "")  # remove newline from names
            s = Sim(int(sim_id), acc_hash, phone_number, sim_name)
            cards.append(s)
    f.close()
    return cards


def LogOut():
    time.sleep(2)
    ClickIfVisible('back.PNG')
    time.sleep(2)
    ClickIfVisible('hamburger.PNG')
    time.sleep(2)
    ClickIfVisible('menu_icon.PNG')
    time.sleep(2)
    ClickIfVisible('cog_wheel.PNG')
    time.sleep(2)
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


if __name__ == '__main__':
    sim_cards = CreateSimList()
    for sim in sim_cards:
        client = TelegramClient('sessions\\' + sim.phone, sim.ID, sim.access_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(sim.phone)
            CopyMessageToClipboard()
            time.sleep(1)
            PasteMessageInFile()
            code = GetCodeFromFile()
            client.sign_in(phone = sim.phone, code = code)
            print(Fore.GREEN + f"Created {sim.name} session file! Logging out..")
            LogOut()
            client.disconnect()
            DeleteMessageFromFile()
        else:
            print(Fore.RED + f"{sim.name} already exist! skipping")
            client.disconnect()

    print(f"\nSuccesfully created {len(sim_cards)} SESSION files! exiting..")
