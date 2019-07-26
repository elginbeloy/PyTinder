# IDEA: https://hackernoon.com/a-crude-imessage-api-efed29598e61
# IDEA: Use email and get it instantly

# Import needed libraries
import json
import csv
import time
import pyfiglet

from bs4 import BeautifulSoup
from collections.abc import Iterable
from selenium import webdriver
from termcolor import colored
from tinder_bot import inference

from config import (
    TINDER_COLOR,
    SHORT_PAGE_LOAD_WAIT_TIME, 
    LONG_PAGE_LOAD_WAIT_TIME ,
    SWIPE_LOAD_TIME
)


# Print PyTinder banner
ascii_banner = pyfiglet.figlet_format("PyTinder v.1.2")
print(colored(ascii_banner, TINDER_COLOR))
print("By Elgin Beloy\n")


# Text to show before Spider related outputs
PYTINDER_INDICATOR = colored("[PYTINDER] ", TINDER_COLOR)
LOGINBOT_INDICATOR = colored("[LOGINBOT] ", 'blue')
SWIPEBOT_INDICATOR = colored("[SWIPEBOT] ", TINDER_COLOR)
CHATBOT_INDICATOR = colored("[CHATBOT] ", 'magenta')


# Start selenium session with Chrome driver
print(f"{PYTINDER_INDICATOR} Starting Selenium headless Chrome instance...")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

driver = webdriver.Chrome('./chromedriver', options=chrome_options)

print(f"{PYTINDER_INDICATOR} Complete!")


def login():
    print(f"{LOGINBOT_INDICATOR} Going to https://tinder.com...")
    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get("https://tinder.com")
    time.sleep(LONG_PAGE_LOAD_WAIT_TIME)

    # Click to login with phone
    print(f"{LOGINBOT_INDICATOR} Loging in with phone...")
    login_with_phone_button = driver.find_element_by_xpath('//button[@aria-label="Log in with phone number"]')
    login_with_phone_button.click()
    time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)

    # Get phone number to use for Tinder account
    PHONE_NUMBER = input(f"{LOGINBOT_INDICATOR} Tinder Account Phone (#) : ")

    # Fill in phone number and click to continue
    phone_input = driver.find_element_by_name("phone_number")
    phone_input.send_keys(PHONE_NUMBER)
    continue_button = driver.find_element_by_xpath('//button/span/span[text()="Continue"]')
    continue_button.click()

    # Get login code from user (they should have received via SMS)
    login_code = input(f'{LOGINBOT_INDICATOR} Enter the code texted to {PHONE_NUMBER}: ')

    # Fill in code in each of the six input boxes then click to continue
    number_inputs = driver.find_elements_by_xpath('//input[@type="tel"]')
    for index, num_input in enumerate(number_inputs):
        num_input.send_keys(login_code[index])

    continue_button = driver.find_element_by_xpath('//button/span/span[text()="Continue"]')
    continue_button.click()
    time.sleep(LONG_PAGE_LOAD_WAIT_TIME) # Wait an extra long time for loging in

    print(f"{LOGINBOT_INDICATOR} Login complete!")

    # If it makes a fuss about notifications
    try:
        # Click to allow notifications and enable
        print(f"{LOGINBOT_INDICATOR} Enabling notifications for use...")
        allow_button = driver.find_element_by_xpath('//button[@aria-label="Allow"]')
        allow_button.click()
        time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)

        allow_button = driver.find_element_by_xpath('//button[@aria-label="Enable"]')
        allow_button.click()
        time.sleep(LONG_PAGE_LOAD_WAIT_TIME) # Wait extra long for loading of profiles

    except: 
        pass


def remove_if_tinder_notification():
    # If there is a "Not interested" button (I.E a notification), click it.
    try:
        not_interested_button = driver.find_element_by_xpath('//button/span/span[text()="Not interested"]')
        not_interested_button.click()
        print(f"{PYTINDER_INDICATOR} Removing Tinder notification...")
        time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)
    except:
        pass


def respond_to_messages():
    print(f"{CHATBOT_INDICATOR} Doing the rounds!")
    messages_button = driver.find_element_by_xpath('//div/span[text()="Messages"]')
    messages_button.click()
    time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)

    chats = driver.find_elements_by_class_name('messageListItem')
    for chat in chats:
        chat.click()
        time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)

        match_name = driver.find_element_by_xpath(
            '//div[contains(@class, "profileCard__header__info")]/div/div/span').text

        print(f"{CHATBOT_INDICATOR} Checking chat with {match_name}.")

        all_messages = driver.find_elements_by_class_name('msg')
        if len(all_messages) == 0:
            print(f"{CHATBOT_INDICATOR} Starting conversation with {match_name}...")
            print(f"Saying: Hey, what are you up to this weekend?")

            response_box = driver.find_element_by_class_name("sendMessageForm__input")
            response_box.send_keys("Hey, what are you up to this weekend?")
            send_button = driver.find_element_by_xpath('//form/button[@type="submit"]')
            send_button.click()
            continue
        
        last_message = all_messages[-1]
        
        # C(#000) means text color #000, which is only true if message is 
        # the matches and not ours ...
        if "C(#000)" in last_message.get_attribute('class').split():
            # Message might not have text, just emoji.
            try:
                last_message_text = last_message.find_element_by_xpath(".//span").text
            except:
                last_message_text = "i like this picture"

            response_text = inference(last_message_text)
            print(f"{CHATBOT_INDICATOR} Responding to {match_name}'s last message...")
            print(f"{match_name}: {last_message_text}")
            print(f"Response: {response_text}")

            response_box = driver.find_element_by_class_name("sendMessageForm__input")
            response_box.send_keys(response_text)
            send_button = driver.find_element_by_xpath('//form/button[@type="submit"]')
            send_button.click()

            print(f"{CHATBOT_INDICATOR} Response sent!")

    print(f"{CHATBOT_INDICATOR} All done! Going back to swiping tab.")
    x_button = driver.find_element_by_xpath('//a[@href="/app/matches"]')
    x_button.click()
    time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)





if __name__ == "__main__":
    # Login to tinder 
    login()

    while True:
        # Respond to messages
        respond_to_messages()

        # Like 50 people then keep responding
        likes = 0
        while likes < 50:
            remove_if_tinder_notification()

            # If it's a match, keep swiping.
            try:
                keep_swiping_button = driver.find_element_by_xpath('//a/span[text()="Keep Swiping"]')
                keep_swiping_button.click()
                print(f"{SWIPEBOT_INDICATOR} Match found!")
                time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)
            except:
                pass

            # Like em!
            like_button = driver.find_element_by_xpath('//button[@aria-label="Like"]')
            like_button.click()
            print(f"{SWIPEBOT_INDICATOR} Swiped right.")
            likes += 1
            time.sleep(SHORT_PAGE_LOAD_WAIT_TIME)

