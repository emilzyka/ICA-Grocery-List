from random import randint
from time import sleep
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from keyboard import write
from dotenv import load_dotenv
import os
from App import config


"""
This program finds and adds random recipes to your shopping list on the ICA app. All recipes are taken from "middagar".
No baking- or dessert recipes. All recipes add will be unique. 
You can select sorting category, number of recipes you want to add, and how many recipes to pick a random from.
There is no exception handling in the program. Make sure all inputs are made with the correct datatype. 
Once you entered all input don't press any key or click with your mouse as the webdriver will lose focus and likely
cause a crash. 

Sometimes pages or elements loads too quick/slow, and the program will crash because of that. 
Just restart if this happens. 
"""

# Store user input
antal, urval, kategori = config.user_define()
lst_måltider = []

# Load .env variables -> To login on the ICA website you need your "personnumer" and "password" for your account.
# You can load them from a .env file or just hard-code them below.
load_dotenv()
personnmr = os.getenv('PERSONNUMMER')
password = os.getenv('PASSWORD')

# Set up driver and create new local session of firefox
# Load the Directory path of your driver can be hard-coded or loaded from .env file in the Service() method.
ser_proxy = Service(os.getenv('DIRPATH_GECKO_DRIVER'))
driver = webdriver.Firefox(service=ser_proxy)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)


def navigate_xpath(xpath: str, driver: driver):
    """
    :param xpath:  The xpath of the element you want to click
    :param driver: Your selenium webdriver
    """
    element = wait.until(EC.element_to_be_clickable((By.XPATH, fr'{xpath}')))
    driver.execute_script("arguments[0].click();", element)


def log_in(personnmr: str, password: str, driver: driver):
    """
    :param personnmr: personnummer used to login to your account
    :param password: password used to login to your account
    :param driver: webdriver
    """
    driver.get("https://www.ica.se/recept/")
    navigate_xpath("//button[@id='onetrust-accept-btn-handler']", driver)
    navigate_xpath('//button[@class="button--32 login button--text-icon"]', driver)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        (By.XPATH, r'//iframe[@class="fullscreen-iframe-modal__frame"]')))
    navigate_xpath('//a[@class="nav__tab font-fixed"]', driver)
    navigate_xpath('//input[@id="userName"]', driver)
    driver.find_element(By.XPATH, r'//label[@class="input-text__label"]').click()
    driver.find_element(By.XPATH, r'//input[@id="userName"]').click()
    write(personnmr)
    navigate_xpath('//input[@id="password"]', driver)
    driver.find_element(By.XPATH, r'//label[@class="input-text__label"]').click()
    driver.find_element(By.XPATH, r'//input[@id="password"]').click()
    write(password)
    navigate_xpath('//button[@id="submit-button"]', driver)
    navigate_xpath('//button[@id="submit-button"]', driver)
    sleep(3)


def find_recipes(kategori: str, driver: driver):
    driver.switch_to.default_content()
    navigate_xpath('//a[@data-id="33"]', driver)
    navigate_xpath('//div[@class="filter-dropdown-selected"]', driver)
    navigate_xpath(f'//filter-option[@value="{kategori}"]', driver)


def select_r_recipe(urval, driver: driver):
    for i in range(urval):
        sleep(0.3)
        navigate_xpath('//a[@class="loadmore loadmore-button large-spinner ajax loadmore-loaded"]', driver)
    r = randint(1, 14 * urval)
    navigate_xpath(f'//article[@data-recipeposition="{r}"]/div', driver)
    navigate_xpath(f'//article[@data-recipeposition="{r}"]/div/header/h2/a', driver)


def add_recipe_new_lst(driver: driver):
    """
    :return: returns name of the recipe added as your first recipe for the "inköpslista"
    """
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, r'/html/body/div[1]/div/div/div[3]/div/div/main/div[1]/div[1]/div/h1')))
    name_recipe = driver.find_element(
        By.XPATH, r'/html/body/div[1]/div/div/div[3]/div/div/main/div[1]/div[1]/div/h1').text
    navigate_xpath('//button[@class="button--48 button--text-icon add-to-list"]', driver)
    navigate_xpath('//div[@class="check-all_text"]', driver)
    navigate_xpath('//button[@class="button--48 button--text-icon button--fullwidth"]', driver)
    navigate_xpath('//button[@class="button--48 button--text-icon button--fullwidth"]', driver)
    navigate_xpath('//button[@class="button--40 button--fullwidth"]', driver)
    navigate_xpath('//button[@class="button--40 button--secondary button--fullwidth"]', driver)
    driver.back()
    driver.refresh()
    return name_recipe


def check_name(driver: driver):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, r'/html/body/div[1]/div/div/div[3]/div/div/main/div[1]/div[1]/div/h1')))
    name_recipe = driver.find_element(
        By.XPATH, r'/html/body/div[1]/div/div/div[3]/div/div/main/div[1]/div[1]/div/h1').text
    return name_recipe


def append_new_recipe(driver: driver):
    navigate_xpath('//button[@class="button--48 button--text-icon add-to-list"]', driver)
    navigate_xpath('//div[@class="check-all_text"]', driver)
    navigate_xpath('//button[@class="button--48 button--text-icon button--fullwidth"]', driver)
    navigate_xpath('/html/body/div[1]/div/div/div[5]/div/div/div/div[2]/div/div/div/div[1]/div[1]', driver)
    navigate_xpath('//button[@class="button--40 button--secondary button--fullwidth"]', driver)
    driver.back()
    driver.refresh()


def execute_program():
    log_in(personnmr, password, driver)
    find_recipes(kategori, driver)
    select_r_recipe(urval, driver)
    name_recipe = add_recipe_new_lst(driver)
    lst_måltider.append(name_recipe)
    print(f'{name_recipe} lades till i inköpslistan')
    for i in range(antal - 1):
        select_r_recipe(urval, driver)
        n = ''
        n = check_name(driver)
        print(f'{n} lades till i inköpslistan')
        while n in lst_måltider:
            driver.back()
            driver.refresh()
            select_r_recipe(urval, driver)
            n = check_name(driver)
        name_recipe = check_name(driver)
        lst_måltider.append(name_recipe)
        append_new_recipe(driver)
        tmp_name = name_recipe

    driver.close()
    print('')
    print(f'Din inköpslista består av följande recept: {lst_måltider}')


execute_program()
