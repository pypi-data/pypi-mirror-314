import pytest
from easyweb.config import config


@pytest.fixture(scope='module')
def page():
    from playwright.sync_api import sync_playwright
    driver = sync_playwright().start()
    browser = driver.chromium.launch_persistent_context(
        user_data_dir=config.USER_DATE_DIR,
        executable_path=config.EXECUTABLE_PATH,
        ignore_https_errors=True,
        no_viewport=True,
        slow_mo=500,
        headless=config.HEADLESS,
        bypass_csp=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--start-maximized',
        ],

    )
    _page = browser.pages[0]
    yield _page
    browser.close()
    driver.stop()
