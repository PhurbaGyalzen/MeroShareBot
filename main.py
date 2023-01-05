from mero_bot import MeroSeleniumDriver

import csv
if __name__ == "__main__":
    import csv
    from pyfiglet import Figlet
    from termcolor import colored

    custom_fig = Figlet(font='standard')
    print(colored(custom_fig.renderText("Mero Share Bot"), 'green'))
    with open("./accounts.csv", 'r') as file:
        csvreader = csv.reader(file)
        headings = next(csvreader)
        for account in csvreader: 
            obj = MeroSeleniumDriver()
            obj.login(username=account[0], password=account[1], bank_index=account[3])
            obj.checkShares()
            obj.apply(crn=account[2], transaction_pin=account[4])