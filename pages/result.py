from selenium.webdriver.common.by import By

class GoogleResultPage:

    LINK_DIVS = (By.CSS_SELECTOR, '#center_col > div')
    SEARCH_INPUT = (By.NAME, 'q')

    @classmethod
    def PHRASE_RESULTS(cls, phrase):
        xpath = f"//div[@id='center_col']//*[contains(text(), '{phrase}')]"
        return (By.XPATH, xpath)

    def __init__(self, browser):
        self.browser = browser

    def link_div_count(self):
        link_divs = self.browser.find_elements(*self.LINK_DIVS)
        return len(link_divs)

    def phrase_result_count(self, phrase):
        phrase_results = self.browser.find_elements(*self.PHRASE_RESULTS(phrase))
        return len(phrase_results)

    def search_input_value(self):
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        return search_input.get_attribute('value')