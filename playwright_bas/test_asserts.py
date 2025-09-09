import re
import pytest
from playwright.sync_api import sync_playwright, Page, expect
from time import sleep

# 53-13

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=200,
            # proxy={"server": "http://inet.fido.uz:3128"},
            args=["--disable-blink-features=AutomationControlled"]
        )
        yield browser
        browser.close()


@pytest.fixture()
def context(browser):
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )
    yield context
    context.close()


@pytest.fixture()
def page(context):
    page = context.new_page()
    yield page
    page.close()


def test_visible(page: Page):
    page.goto("https://www.qa-practice.com/elements/input/simple")
    reqs = page.locator('#req_text')
    expect(reqs).not_to_be_visible()
    page.locator('#req_header').click()
    expect(reqs).to_be_visible()

def test_enabled_and_select(page: Page):
    page.goto('https://www.qa-practice.com/elements/button/disabled')
    button = page.locator('#submit-id-submit')
    expect(button).to_be_disabled()
    page.locator('#id_select_state').select_option('enabled')
    expect(button).to_be_enabled()
    expect(button).to_have_text('Submit')

def test_value(page: Page):
    txt = 'qwerty'
    page.goto('https://www.qa-practice.com/elements/input/simple')
    input_field = page.locator('#id_text_string')
    input_field.fill(txt)
    expect(input_field, f'input value is not {txt}').to_have_value(txt)


def test_sorting_and_waits(page: Page):
    page.goto('https://magento.softwaretestingboard.com/hero-hoodie.html')
    greet = page.locator('.greet.welcome').locator('nth=0')
    expect(greet).not_to_be_empty()
    first_man = page.locator('.product-item-link').locator('nth=0')
    print(first_man.inner_text())
    page.locator('#sorter').locator('nth=0)').select_option('Price')
    expect(page).to_have_url(re.compile('price'))
    print(first_man.inner_text())
