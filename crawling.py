from utils import *
from selenium.webdriver.common.by import By

driver_path = '/Users/choiwonwong/STUDY/NS_CRAWL/chromedriver-mac-arm64/chromedriver'

def crawlItems(elements, subDriver):
    items = []
    for e in elements:
        # 아이템 제목
        title = e.find_element(By.CLASS_NAME, "product_link__TrAac.linkAnchor").text

        # SDP Link
        redirectLink = e.find_element(By.CLASS_NAME, "product_link__TrAac.linkAnchor").get_attribute("href")
        try:
            subDriver.get(redirectLink)
            link = subDriver.current_url
        except:
            link = "수집된 SDP는 유효하지 않습니다."

        # 둥록 일자
        registedDate = e.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div[4]/div[1]/div[2]/div/div[14]/div/div/div[2]/div[5]/span[1]").text[4:]
        
        # 가격
        try: 
            price = e.find_element(By.CLASS_NAME, "price_num__S2p_v").text
        except:
            price = "판매 중단"
        
        # 배송비
        deliveryFee = e.find_element(By.CLASS_NAME, "price_delivery__yw_We").text.split()[-1]

        # 카테고리
        categories = []
        adElementCategories = e.find_elements(By.CLASS_NAME, "product_category__l4FWz.product_nohover__Z0Muw")
        for adElementCategory in adElementCategories:
            categories.append(adElementCategory.text)
        categories = " > ".join(categories)
        # 광고 유무
        ad = False

        # 판매자
        try: 
            sellerElement  = e.find_element(By.CLASS_NAME, "product_mall__hPiEH.linkAnchor")
            if sellerElement.text == "":
                seller= sellerElement.find_element(By.TAG_NAME, "img").get_attribute("alt")
            else:
                seller= sellerElement.text
        except:
            seller = "추가 처리 필요"
        
        item = {
            "title": title,
            "link": link,
            "price": price,
            "deliveryFee": deliveryFee,
            "registedDate": registedDate,
            "category": categories,
            "ad": ad,
            "seller": seller
            }
        items.append(item)
    return items

# 광고 상품 크롤링
def crawlAdItems(adElements, subDriver):
    adItems = []
    for adElement in adElements:
        # 아이템 제목
        title = adElement.find_element(By.CLASS_NAME, "adProduct_link__NYTV9.linkAnchor").text

        # SDP Link
        redirectLink = adElement.find_element(By.CLASS_NAME, "adProduct_link__NYTV9.linkAnchor").get_attribute("href")
        try:
            subDriver.get(redirectLink)
            link = subDriver.current_url
        except:
            link = "수집된 SDP는 유효하지 않습니다."

        # 둥록 일자
        registedDate = adElement.find_element(By.CLASS_NAME, "adProduct_etc_box__UJJ90").find_element(By.TAG_NAME, "span").text[4:]

        # 가격
        try: 
            price = adElement.find_element(By.CLASS_NAME, "price_num__S2p_v").text
        except:
            price = "판매 중단"
        
        # 배송비
        deliveryFee = adElement.find_element(By.CLASS_NAME, "price_delivery__yw_We").text.split()[-1]

        # 카테고리
        categories = []
        adElementCategories = adElement.find_elements(By.CLASS_NAME, "adProduct_category__ZIAfP.adProduct_nohover__zHCEV")
        for adElementCategory in adElementCategories:
            categories.append(adElementCategory.text)
        categories = " > ".join(categories)
        
        # 광고 유무
        ad = True

        # 판매자
        sellerElement  = adElement.find_element(By.CLASS_NAME, "adProduct_mall__zeLIC.linkAnchor")
        if sellerElement.text == "":
            seller= sellerElement.find_element(By.TAG_NAME, "img").get_attribute("alt")
        else:
            seller= sellerElement.text
        
        adItem = {
            "title": title,
            "link": link,
            "price": price,
            "deliveryFee": deliveryFee,
            "registedDate": registedDate,
            "category": categories,
            "ad": ad,
            "seller": seller
            }
        adItems.append(adItem)
    return adItems