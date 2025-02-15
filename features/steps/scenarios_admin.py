import sys
import time
from time import sleep
from zipfile import ZipFile

from behave import *

from features.steps.scenarios_customer import Patiently
from features.steps.scenarios_customer import ensure_user_logged_in
from features.steps.scenarios_customer import user_email_registered
from features.steps.scenarios_customer import main_page_url as main_page_user_url
from features.steps.scenarios_customer import user_full_name

from features.steps.scenarios_customer import click
from features.steps.scenarios_customer import send_keys
from features.steps.scenarios_customer import clear

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# don't use regex matching?
# use_step_matcher("re")

main_page_admin_url = "http://pat.fit.vutbr.cz:8072/admin/index.php"
user_email_new = ""

# There are two scenarios for testing user reward points changes
user_points_before_1 = 0
user_points_before_2 = 0

# points added to user
K_points = 2147483648  # 1 + maximum Int32 value


def ensure_admin_logged_in(context):
    context.browser.get(main_page_admin_url)

    try:
        context.browser.find_element(By.ID, "input-username").click()
    except NoSuchElementException:
        # already logged in
        return

    context.browser.find_element(By.ID, "input-username").send_keys("admin")
    context.browser.find_element(By.ID, "input-password").click()
    context.browser.find_element(By.ID, "input-password").send_keys("admin")
    context.browser.find_element(By.CSS_SELECTOR, ".btn").click()


# ==================================================
#  Customers Online Report shows customers


@given("User Bob is Browsing the store")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError


@when("Admin Area Customers Online Report section is opened")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Admin Area Customers Online Report section is opened')


@then("Admin Area Customers Online Report will show Online customer/s")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then Admin Area Customers Online Report will show Online customer/s')


# ==================================================
#  Extension Installer Upload Interrupted


def create_extension_like_file():
    file_name = 'spam.zip'
    try:
        with ZipFile(file_name, 'w') as myzip:
            myzip.write('eggs.txt')
    except Exception:
        return ""

    return file_name


"""
# This scenario was not implemented
# as I found no way to upload a file

@given("Admin Alice is uploading an extension installer")
def step_impl(context):

    file_path = create_extension_like_file()

    ensure_admin_logged_in(context)

    elements = [
        (By.CSS_SELECTOR, ".fa-indent", click, None),
        (By.CSS_SELECTOR, "#extension span", click, None),
        (By.LINK_TEXT, "Extension Installer", click, None),

        # clicking on button-upload brings up local system window that selenium cannot interact with
        # (By.ID, "button-upload", click, None),

        # cannot send keys to this button
        # (By.NAME, "button-upload", send_keys, file_path),

        (By.NAME, "file", send_keys, file_path),

        # logout
        (By.CSS_SELECTOR, ".nav > li:nth-child(4) > a", click, None),
    ]
    
    wait = Patiently.wait(context.browser)
    try:
        for elem in elements:
            curr_elem = (elem[0], elem[1])
            if elem[2] == click:
                curr_elem = wait.until(EC.element_to_be_clickable(curr_elem))
                curr_elem.click()
            elif elem[2] == send_keys:
                curr_elem = wait.until(EC.visibility_of_element_located(curr_elem))
                curr_elem.send_keys(elem[3])
            elif elem[2] == clear:
                curr_elem = wait.until(EC.visibility_of_element_located(curr_elem))
                curr_elem.clear()
    except Exception as exc:
        raise
    print("ok")


@when("Admin Alice logs out before the upload finishes And")
def step_impl(context):

    raise NotImplementedError(u'STEP: When Admin Alice logs out before the upload finishes And')


@step("Admin Alice logs back in again")
def step_impl(context):

    raise NotImplementedError(u'STEP: And Admin Alice logs back in again')


@then("Administration section Dashboard will be shown")
def step_impl(context):

    raise NotImplementedError(u'STEP: Then Administration section Dashboard will be shown')

"""

# =============================================================
#  User information change is reflected in orders' view


@given("Registered User Bob had made an order X")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    ensure_user_logged_in(context)

    # context.browser.get(main_page_user_url)

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

    wait = Patiently().wait(context.browser)

    try:
        for elem in elements:
            curr_elem = wait.until(EC.element_to_be_clickable(elem))
            curr_elem.click()
    except Exception as exc:
        pass
    pass


@step("Bob changed their email address after the order X had been made")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # ensure_user_logged_in(context)

    # context.browser.get(main_page_user_url)

    global user_email_new
    user_email_new = "xmicul08@vutbr.cz"

    elements = [
        (By.CSS_SELECTOR, ".list-inline .dropdown-toggle", click, None),
        (By.CSS_SELECTOR, ".dropdown-menu > li:nth-child(1) > a", click, None),
        (By.CSS_SELECTOR, "#content > .list-unstyled:nth-child(2) > li:nth-child(1) > a", click, None),
        (By.ID, "input-email", click, None),
        (By.ID, "input-email", clear, None),
        (By.ID, "input-email", send_keys, user_email_new),
        (By.CSS_SELECTOR, ".btn-primary", click, None)
    ]

    wait = Patiently.wait(context.browser)

    try:
        for elem in elements:
            elem_locator = (elem[0], elem[1])
            if elem[2] == click:
                curr_elem = wait.until(EC.element_to_be_clickable(elem_locator))
                curr_elem.click()
            elif elem[2] == send_keys:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.send_keys(elem[3])
            elif elem[2] == clear:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.clear()
    except Exception as exc:
        raise exc
    pass


