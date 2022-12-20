from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from webdriver_manager.chrome import ChromeDriverManager


options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")


class WebDriverSingleton:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        return cls._driver
