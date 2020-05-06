from selenium import webdriver
from features.steps.scenarios_customer import Patiently, main_page_url, ensure_user_registered, user_registered


def before_all(context):
    dp = {'browserName': 'firefox', 'marionette': 'true',
          'javascriptEnabled': 'true'}

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    """
    context.browser = webdriver.Remote(
                    command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
                    desired_capabilities=dp)
    """

    context.browser.implicitly_wait(15)
    context.browser.set_window_size(800, 800)

    ensure_user_registered(context)


def after_all(context):
    context.browser.quit()
