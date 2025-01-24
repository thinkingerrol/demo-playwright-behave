from behave_playwright import Playwright


def before_all(context):
    Playwright.before_all(context)


def before_scenario(context, scenario):
    Playwright.before_scenario(context, scenario)


def after_scenario(context, scenario):
    try:
        # implement your cleanup here, to ensure repeatability of the tests
        pass
    finally:
        Playwright.after_scenario(context, scenario)


def before_step(context, step):
    Playwright.before_step(context, step)


def after_step(context, step):
    Playwright.after_step(context, step)
