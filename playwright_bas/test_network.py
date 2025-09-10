import re
import pytest, requests
from playwright.sync_api import sync_playwright, Page, expect, BrowserContext, Dialog, Request

# 41-14

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=800,
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


def test_listen(page: Page):
    def req(request: Request):
        print(request.post_data, request.url)
    page.on('request', req)
    page.on('response', lambda response: print('RESPONSE', response.text, response.url))
    page.goto('https://www.qa-practice.com/')
    page.get_by_role('link', name='Text input').click()
    input_field = page.locator('#id_text_string')
    input_field.fill('some text')
    input_field.press('Enter')

def test_catch_res(page: Page):
    page.goto('https://www.airbnb.ru/')
    with page.expect_response('**/autosuggestions**') as response_event:
        page.locator('#search-block-tab-EXPERIENCES').click()
    response = response_event.value
    print(response.url)
    print(response.status)
    print(response.json())