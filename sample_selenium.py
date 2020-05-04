# -*- coding: utf-8 -*-
# Remote Control
import selenium
import unittest
import time
import re

# WebDriver
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class WebDriverFirefox(unittest.TestCase):
    def setUp(self):
        dp = {'browserName': 'firefox', 'marionette': 'true',
              'javascriptEnabled': 'true'}
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=dp)
        """
        #                desired_capabilities=DesiredCapabilities.FIREFOX)
        """

        # Firefox(executable_path='/path/to/geckodriver')

        """
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=dp)
        
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        """
        self.driver.implicitly_wait(10)
        self.base_url = "http://www.fit.vut.cz/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_fit(self):
        driver = self.driver
        driver.get(self.base_url)
        # driver.find_element_by_css_selector("li > a > span").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        if self.verificationErrors is not None:
            print(self.verificationErrors)

        self.assertEqual([], self.verificationErrors)


"""
class WebDriverChrome(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        \"""
        self.driver = webdriver.Chrome(executable_path='./chromedriver')
        \"""
        self.driver.implicitly_wait(10)
        self.base_url = "http://www.fit.vutbr.cz/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_fit(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_css_selector("li > a > span").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
"""

if __name__ == "__main__":
    unittest.main(warnings='ignore')
