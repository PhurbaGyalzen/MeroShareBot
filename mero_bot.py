import os
import time
from pathlib import Path
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from MeroBot.main_bot_driver import WebDriverSingleton


class MeroSeleniumDriver:
    def __init__(self):
        self.driver = WebDriverSingleton.get_driver()
        self.dotenv_path = Path("path/to/.env")
        load_dotenv(dotenv_path=self.dotenv_path)

    def login(self, username, password, bank_index):
        # Navigate to login page
        self.driver.get(os.getenv("MERO_SHARE_LOGIN_URL"))

        # Select the bank
        self.driver.find_element(By.XPATH, os.getenv("BANK_SELECTOR")).click()
        bank_dropdown = self.driver.find_element(By.XPATH, os.getenv('BANK_MAIN_SELECTOR'))
        select = Select(bank_dropdown)
        banks = bank_dropdown.text.split("\n")
        bank_input = self.driver.find_element(By.XPATH, os.getenv("BANK_SELECTOR_INPUT"))
        with open("banks.txt", mode="w") as file:
            for index, bank in enumerate(banks):
                file.write(f"{bank} ---------------<<bank index>>---> [{index}]\n")
        bank_input.send_keys(banks[int(bank_index)])
        self.driver.find_element(By.XPATH, os.getenv("BANK_OPTION_SANIMA")).click()

        # Enter the username and password
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys(username)
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        # time.sleep(200)
        password_input.send_keys(Keys.RETURN)
        print("USER LOGGED IN")
        time.sleep(1)


    def checkShares(self):
        # Navigate to My ASBA Process
        self.driver.find_element(By.XPATH, os.getenv("HAMBURGER_MENU")).click()
        self.driver.find_element(By.XPATH, os.getenv("ASBA_TAB_LINK")).click()
        time.sleep(1)

        # Apply For ISSUE
        self.driver.find_element(By.XPATH, os.getenv("APPLY_FOR_ISSUE")).click()
        time.sleep(1)

        # Find available shares
        company_elements = self.driver.find_elements(By.CLASS_NAME, "company-list")
        values = [
            company.find_element(By.CLASS_NAME, "company-name").text.split("\n")
            for company in company_elements
        ]
        values = [
            value for value in values if value[3] == "IPO" and value[4] == "Debentures"
        ]

        print("Available Shares:")
        print("*" * 50)
        for index, value in enumerate(values, 1):
            print(f"{value[0]} [{index}]")
        print("*" * 50)

        # Select share
        share_index = None
        while share_index is None:
            try:
                share_number = int(input("Select the Share Number:")) - 1
                company_elements[share_number].find_element(
                    By.TAG_NAME, "button"
                ).click()
                share_index = share_number
            except (IndexError, ValueError):
                print("Please enter a valid share number")
        time.sleep(1)

    def apply(self, crn, transaction_pin):
        # Select bank from dropdown
        bank_dropdown = self.driver.find_element(By.ID, "selectBank")
        select = Select(bank_dropdown)
        banks = bank_dropdown.text.split("\n")
        banks = [bank.strip() for bank in banks if bank.strip() != ""][1:]
        
        if len(banks) == 1:
            select.select_by_visible_text(banks[0])
        else:
            print("Avaliable Banks: \n")
            for index, bank in enumerate(banks, 1):
                print(f"{bank}-[{index}]")
            while True:
                bank_value = int(input("Enter the bank index from the given options bank options:"))
                if bank_value > len(banks) or bank_value == 0:
                    print("please enter the right bank number availabel.")
                    continue
                select.select_by_visible_text(banks[bank_value - 1])
                break

        # Enter applyKitta and CRN number
        apply_kitta = self.driver.find_element(By.ID, "appliedKitta")
        apply_kitta.send_keys("10")
        crn_number = self.driver.find_element(By.ID, "crnNumber")
        crn_number.send_keys(crn)

        # Agree to disclaimer and proceed
        self.driver.find_element(By.ID, "disclaimer").click()
        self.driver.find_element(By.XPATH, os.getenv("PROCEED_BUTTON")).click()

        # Enter transaction PIN
        pin_input = self.driver.find_element(By.ID, "transactionPIN")
        pin_input.send_keys(transaction_pin)

        time.sleep(1)
        self.driver.find_element(By.XPATH, os.getenv('APPLY_BUTTON')).click()

        time.sleep(3)
