from behave import *


# don't use regex matching?
# use_step_matcher("re")


@given("User Bob is Browsing the store")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given User Bob is Browsing the store')


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


@given("Admin Alice is uploading an extension installer")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given Admin Alice is uploading an extension installer')


@when("Admin Alice logs out before the upload finishes And")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Admin Alice logs out before the upload finishes And')


@step("Admin Alice logs back in again")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Admin Alice logs back in again')


@then("Administration section Dashboard will be shown")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then Administration section Dashboard will be shown')


@given("Registered User Bob had made an order X")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given Registered User Bob had made an order X')


@step("Bob changed their email address after the order X had been made")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Bob changed their email address after the order X had been made')


@when("Admin Alice sends an email to the author of the order")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Admin Alice sends an email to the author of the order')


@then("Email will be sent to the new Bob's address")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u"STEP: Then Email will be sent to the new Bob's address")


@given("Admin Alice has opened Registered User's (Bob's) Reward points balance")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u"STEP: Given Admin Alice has opened Registered User's (Bob's) Reward points balance")


@when("Alice gives Bob K points")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Alice gives Bob K points')


@step("Alice gives Bob -(K/2) points")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Alice gives Bob -(K/2) points')


@then("Bob's points will be at their previous value")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u"STEP: Then Bob's points will be at their previous value")


@when("Alice gives Bob K (K > INT_MAX) points")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Alice gives Bob K (K > INT_MAX) points')


@then("Bob's points will be equal to (K plus his previous points balance)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u"STEP: Then Bob's points will be equal to (K + his previous points balance)")


