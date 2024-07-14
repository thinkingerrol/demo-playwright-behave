from behave import then, when
from playwright.sync_api import expect

@when('I open the url {url}')
def when_open_url(context, url):
    context.page.goto(url)


@then('"{text}" is visible on the page')
def then_text_is_visible(context, text):
    expect(context.page.get_by_text(text, exact=True)).to_be_visible()
