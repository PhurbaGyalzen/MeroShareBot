import os
import time
from pathlib import Path
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from MeroBot.main_bot_driver import WebDriverSingleton

from MeroBot.utils import save_bank_records


class MeroSeleniumDriver:
    def __init__(self):
        self.driver = WebDriverSingleton.get_driver()
        load_dotenv()
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.kitta = "10"
        self.search_share_type = "Debentures"
        # uncomment the code below for searching only Ordinary Shares
        # self.search_share_type="Ordinary Shares"

    def wait_for_element(self, by, path):
        return self.wait.until(EC.presence_of_element_located((by, path)))

    def login(self, username, password, bank_index):
        # Navigate to login page
        self.driver.get(os.getenv("MERO_SHARE_LOGIN_URL"))

        # Select the bank
        self.wait_for_element(by=By.XPATH, path=os.getenv("BANK_SELECTOR")).click()
        bank_dropdown = self.wait_for_element(
            by=By.XPATH, path=os.getenv("BANK_MAIN_SELECTOR")
        )
        select = Select(bank_dropdown)
        banks = bank_dropdown.text.split("\n")
        bank_input = self.wait_for_element(
            by=By.XPATH, path=os.getenv("BANK_SELECTOR_INPUT")
        )
        save_bank_records(filename="banks.txt", banks=banks)
        bank_input.send_keys(banks[int(bank_index)])
        self.wait_for_element(by=By.XPATH, path=os.getenv("BANK_OPTION_SANIMA")).click()

        # Enter the username and password
        username_input = self.wait_for_element(by=By.ID, path="username")
        username_input.send_keys(username)
        password_input = self.wait_for_element(by=By.ID, path="password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        print("USER LOGGED IN")

    def checkShares(self):
        # Navigate to My ASBA Process
        self.wait_for_element(by=By.XPATH, path=os.getenv("HAMBURGER_MENU")).click()
        self.wait_for_element(by=By.XPATH, path=os.getenv("ASBA_TAB_LINK")).click()

        # Apply For ISSUE
        self.wait_for_element(by=By.XPATH, path=os.getenv("APPLY_FOR_ISSUE")).click()

        # Find available shares
        company_elements = self.wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "company-list"))
        )
        values = [
            company.find_element(By.CLASS_NAME, "company-name").text.split("\n")
            for company in company_elements
        ]
        values = [
            value
            for value in values
            if value[3] == "IPO" and value[4] == self.search_share_type
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

    def apply(self, crn, transaction_pin):
        # Select bank from dropdown
        bank_dropdown = self.wait_for_element(by=By.ID, path="selectBank")
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
                bank_value = int(
                    input("Enter the bank index from the given options bank options:")
                )
                if bank_value > len(banks) or bank_value == 0:
                    print("please enter the right bank number availabel.")
                    continue
                select.select_by_visible_text(banks[bank_value - 1])
                break

        # Enter applyKitta and CRN number
        apply_kitta = self.wait_for_element(by=By.ID, path="appliedKitta")
        apply_kitta.send_keys(self.kitta)

        crn_number = self.wait_for_element(by=By.ID, path="crnNumber")
        crn_number.send_keys(crn)

        # Agree to disclaimer and proceed
        self.wait_for_element(by=By.ID, path="disclaimer").click()
        self.wait_for_element(by=By.XPATH, path=os.getenv("PROCEED_BUTTON")).click()

        # Enter transaction PIN
        pin_input = self.wait_for_element(by=By.ID, path="transactionPIN")
        pin_input.send_keys(transaction_pin)

        # Click Apply Button
        self.wait_for_element(by=By.XPATH, path=os.getenv("APPLY_BUTTON")).click()

        # waits for 3 seconds before closing the webdriver
        time.sleep(3)
