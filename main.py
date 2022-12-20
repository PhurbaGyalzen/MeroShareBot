from mero_bot import MeroSeleniumDriver
import csv
if __name__ == "__main__":
    import csv

    with open("./accounts.csv", 'r') as file:
        csvreader = csv.reader(file)
        headings = next(csvreader)
        for account in csvreader: 
            obj = MeroSeleniumDriver()
            obj.login(account[0], account[1], account[3])
            obj.checkShares()
            obj.apply(account[2], account[4])