import sys
import time
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def chrome_driver(chromeDriverPath, headless = False):
    service = webdriver.ChromeService(executable_path=chromeDriverPath, log_output='log/test_log')
    options = webdriver.ChromeOptions() # 옵션 지정 객체
    options.add_argument("--start-maximized") # 화면 최대화
    if headless:
        options.add_argument("--headless") # 백그라운드 명시적 지정
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

def setupBeforeCrawling(chromeDriver):
    driver = chromeDriver
    # 네이버 메인 페이지 이동
    driver.get("https://www.naver.com")
    # 로딩 대기
    driver.implicitly_wait(5)

    # 쇼핑 버튼 클릭
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[5]/ul/li[4]/a").click() # XPATH
    driver.implicitly_wait(3)

    # 쇼핑 페이지 전환
    shopping_window_handle = driver.window_handles[-1]
    driver.switch_to.window(shopping_window_handle)

    # 팝업 닫는 로직
    if driver.find_element(By.CSS_SELECTOR, "div._buttonArea_button_area_2o-U6 > button._buttonArea_button_1jZae._buttonArea_close_34bcm"):
        driver.find_element(By.CSS_SELECTOR, "div._buttonArea_button_area_2o-U6 > button._buttonArea_button_1jZae._buttonArea_close_34bcm").click()
    return driver