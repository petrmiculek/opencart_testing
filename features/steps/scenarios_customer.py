import sys

from behave import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# use_step_matcher("re")
from selenium.webdriver.support.wait import WebDriverWait

main_page_url = "http://pat.fit.vutbr.cz:8072"
orders_count = 0
delay = 5  # seconds, hopefully; for explicit waiting on element loading


# don't worry about the name, it will all make sense later
class Patiently:
    wait_var = None

    # def __init__(self, context):

    @classmethod
    def wait(cls, browser):
        if cls.wait_var is None:
            cls.wait_var = WebDriverWait(browser, delay)
        return cls.wait_var


def ensure_user_is_logged_in(context):

    context.browser.get(main_page_url)
    context.browser.find_element(By.CSS_SELECTOR, ".fa-user").click()

    try:
        context.browser.find_element(By.LINK_TEXT, "Login").click()
    except NoSuchElementException:
        # already logged in
        return

    context.browser.find_element(By.ID, "input-email").click()

    context.browser.find_element(By.ID, "input-email").send_keys("petr.miculek@gmail.com")

    context.browser.find_element(By.ID, "input-password").send_keys("verysecurepassword")

    context.browser.find_element(By.XPATH, "//input[@value=\'Login\']").click()

    # context.browser.find_element(By.CSS_SELECTOR, ".fa-home").click()


def count_user_orders(context):

    wait = Patiently().wait(context.browser)
    ensure_user_is_logged_in(context)

    context.browser.get(main_page_url)

    elements = [
        # (By.CSS_SELECTOR, ".list-inline .dropdown-toggle"),  # ".fa-user"
        # (By.CSS_SELECTOR, ".dropdown-menu > li:nth-child(2) > a"),
        (By.XPATH, "//div[@id=\'top-links\']/ul/li[2]/a/span[2]"),
        (By.XPATH, "//div[@id=\'top-links\']/ul/li[2]/ul/li[2]/a"),
    ]

    try:
        for elem in elements:
            curr_elem = wait.until(EC.visibility_of_element_located(elem))
            curr_elem.click()
    except Exception as exc:
        pass
    pass
    """
    count = 0
    try:
        while count <= 1000:  # arbitraty limit

            # count lines of table == orders
            css_text = "tr:nth-child({})".format(count + 1)
            context.browser.find_element(By.CSS_SELECTOR, css_text).click()

            count += 1

    except NoSuchElementException:
        # once the total orders amount is exceeded, return it
        return count
    """
    try:
        # also works but decided against using it
        # row_list = context.browser.find_elements(By.XPATH, "//div[@id=\'content\']/div/table/tbody/tr")

        row_list = context.browser.find_elements(By.XPATH, "//tbody/tr")
        return len(row_list)

    except NoSuchElementException:
        return 0


# ===========================================================================
#  Scenario Outline: Search for existing product


@given("Main page is loaded")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(main_page_url)  # already done by setup

    """
    # verify it's the main page - no benefit
    title = context.browser.find_element_by_xpath('/html/head/title')

    expected_title = 'My Store'
    assert title == expected_title, "Expected = {0}, Real = {1}".format(expected_title, title)
    """


@when("{} is searched for")  # <existing product>
def step_impl(context, product_name):
    """
    :type context: behave.runner.Context
    :type product_name: str
    """

    context.browser.find_element(By.NAME, "search").click()
    context.browser.find_element(By.NAME, "search").send_keys(product_name)
    context.browser.find_element(By.CSS_SELECTOR, ".fa-search").click()

    # raise NotImplementedError(u'STEP: When <existing product> is searched for')


@then("Results will contain {}")  # <existing product>
def step_impl(context, product_name):
    """
    :type context: behave.runner.Context
    :type product_name: str
    """
    expected_url = main_page_url + "/index.php?route=product/search&search=" + product_name
    url = context.browser.current_url

    assert url == expected_url, "Expected URL: '{}', Actual URL: '{}'".format(expected_url, url)

    # potentially also test contents of page
    # raise NotImplementedError(u'STEP: Then Results will contain <existing product>')


# ===========================================================================
#  Scenario: Order gets added to Order History (Registered user)


@step("User has N orders in their Order History")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    ensure_user_is_logged_in(context)

    global orders_count
    orders_count = count_user_orders(context)


@when("User creates and submits Order")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    wait = Patiently().wait(context.browser)

    context.browser.get(main_page_url)

    # sequence of elements to click on
    elements = [
        # add item to cart
        (By.LINK_TEXT, "iPhone"),
        (By.ID, "button-cart"),

        # fill in order details
        (By.XPATH, "//div[@id=\'cart\']/button"),
        (By.XPATH, "//div[@id=\'cart\']/ul/li[2]/div/p/a[2]/strong/i"),
        (By.ID, "button-payment-address"),
        (By.ID, "button-shipping-address"),
        (By.ID, "button-shipping-method"),
        (By.NAME, "agree"),
        (By.ID, "button-payment-method"),

        # submit order
        (By.ID, "button-confirm"),
        (By.LINK_TEXT, "Continue")
    ]

    try:
        for elem in elements:
            curr_elem = wait.until(EC.element_to_be_clickable(elem))
            curr_elem.click()
    except Exception as exc:
        pass
    pass


@step("User's Order History will be N plus 1 Orders long")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    """
    context.browser.get(main_page_url)
    
    elements = [
        (By.CSS_SELECTOR, ".list-inline .dropdown-toggle"),
        (By.CSS_SELECTOR, ".dropdown-menu > li:nth-child(2) > a"),
    ]

    try:
        for elem in elements:
            curr_elem = Patiently.wait().until(EC.element_to_be_clickable(elem))
            curr_elem.click()
    except Exception as exc:
        pass
    pass
    """

    new_orders = count_user_orders(context)

    assert new_orders - orders_count == 1,\
        "Creating an order resulted in {} new orders (there were {} before)".format(new_orders, orders_count)


@given("There is a valid order form filled up to the Delivery Method step")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given There is a valid order form filled up to the Delivery Method step')


@when("Malicious user inputs the shipping method and a very long comment about their order before proceeding")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: When Malicious user inputs the shipping method and a very long comment about their order before proceeding')


@then("Order will proceed or warn user about the comment-too-long problem")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then Order will proceed or warn user about the comment-too-long problem')


@given("Purchase a Gift Certificate page is open")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given Purchase a Gift Certificate page is open')


@when("Gift certificate purchase Form is filled and submitted")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Gift certificate purchase Form is filled and submitted')


@then("User is redirected back to the store")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then User is redirected back to the store')


@step("Admin Gift Vouchers section will show the gift certificate")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Admin Gift Vouchers section will show the gift certificate')
