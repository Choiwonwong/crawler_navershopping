from utils import *
from crawling import *
import time
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from openpyxl import Workbook

driver_path = '/Users/choiwonwong/STUDY/NS_CRAWL/chromedriver-mac-arm64/chromedriver'
output_name = datetime.today().strftime("%Y-%m-%d")

if __name__ == "__main__":
    start_time = time.time()
    driver = chrome_driver(driver_path)

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

    # 입력 버튼 선택
    search = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[1]/div/input") # XPATH
    search.click()

    # 쿼리 검색
    search.send_keys("아이폰 14 Pro")
    search.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)

    # 무한 스크롤 처리
    processInfiniteScroll(driver)

    # 전체 상품 리스트 - div > basicList_basis__uNBZx
    items = driver.find_element(By.CLASS_NAME, "basicList_list_basis__uNBZx")

    # 광고 제품 HTML 요소 가져오기 - div > adProduct_inner__W_nuz
    adElements = items.find_elements(By.CLASS_NAME, "adProduct_inner__W_nuz")
    subDriver = chrome_driver(driver_path, headless=True)
    adItems = crawlAdItems(adElements=adElements, subDriver=subDriver)

    # 미광고 제품 - div > product_inner__gr8QR
    elements = items.find_elements(By.CLASS_NAME, "product_inner__gr8QR")
    items = crawlItems(elements=elements, subDriver=subDriver)

    crawledItems = adItems + items
    subDriver.quit()

    wb = Workbook()
    ws = wb.active
    headers = list(crawledItems[0].keys())

    for col_idx, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col_idx, value=header)
    
    for row_idx, data_dict in enumerate(crawledItems, start=2):
        for col_idx, header in enumerate(headers, start=1):
            ws.cell(row=row_idx, column=col_idx, value=data_dict.get(header))
    
    wb.save(output_name + ".xlsx")
    print("[" + output_name + "] 크롤링 결과물이 생성되었습니다.")
    end_time = time.time()
    sec = end_time - start_time
    print("소요 시간:", timedelta(seconds=sec))