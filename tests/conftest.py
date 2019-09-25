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


# ====== selenoid browsers ======
CONFIG_PATH_SELENOID = 'tests/config_selenoid.json'
URL_SELENOID = "http://192.168.2.14:8080/wd/hub"
SUPPORTED_BROWSERS_SELENOID = ['chrome', 'firefox', 'opera']
SUPPORTED_VERSION_SELENOID = ['75.0', '76.0', '67.0', '68.0', '60.0', '62.0']
DEFAULT_WAIT_TIME_SELENOID = 10
SUPPORTED_BROWSERS_VERSION = [
    ['chrome', '75.0'],
    ['chrome', '76.0'],
    ['firefox', '67.0'],
    ['firefox', '68.0'],
    ['opera', '60.0'],
    ['opera', '62.0']
]


@pytest.fixture(scope='session')
def config_selenoid():
    with open(CONFIG_PATH_SELENOID, 'r') as config_selenoid_file:
        data_selenoid = json.load(config_selenoid_file)
    return data_selenoid


@pytest.fixture(scope='session')
def config_browser_name(config_selenoid):
    if 'browserName' not in config_selenoid:
        raise Exception('The config_selenoid file does not contain "browserName"')
    elif config_selenoid['browserName'] not in SUPPORTED_BROWSERS_SELENOID:
        raise Exception(f'"{config_selenoid["browserName"]}" is not a supported browser')

    return config_selenoid['browserName']


@pytest.fixture(scope='session')
def config_version(config_selenoid):
    if 'version' not in config_selenoid:
        raise Exception('The config_selenium file does not contain "version"')
    elif config_selenoid['version'] not in SUPPORTED_VERSION_SELENOID:
        raise Exception(f'"{config_selenoid["version"]}" is not a supported version')

    return config_selenoid['version']


@pytest.fixture(scope='session')
def config_enableVNC(config_selenoid):
    if 'enableVNC' not in config_selenoid:
        raise Exception('The config_selenoid file does not contain "enableVNC"')
    elif config_selenoid['enableVNC'] not in [True, False]:
        raise Exception(f'"{config_selenoid["enableVNC"]}" invalid value, "enableVNC" can only accept true or false')

    return config_selenoid['enableVNC']


@pytest.fixture(scope='session')
def config_enableVideo(config_selenoid):
    if 'enableVideo' not in config_selenoid:
        raise Exception('The config_selenoid file does not contain "enableVideo"')
    elif config_selenoid['enableVideo'] not in [True, False]:
        raise Exception(
            f'"{config_selenoid["enableVideo"]}" invalid value, "enableVideo" can only accept true or false')

    return config_selenoid['enableVideo']


@pytest.fixture(scope='session')
def capabilities_data(config_browser_name, config_version, config_enableVNC, config_enableVideo):
    browser_version = [config_browser_name] + [config_version]
    if browser_version not in SUPPORTED_BROWSERS_VERSION:
        raise Exception(f'"{[browser_version]}" is not a supported browsers version')
    else:
        capabilities = {
            "browserName": config_browser_name,
            "version": config_version,
            "enableVNC": config_enableVNC,
            "enableVideo": config_enableVideo
        }

    return capabilities


@pytest.fixture(scope='session')
def config_wait_time(config_selenoid):
    # Validate and return the wait time from the config data
    return config_selenoid['wait_time'] if 'wait_time' in config_selenoid else DEFAULT_WAIT_TIME_SELENOID


@pytest.fixture()
def browsers_selenoid(capabilities_data, config_wait_time):
    ''' Browsers selenoid for tests '''
    driver = webdriver.Remote(
        command_executor=URL_SELENOID,
        desired_capabilities=capabilities_data
    )
    driver.implicitly_wait(config_wait_time)
    yield driver
    driver.close()