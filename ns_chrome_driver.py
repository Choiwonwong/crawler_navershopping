import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver_path = '/Users/choiwonwong/STUDY/NS_CRAWL/chromedriver-mac-arm64/chromedriver'

service = webdriver.ChromeService(executable_path=driver_path, log_output='log/test_log')
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

# 네이버 메인 페이지 이동
driver.get("https://www.naver.com")
# 로딩 대기
driver.implicitly_wait(5)

# 쇼핑 버튼 클릭
# driver.find_element(By.CSS_SELECTOR, "a.link_service[href='https://shopping.naver.com/home']").click()
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[5]/ul/li[4]/a").click() # XPATH
driver.implicitly_wait(5)

# 전환
shopping_window_handle = driver.window_handles[-1]
driver.switch_to.window(shopping_window_handle)


# 입력 버튼 선택
# driver.find_element(By.CLASS_NAME, "_searchInput_search_text_3CUDs").click() # Class
search = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[2]/form/div[1]/div/input") # XPATH
search.click()

# 쿼리 검색
search.send_keys("아이폰 14 Pro")
search.send_keys(Keys.ENTER)
driver.implicitly_wait(5)

# 무한 스크롤 처리
beforeScrollY = driver.execute_script("return window.scrollY")
while True:
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    time.sleep(0.5)
    afterScrollY = driver.execute_script("return window.scrollY")
    if beforeScrollY == afterScrollY:
        break
    beforeScrollY = afterScrollY

# 전체 상품 리스트 - div > basicList_basis__uNBZx
items = driver.find_element(By.CLASS_NAME, "basicList_list_basis__uNBZx")

# 광고 제품 HTML 요소 가져오기 - div > adProduct_inner__W_nuz
adItems = items.find_elements(By.CLASS_NAME, "adProduct_inner__W_nuz")

# 광고 제품들을 담을 곳
adItemsDict = {}
for adItem in adItems:
    # 아이템 제목
    title = adItem.find_element(By.CLASS_NAME, "adProduct_link__NYTV9.linkAnchor").text
    # SDP
    link = adItem.find_element(By.CLASS_NAME, "adProduct_link__NYTV9.linkAnchor").get_attribute("href")

    # 등록 일자
    registedDate = adItem.find_element(By.CLASS_NAME, "adProduct_etc_box__UJJ90").find_element(By.TAG_NAME, "span").text[4:]

    # 가격
    try: 
        price = adItem.find_element(By.CLASS_NAME, "price_num__S2p_v").text
    except:
        price = "판매 중단"

    # 배송비
    deliveryFee = adItem.find_element(By.CLASS_NAME, "price_delivery__yw_We").text.split()[-1]

    # 카테고리
    categories = []
    adItemCategories = adItem.find_elements(By.CLASS_NAME, "adProduct_category__ZIAfP.adProduct_nohover__zHCEV")
    for adItemCategory in adItemCategories:
        categories.append(adItemCategory.text)
    
    # 광고 상품 유무
    ad = True

    # 판매자
    seller = adItem.find_element(By.CLASS_NAME, "adProduct_mall__zeLIC.linkAnchor")
    if seller.text == "": # 판매자 정보가 이미지로 이루어져 있을 경우
        seller = seller.find_element(By.TAG_NAME, "img").get_attribute("alt")
    else: # 판매자 정보가 텍스트로 이루어져 있을 경우
        seller = seller.text
    
    print(title, link, registedDate, price, deliveryFee, categories, ad, seller)

# 광고 제품 처리

# for adItem in adItems:
#     print(adItem.text)
# 미광고 제품 - div > product_inner__gr8QR

# nonadItems = items.find_elements(By.CLASS_NAME, "product_inner__gr8QR")
