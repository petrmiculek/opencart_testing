from behave import fixture, use_fixture

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def before_all(context):
    dp = {'browserName': 'firefox', 'marionette': 'true',
          'javascriptEnabled': 'true'}

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    context.browser = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',  # todo change
        desired_capabilities=dp)

    """
    context.browser = webdriver.Remote(
                    command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
                    desired_capabilities=dp)
    """

    context.browser.implicitly_wait(15)
    context.browser.get('http://pat.fit.vutbr.cz:8072/')


def after_all(context):
    context.browser.quit()
