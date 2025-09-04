import re
import pytest
from playwright.sync_api import sync_playwright, Page, expect
from time import sleep

# 44-35

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # headed режим
            slow_mo=200,     # замедление для наглядности
            proxy={"server": "http://inet.fido.uz:3128"},
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


def test_first(page: Page):
    sleep(3)
    page.goto('https://www.google.com/')
    search_field = page.get_by_role('combobox')
    search_field.fill('cat')
    search_field.press('Enter')
    expect(page).to_have_title(re.compile('^cat'))


def test_by_role(page: Page):
    sleep(3)
    page.goto('https://magento.softwaretestingboard.com/')
    page.get_by_role('menuitem', name="What's New").click()
    sleep(2)
    page.get_by_role('link', name='Search Terms').click()
    sleep(3)


def test_by_text(page: Page):
    sleep(3)
    page.goto('https://www.qa-practice.com/')
    page.get_by_text('Single UI Elements').click()
    sleep(3)


def test_by_label(page: Page):
    sleep(3)
    page.goto('https://www.qa-practice.com/elements/input/simple')
    field = page.get_by_label('Text string')
    field.press_sequentially('ksjdfhksjdfh', delay=500)
    sleep(1)
    field.press('Control+a')
    sleep(1)
    field.press('Backspace')
    sleep(3)


def test_by_placeholder(page: Page):
    sleep(3)
    page.goto('https://www.qa-practice.com/elements/input/simple')
    page.get_by_placeholder('Submit me').fill('skdjfhsdf')
    sleep(3)


def test_by_alt_text(page: Page):
    sleep(3)
    page.goto('https://epam.com')
    page.get_by_alt_text('The Next Evolution of Software Engineering').click()
    sleep(3)


def test_by_title(page: Page):
    sleep(3)
    page.goto('https://www.google.com/')
    page.get_by_title('Шукаць').fill('cat')
    sleep(3)


def test_by_testid(page: Page):
    sleep(3)
    page.goto('https://www.airbnb.com/')
    sleep(2)
    page.get_by_test_id('header-tab-search-block-tab-EXPERIENCES').click()
    sleep(3)


def test_by_css_selector(page: Page):
    sleep(3)
    page.goto('https://magento.softwaretestingboard.com/')
    page.locator('.showcart').click()
    sleep(3)


def test_by_xpath(page: Page):
    sleep(3)
    page.goto('https://magento.softwaretestingboard.com/')
    page.locator('//*[@class="action showcart"]').click()
    sleep(3)