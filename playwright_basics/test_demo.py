import re
import pytest
from playwright.sync_api import sync_playwright, Page, expect


# 25-01

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={"server": "http://inet.fido.uz:3128"})
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_google():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()


        page.goto("https://www.google.com/")
        page.fill("textarea[name='q']", "cat")
        page.press("textarea[name='q']", "Enter")
        expect(page).to_have_title(re.compile('^cat'))
        browser.close()
