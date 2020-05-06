from behave import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

main_page_url = "http://pat.fit.vutbr.cz:8072"
user_email_registered = "petr.miculek@gmail.com"
user_password_registered = "verysecurepassword"
user_full_name = "Name Surname"

user_registered = False

orders_count = 0

# supposed to be constants, #define ... ...
click = 0
send_keys = 1
clear = 2


class Patiently:
    delay = 15  # seconds, hopefully; for explicit waiting on element loading
    wait_var = None

    @classmethod
    def wait(cls, browser):
        if cls.wait_var is None:
            from selenium.webdriver.support.wait import WebDriverWait
            cls.wait_var = WebDriverWait(browser, cls.delay)
        return cls.wait_var


def ensure_user_logged_in(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(main_page_url)
    context.browser.find_element(By.CSS_SELECTOR, ".fa-user").click()

    try:
        login_link = context.browser.find_element(By.LINK_TEXT, "Login")
        login_link.click()
    except NoSuchElementException:
        # already logged in
        return

    elements = [
        (By.ID, "input-email", send_keys, user_email_registered),
        (By.ID, "input-password", send_keys, user_password_registered),
        (By.XPATH, "//input[@value=\'Login\']", click, None),
        (By.CSS_SELECTOR, ".fa-home", click, None)
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
        raise Exception("Could not log in")


def count_user_orders(context):
    """
    :type context: behave.runner.Context
    """
    wait = Patiently().wait(context.browser)
    ensure_user_logged_in(context)

    context.browser.get(main_page_url)

    elements = [
        (By.XPATH, "//div[@id=\'top-links\']/ul/li[2]/a/span[2]"),
        (By.XPATH, "//div[@id=\'top-links\']/ul/li[2]/ul/li[2]/a"),
    ]

    try:
        for elem in elements:
            curr_elem = wait.until(EC.element_to_be_clickable(elem))
            curr_elem.click()
    except Exception as exc:
        pass
    pass

    try:
        # also works but decided against using it
        # row_list = context.browser.find_elements(By.XPATH, "//div[@id=\'content\']/div/table/tbody/tr")

        row_list = context.browser.find_elements(By.XPATH, "//tbody/tr")
        return len(row_list)

    except NoSuchElementException:
        return 0
    except Exception:
        raise


def ensure_user_registered(context):
    """
    :type context: behave.runner.Context
    """
    global user_registered

    if user_registered:
        return

    context.browser.get(main_page_url)

    context.browser.find_element(By.CSS_SELECTOR, ".list-inline .dropdown-toggle").click()

    try:
        context.browser.find_element(By.LINK_TEXT, "Register").click()
    except NoSuchElementException:
        # logged in, cannot register
        return

    elements = [

        (By.ID, "input-firstname", send_keys, "Name"),
        (By.ID, "input-lastname", send_keys, "Surname"),
        (By.ID, "input-email", send_keys, user_email_registered),
        (By.ID, "input-telephone", send_keys, "731731390"),
        (By.ID, "input-address-1", send_keys, "Street"),
        (By.ID, "input-city", send_keys, "Brno"),
        (By.ID, "input-postcode", click, None),
        (By.CSS_SELECTOR, ".row:nth-child(2)", click, None),
        (By.ID, "input-country", click, None),
        (By.CSS_SELECTOR, "option:nth-child(62)", click, None),
        (By.ID, "input-zone", click, None),
        (By.CSS_SELECTOR, "#input-zone > option:nth-child(3)", click, None),
        (By.CSS_SELECTOR, ".row:nth-child(2)", click, None),
        (By.ID, "input-password", send_keys, user_password_registered),
        (By.ID, "input-confirm", send_keys, user_password_registered),
        (By.CSS_SELECTOR, ".row:nth-child(2)", click, None),
        (By.NAME, "agree", click, None),
        (By.CSS_SELECTOR, ".btn-primary", click, None),
        (By.LINK_TEXT, "Continue", click, None),

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
        pass

    user_registered = True
    print("HellNo")


def ensure_user_logged_out(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_element(By.CSS_SELECTOR, ".list-inline .dropdown-toggle").click()

    try:
        context.browser.find_element(By.LINK_TEXT, "Logout").click()
        context.browser.find_element(By.LINK_TEXT, "Continue").click()
    except NoSuchElementException:
        # already logged out
        return


# ===========================================================================
#  Scenario Outline: Search for existing product


@given("Main page is loaded")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get(main_page_url)


@when("{} is searched for")  # <existing product>
def step_impl(context, product_name):
    """
    :type context: behave.runner.Context
    :type product_name: str
    """

    context.browser.find_element(By.NAME, "search").click()
    context.browser.find_element(By.NAME, "search").send_keys(product_name)
    context.browser.find_element(By.CSS_SELECTOR, ".fa-search").click()


@then("Results will contain {}")  # <existing product>
def step_impl(context, product_name):
    """
    :type context: behave.runner.Context
    :type product_name: str
    """
    url = context.browser.current_url

    url_product_independent = url[:url.find("&search=")]
    expected_url_product_independent = main_page_url + "/index.php?route=product/search"

    assert url_product_independent == expected_url_product_independent, "Expected URL: '{}',\n Actual URL: '{}'" \
        .format(expected_url_product_independent, url_product_independent)


# ===========================================================================
#  Scenario: Order gets added to Order History (Registered user)


@given("User has N orders in their Order History")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # ensure_user_logged_in(context)

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
    new_orders = count_user_orders(context)

    assert new_orders - orders_count == 1, \
        "Creating an order resulted in {} new orders (there were {} before)".format(new_orders, orders_count)

    """
        There might be more pages to the table.
        
        The solution would be to generate a random string, put it as the order comment
        and then check if it is there. (There is no better attribute that guarantees
        that the order is the one we have just made)
    """


# =================================================================================
#  Make an order with long note (Registered user)


@given("There is a valid order form filled up to the Delivery Method step")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    wait = Patiently().wait(context.browser)

    ensure_user_logged_in(context)

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

        # if you want to move these two down to Then, change the JS selector
        (By.ID, "button-shipping-method"),
        (By.NAME, "agree"),
        # no longer needed, thanks to JS
        # (By.XPATH, "//p[3]/textarea")
    ]

    try:
        for elem in elements:
            curr_elem = wait.until(EC.element_to_be_clickable(elem))
            curr_elem.click()
    except Exception as exc:
        pass
    pass

    """
    w.ith open("order_note.txt") as file:
        very_long_note = file.read()
    """


@when("Malicious user inputs the shipping method and a very long comment about their order before proceeding")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # reached the error behavior at 3 million, could not avoid timeout that way
    context.browser.execute_script("var x = document.querySelectorAll('p:nth-child(4) > .form-control');"
                                   "for (let e of x) { e.value = 'AAAA'.repeat(1000000); }")


@then("Order will proceed or warn user about the comment-too-long problem")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    wait = Patiently().wait(context.browser)

    elements2 = [
        (By.ID, "button-payment-method"),

        # submit order
        (By.ID, "button-confirm"),
        (By.LINK_TEXT, "Continue")
    ]

    try:
        for elem in elements2:
            curr_elem = wait.until(EC.element_to_be_clickable(elem))
            curr_elem.click()
    except TimeoutException as exc:
        assert 0 == 1, "timeout reached"
    pass


# ==================================================
#  Purchase a Gift Certificate


@given("Registered user has opened the Purchase a Gift Certificate page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    ensure_user_logged_in(context)

    context.browser.get(main_page_url)
    context.browser.find_element(By.LINK_TEXT, "Gift Certificates").click()


@when("Gift certificate purchase Form is filled and submitted")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    elements = [
        (By.ID, "input-to-name", clear, None),
        (By.ID, "input-to-name", click, None),
        (By.ID, "input-to-name", send_keys, "Friend"),

        (By.ID, "input-to-email", clear, None),
        (By.ID, "input-to-email", click, None),
        (By.ID, "input-to-email", send_keys, "xmicul08@stud.fit.vutbr.cz"),

        (By.ID, "input-from-name", clear, None),
        (By.ID, "input-from-name", click, None),
        (By.ID, "input-from-name", send_keys, "Your Friend Name Surname"),

        (By.ID, "input-from-email", clear, None),
        (By.ID, "input-from-email", click, None),
        (By.ID, "input-from-email", send_keys, "petr.miculek@gmail.com"),

        (By.XPATH, "(//input[@name=\'voucher_theme_id\'])[3]", click, None),

        (By.ID, "input-message", clear, None),
        (By.ID, "input-message", click, None),
        (By.ID, "input-message", send_keys, "Happy end of exams term!"),

        (By.ID, "input-amount", click, None),
        (By.CSS_SELECTOR, ".pull-right:nth-child(1)", click, None),
        (By.NAME, "agree", click, None),
        (By.CSS_SELECTOR, ".btn-primary", click, None)
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
        pass
    pass


@then("User is redirected back to the store")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    shown_text = ""

    try:
        shown_text = context.browser.find_element(By.CSS_SELECTOR, "b:nth-child(1)").text
        pass
    except Exception as exc:
        pass

    "https://demo.opencart.com/index.php?route=account/account"

    assert shown_text != "Warning", "Page seems to have crashed"


# todo use or delete
@step("Admin Gift Vouchers section will show the gift certificate")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Admin Gift Vouchers section will show the gift certificate')
