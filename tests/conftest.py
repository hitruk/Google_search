import json
import pytest
from selenium import webdriver

# ====== local browser ======
CONFIG_PATH = 'tests/config.json'
DEFAULT_WAIT_TIME = 10
SUPPORTED_BROWSERS = ['chrome', 'firefox']
geckodriver_chrome = '/usr/bin/chromedriver'


@pytest.fixture(scope='session')
def config():
    # Считываем данные из config.json
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture(scope='session')
def config_browser(config):
    # Проверить и вернуть выбор браузера из данных конфигурации
    if 'browser' not in config:
        raise Exception('The config file does not contain "browser"')
    elif config['browser'] not in SUPPORTED_BROWSERS:
        raise Exception(f'"{config["browser"]}" is not a supported browser')
    return config['browser']


@pytest.fixture(scope='session')
def config_wait_time(config):
    # Проверить и вернуть время ожидания из данных конфигурации
    return config['wait_time'] if 'wait_time' in config else DEFAULT_WAIT_TIME


@pytest.fixture
def browser(config_browser, config_wait_time):
    # Инициализируем WebDriver
    if config_browser == 'chrome':
        driver = webdriver.Chrome(executable_path=geckodriver_chrome)
    elif config_browser == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise Exception(f'"{config_browser}" is not a supported browser')
    driver.implicitly_wait(config_wait_time)

    yield driver
    driver.close()

# ====== selenoid broowser ======
