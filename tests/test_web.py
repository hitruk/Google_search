from pages.search import GoogleSearchPage
from pages.result import GoogleResultPage

def test_basic_google_search(browser):
    PHRASE = 'Hello World'

    search_page = GoogleSearchPage(browser)
    search_page.load()
    search_page.search(PHRASE)

    result_page = GoogleResultPage(browser)
    assert result_page.link_div_count() > 0
    assert result_page.phrase_result_count(PHRASE) > 0
    assert result_page.search_input_value() == PHRASE
