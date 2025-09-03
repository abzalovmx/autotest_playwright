import re
import pytest
from playwright.sync_api import sync_playwright, Page, expect


# 37-00

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


def test_google(page: Page):
    page.goto("https://www.google.com/")
    page.fill("textarea[name='q']", "cat")
    page.press("textarea[name='q']", "Enter")
    expect(page).to_have_title(re.compile("^cat"))


def test_by_role(page: Page):
    page.goto("https://magento.softwaretestingboard.com/")
    page.get_by_role("menuitem", name="What's New").click()
    page.get_by_role("link", name="Search Terms").click()
