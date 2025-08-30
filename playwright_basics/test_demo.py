import re
from playwright.sync_api import Page, expect

# 13-09


def test_one(page: Page):
      page.goto("https://google.com")
      search_field = page.get_by_role('combobox')
      search_field.fill('Enter')
      page.keyboard.press('Enter')
      expect(page).to_have_title(re.compile('cat'))