@when("Admin Alice checks order author's email")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    ensure_admin_logged_in(context)

    context.browser.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .btn").click()

    # name surname
    elem_name = context.browser.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(2) tr:nth-child(1) a")

    if elem_name.text != user_full_name:
        raise Exception("name mismatch (internal error): expected '{}', actual: '{}'"
                        .format(user_full_name, elem_name.text))


@then("Email shown will be the new Bob's address")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    # email
    elem_email = context.browser.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a")
    if elem_email.text != user_email_new:
        if elem_email.text == user_email_registered:
            assert False, "original email address did not get changed\n"\
                            "    expected '{}', actual '{}'".format(user_email_new, elem_email.text)
        else:
            assert False, "invalid email - neither the expected not the original address\n"\
                            "    expected '{}', actual '{}'".format(user_email_new, elem_email.text)


# =======================================================
#  User's reward points are altered (even values)
def get_user_reward_points(context):
    """
    Must be called when on reward points page
    :param context:
    :return:
    """
    tries_counter = 0
    succeeded = False
    balance_text_split = []
    while tries_counter < 3 and not succeeded:
        try:
            elem = context.browser.find_element(By.XPATH, "(//div[@id='reward']/div/table/tbody/tr)[last()]")
            balance_text_split = elem.text.split(' ')
            succeeded = True
        except Exception:
            tries_counter += 1

    if balance_text_split[0] != "Balance":
        # No Reward points history for given user -> no rows
        return 0
        # this may hide possible future errors (page layout changes)

    points = int(balance_text_split[1])
    print("Bob has", points, "points")
    return points


@given("Admin Alice has opened Registered User's (Bob's) Reward points balance")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(main_page_admin_url)

    ensure_admin_logged_in(context)

    try:
        hamburger_menu = context.browser.find_element(By.CSS_SELECTOR, ".fa-indent")
        hamburger_menu.click()
    except NoSuchElementException:
        # Hamburger menu is a toggle (expanded, collapsed) that remembers the last state it was in (between sessions)
        # I found no locator that would work in both states
        pass

    elements = [

        (By.CSS_SELECTOR, "#customer span", click, None),
        (By.CSS_SELECTOR, ".in > li:nth-child(1) > a", click, None),
        (By.CSS_SELECTOR, "tr:nth-child(1) .btn-primary", click, None),
        (By.LINK_TEXT, "Reward Points", click, None),
    ]

    wait = Patiently.wait(context.browser)

    try:
        for elem in elements:
            elem_locator = (elem[0], elem[1])
            if elem[2] == click:
                curr_elem = wait.until(EC.element_to_be_clickable(elem_locator))
                curr_elem.click()
            elif elem[2] == send_keys:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.send_keys(elem[3])
            elif elem[2] == clear:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.clear()
    except Exception as exc:
        time.sleep(5)
        raise


@when("Alice gives Bob K points")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    global user_points_before_1
    user_points_before_1 = get_user_reward_points(context)

    elements = [
        # (By.ID, "input-points", click, None),
        (By.ID, "input-points", send_keys, str(K_points)),
        (By.ID, "button-reward", click, None),
    ]

    wait = Patiently.wait(context.browser)

    try:
        for elem in elements:
            elem_locator = (elem[0], elem[1])
            if elem[2] == click:
                curr_elem = wait.until(EC.element_to_be_clickable(elem_locator))
                curr_elem.click()
            elif elem[2] == send_keys:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.send_keys(elem[3])
            elif elem[2] == clear:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.clear()
    except Exception as exc:
        raise

    print("added", K_points)


@step("Alice gives Bob -(K/2) points")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    elements = [
        # (By.ID, "input-points", click, None),
        (By.ID, "input-points", send_keys, "{0:d}".format(-K_points // 2)),
        (By.ID, "button-reward", click, None),
    ]

    wait = Patiently.wait(context.browser)

    try:
        for elem in elements:
            elem_locator = (elem[0], elem[1])
            if elem[2] == click:
                curr_elem = wait.until(EC.element_to_be_clickable(elem_locator))
                curr_elem.click()
            elif elem[2] == send_keys:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.send_keys(elem[3])
            elif elem[2] == clear:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.clear()
    except Exception as exc:
        raise

    print("subtracted {0:d}".format(-K_points // 2))


@then("Bob's points will be at their previous value")
def step_impl(context):
    """
    @precondition: Loaded page is 'View user reward points'
    :type context: behave.runner.Context
    """
    user_points_after = get_user_reward_points(context)

    diff = user_points_after - user_points_before_1

    assert diff == 0, "Bob's points differ by '{}', expected difference '{}'".format(diff, 0)


# ======================================================
#  User's reward points are altered (high values)


# @given is higher up, reused from previous step


@when("Alice gives Bob K (K > INT_MAX) points")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    global user_points_before_1
    user_points_before_1 = get_user_reward_points(context)

    elements = [
        # (By.ID, "input-points", click, None),
        (By.ID, "input-points", send_keys, str(K_points)),
        (By.ID, "button-reward", click, None),
    ]

    wait = Patiently.wait(context.browser)

    try:
        for elem in elements:
            elem_locator = (elem[0], elem[1])
            if elem[2] == click:
                curr_elem = wait.until(EC.element_to_be_clickable(elem_locator))
                curr_elem.click()
            elif elem[2] == send_keys:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.send_keys(elem[3])
            elif elem[2] == clear:
                curr_elem = wait.until(EC.visibility_of_element_located(elem_locator))
                curr_elem.clear()
    except Exception as exc:
        raise

    print("added", K_points)


@then("Bob's points will be equal to (K plus his previous points balance)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    user_points_after = get_user_reward_points(context)

    diff = user_points_after - user_points_before_1

    assert diff == K_points, "Bob's points differ by '{}', expected difference '{}'" \
        .format(diff, K_points)
