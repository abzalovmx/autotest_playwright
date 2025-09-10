import re
import pytest
from playwright.sync_api import sync_playwright, Page, expect, BrowserContext, Dialog
from time import sleep

# full

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


def test_focused(page: Page):
    page.goto('https://www.google.com/')
    fild = page.locator('[name="q"]')
    expect(fild).to_be_focused()


def test_tabs(page: Page, context: BrowserContext):
    page.goto('https://www.qa-practice.com/elements/new_tab/link')
    link = page.locator('#new-page-link')
    with context.expect_page() as new_page_event:
        link.click()
    new_page = new_page_event.value
    result = new_page.locator('#result-text')
    expect(result).to_have_text('I am a new page in a new tab')
    page.get_by_role('link', name='New tab button').click()


def test_hover(page: Page):
    page.goto('https://magento.softwaretestingboard.com/hero-hoodie.html')
    men = page.locator('#ui-id-5')
    tops = page.locator('#ui-id-17')
    jackets = page.locator('#ui-id-19')
    men.hover()
    tops.hover()
    jackets.click()


def test_d_n_d(page: Page):
    page.goto('https://www.qa-practice.com/elements/dragndrop/boxes')
    drag_me = page.locator('#rect-draggable')
    drop_here = page.locator('#rect-droppable')
    drag_me.drag_to(drop_here)


def test_alert(page: Page):
    def cancel_alert(alert: Dialog):
        print(alert.message)
        print(alert.type)
        alert.dismiss()
    def fill_a_acc(alert: Dialog):
        alert.accept('some text')
    page.on('dialog', lambda alert: alert.accept('some text'))
    page.goto('https://www.qa-practice.com/elements/alert/prompt')
    page.get_by_role('link', name='Click').click()