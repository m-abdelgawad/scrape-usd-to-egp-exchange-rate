from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_egp_rate(driver_path):

    options = Options()
    # options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.

    chrome_service = Service(driver_path)
    browser = webdriver.Chrome(service=chrome_service, options=options)

    browser.get(url='https://www.google.com/')

    search_box = browser.find_element(By.CSS_SELECTOR, 'input.gLFyf')
    search_box.send_keys('1USD to EGP')
    search_box.send_keys(Keys.RETURN)

    egp_rate = browser.find_element(
        By.CSS_SELECTOR,
        'div#knowledge-currency__updatable-data-column div div:nth-child(2) span'
    ).text

    # All windows related to driver instance will quit
    browser.quit()

    return egp_rate
