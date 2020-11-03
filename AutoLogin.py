from telethon.sync import TelegramClient
import time
from selenium import webdriver
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from declerations import NameList

## implementing the driver and saved profile
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Guy Buky\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
simSMS = webdriver.Chrome(executable_path = "chromedriver.exe", options = options)

# entering to the website
simSMS.get("https://www.simsms.org/")
simSMS.maximize_window()

## pressing Country button
for country in simSMS.find_elements_by_tag_name('b'):
    if country.text == "Израиль":  # israel
        country.click()
        break

## pressing the Telegram button
titles = simSMS.find_elements_by_class_name(name = "title")
for title in titles:
    if title.text == "Telegram":
        title.click()
        break

button_list = simSMS.find_elements_by_id("get-phone")
for button in button_list:
    if button.is_displayed():
        button.click()
        break

## gets the phone number
time.sleep(5)
country_code = simSMS.find_element_by_xpath("//button[@title='Скопировать номер с кодом страны']").text
phone = country_code + simSMS.find_element_by_xpath("//button[@title='Скопировать номер без кода страны']").text
print(f"phone: {phone}")

## signs up with the phone number
client = TelegramClient('main_phone', 1922783, '2cbeb7b4527d23558780b5db22707cfe')
client.connect()
client.send_code_request(phone = phone)

## retrieving the code from the website and finish signing up
time.sleep(90)  # wait until code arrives to simSMS
code = simSMS.find_element_by_xpath("//button[@title='Скопировать код из СМС']")

# giving the sim a random name from name file
names = NameList()
name = random.choice(names)
client.start(phone = phone, code_callback = lambda: code, first_name = name[0], last_name = name[1])

## open telegram web and login
time.sleep(5)
tw = webdriver.Chrome(executable_path = "chromedriver.exe")
tw.get("https://web.telegram.org/#/login")
tw.maximize_window()
text_field_tw = WebDriverWait(tw, 15).until(
    EC.presence_of_element_located((By.NAME, "phone_number"))
)
text_field_tw.send_keys(phone)
time.sleep(3)
text_field_tw.submit()
time.sleep(1)
tw.find_element_by_xpath("//*[contains(text(), 'OK')]").click()
time.sleep(150)  # wait at least 2 minutes for sms
tw.find_element_by_xpath("//*[contains(text(), 'Send code via SMS')]").click()

## get back to simSMS and get the login code to telegram web
simSMS.find_element_by_xpath("//button[text()='Доп СМС']").click()
time.sleep(90)
login_code = simSMS.find_element_by_xpath("//button[@title='Скопировать код из СМС']")
tw.find_element_by_name("phone_code").send_keys(login_code)

## now we're logged in, time to move to my.telegram.org
mt = webdriver.Chrome(executable_path = "chromedriver.exe")
mt.get("https://my.telegram.org/auth/")
text_field_mt = WebDriverWait(mt, 15).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
)

text_field_mt.send_keys(phone)
text_field_mt.submit()

## get the login code to mt from telegram convo in telegram web
telegram_icon = tw.find_element_by_xpath("//span[text()='Telegram ']")
telegram_icon.click()
time.sleep(2)
messages = tw.find_elements_by_class_name("im_message_text")
message = messages[-1].text.split()
for i in range(len(message)):
    if message[i] == "code:":
        mt_code = message[i + 1]

## paste the code in my.telegram.org to enter
password_field = mt.find_element_by_id("my_password")
password_field.send_keys(mt_code)
time.sleep(0.5)
password_field.submit()

## now fill in the required fields to go to the id/hash page
time.sleep(5)
mt.find_element_by_xpath("//a[text()='API development tools']").click()
mt.find_element_by_id("app_title").send_keys(name[0] + " " + name[1])
time.sleep(2)
mt.find_element_by_id("app_shortname").send_keys(name[0].replace(' ', '').upper() + "SIM")
time.sleep(3)
mt.find_element_by_id("app_save_btn").click()
time.sleep(5)

ID = int(mt.find_elements_by_tag_name('span')[0].text)
HASH = mt.find_elements_by_tag_name('span')[2].text

# create a new client with id/hash/phone to create a new session file
new_client = TelegramClient(phone, ID, HASH)
new_client.connect()
if not new_client.is_user_authorized():
    new_client.send_code_request(phone)

# get the code from telegram web and finish session file
telegram_icon.click()
time.sleep(2)
messages = tw.find_elements_by_class_name("im_message_text")
message = messages[-1].text.split()[2].strip('.')  # login code
new_client.sign_in(phone = phone, code = message)

# last stage - write to file
file = open('cards.py', 'a')
file.write(str(ID) + ',' + HASH + ',' + phone + ',' + name + '\n')

# exiting properly
simSMS.quit()
tw.quit()
mt.quit()
client.disconnect()
new_client.disconnect()
del client
del new_client
