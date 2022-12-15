import time
import os
from pathlib import Path
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager



dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)


USERNAME = os.getenv('UN')
PASSWORD = os.getenv('PD')

options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# open the webdriver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get(os.getenv('MERO_SHARE_LOGIN_URL'))
print("Opened meroshare...")

# Fill the login form
bank = driver.find_element(
    by=By.XPATH, value=os.getenv('BANK_SELECTOR')).click()
bank_search = driver.find_element(
    by=By.XPATH, value=os.getenv('BANK_SELECTOR_INPUT'))
bank_search.send_keys("SANIMA BANK LTD (15800)")
driver.find_element(
    by=By.XPATH, value=os.getenv('BANK_OPTION_SANIMA')).click()
print("Bank selected...")

username = driver.find_element(by=By.ID, value="username")
username.send_keys(USERNAME)
print("Username entered...")

password = driver.find_element(by=By.ID, value="password")
password.send_keys(PASSWORD)
password.send_keys(Keys.RETURN) 
print("password entered...")

time.sleep(1)
print("redirectetd to dashboard")


# Navigating to My ASBA Processs
driver.find_element(by=By.XPATH, value=os.getenv('HAMBURGER_MENU')).click()
print('clicked the hamburger icon...')
driver.find_element(by=By.XPATH, value=os.getenv('ASBA_TAB_LINK')).click()
print("clicked the Asba menu...")
time.sleep(1)

# Apply For ISSUE
driver.find_element(by=By.XPATH, value=os.getenv('APPLY_FOR_ISSUE')).click()
print("clicked to the Apply for Issue...")
time.sleep(1)
companies = driver.find_elements(by=By.CLASS_NAME, value='company-list')
values =[company for company in [company.find_element(by=By.CLASS_NAME, value='company-name').text.split('\n') for company in companies] if (company[3]=='IPO' and company[4]=='Debentures')]

print("Available Shares:")
print("*"*50)
for index, value in enumerate(values, 1):
    print(f"{value[0]} [{index}]")
print("*"*50)
share_index = int(input("Select the Share Number:")) -1
try:
    companies[share_index].find_element(by=By.TAG_NAME, value='button').click()
except IndexError:
    print("Please enter valid bank number")
    share_index = int(input("Select the Share Number:"))


time.sleep(1)
select = Select(driver.find_element(by=By.ID, value='selectBank'))
select.select_by_value(str(os.getenv('BANK_VALUE')))

applyKitta = driver.find_element(by=By.ID, value="appliedKitta")
applyKitta.send_keys("10")
crnNumber = driver.find_element(by=By.ID, value='crnNumber')
crnNumber.send_keys(os.getenv('CRN_NUMBER'))

driver.find_element(by=By.ID, value="disclaimer").click()
time.sleep(1)
driver.find_element(by=By.XPATH , value=os.getenv('PROCEED_BUTTON')).click()

time.sleep(3000)
driver.close()
