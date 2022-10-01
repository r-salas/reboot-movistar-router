#
#
#
#   Reboot Router
#
#

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

# Load .env file if exists and python-dotenv is installed
try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


def find_and_wait_by_xpath(browser, xpath):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(browser, 5.0).until(element_present)
    return browser.find_element(By.XPATH, xpath)


assert "ROUTER_ADMIN_PASSWORD" in os.environ, "Environment variable `ROUTER_ADMIN_PASSWORD` not found"

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--lang=en")

browser = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

browser.get("http://192.168.1.1/")

frame = find_and_wait_by_xpath(browser, '//frame[@name="mainFrame"]')

browser.switch_to.frame(frame)

elem = find_and_wait_by_xpath(browser, '//input[@name="Password"]')

elem.clear()
elem.send_keys(os.environ["ROUTER_ADMIN_PASSWORD"])
elem.send_keys(Keys.RETURN)

browser.switch_to.default_content()

browser.get("http://192.168.1.1/resetrouter.html")

elem = find_and_wait_by_xpath(browser, '//input[@type="button"]')

elem.click()

browser.close()
