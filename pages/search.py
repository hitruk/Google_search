from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GoogleSearchPage:

    URL = 'https://google.com'
    SEARCH_INPUT = (By.NAME, 'q')

    def __init__(self, browser):
        self.browser = browser

    def load(self):
        self.browser.get(self.URL)

    def search(self, phrase):
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(phrase + Keys.RETURN)
