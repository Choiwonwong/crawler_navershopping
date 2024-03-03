import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def chrome_driver(chromeDriverPath):
    service = webdriver.ChromeService(executable_path=chromeDriverPath, log_output='log/test_log')
    options = webdriver.ChromeOptions() # 옵션 지정 객체
    options.add_argument("--start-maximized") # 화면 최대화
    # options.add_argument("--headless") # 백그라운드 명시적 지정
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def processInfiniteScroll(chromeDriver):
    driver = chromeDriver
    beforeScrollY = driver.execute_script("return window.scrollY")
    while True:
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
        time.sleep(0.1)
        afterScrollY = driver.execute_script("return window.scrollY")
        if beforeScrollY == afterScrollY:
            break
        beforeScrollY = afterScrollY