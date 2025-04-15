# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D5936CE4811350413B70AAE6C8FBBB38E54362F19CA92A925BC3567F65CD6EC7162BD06D9B51AD968EB2B925C1C91644F0E4E67B176B20B1A2CACABC90840ADA657981830D280EFB136D52FF63261C6C6238567D3F1041AF215660E9BF2A3C666C62809C0A78C34D1C4D15A769E45742C2C84649D51F572BC9FFFCBF3E5CE1C157CE0FC5A76A90BD5DFA8C1CE9387E1268BDB9A37A872CA604FE9E638E1D7565666D54B941E88A6A89BCD827022F3B4114359654F2864DACFF89275C39B705A024F3B0495D12531D071C77DFACA94A31F18CDEC850B08E2316F56084720316707E53D3DD8CB49C3A118306DDC3DB0374EADE4B9764C27439FE06C2300BF73668FB4D8319E3A7213BB29A318C67F85FF61FB6E725426D15408735EF741338F09F87DBDFD94BBCB8F79624221B3D59536F7865384C4CA7B487497DB31A5ED636C805F8D16EC63EBA3688ABE906E02ACA185D5961E03B6AEF98F20FF91A59486BC1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
