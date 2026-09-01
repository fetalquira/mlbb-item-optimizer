import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# requests and BeautifulSoup only fetch the static HTML
url = 'https://www.mobilelegends.com/hero/detail'
params = {'channelid': 2678785, 'heroid': 49}
r = requests.get(url, params=params)

# trying Playwright to fetch dynamic content
complete_url = 'https://www.mobilelegends.com/hero/detail?channelid=2678785&heroid=49'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until='networkidle')
    root_div = page.locator("#root").inner_html()
    print(root_div)
    browser.close()