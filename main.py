from mero_bot import MeroSeleniumDriver

if __name__ == "__main__":
    obj = MeroSeleniumDriver()
    obj.login()
    obj.checkShares()
    obj.apply()