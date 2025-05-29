from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import random
from selenium.common.exceptions import NoSuchElementException
import pickle


def init_driver():
    options = ChromeOptions()
    # 사용자 에이전트 설정 (사람처럼 보이도록 위장)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # 브라우저 숨김 실행 시 필요

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # navigator.webdriver 감추기 (탐지 회피)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
        """
    })

    return driver

def is_detail_page(driver):
    # 상세 페이지인지 판단하는 핵심 요소가 있는지 확인
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]")
        return True
    except NoSuchElementException:
        return False

def is_list_page(driver):
    # 리스트 페이지인지 판단
    try:
        driver.find_element(By.CLASS_NAME, "Nv2PK")  # 검색결과 카드 존재 여부
        return True
    except NoSuchElementException:
        return False

def click_first_result(driver):
    # 검색 결과 리스트에서 첫 번째 결과 클릭
    try:
        first_result = driver.find_elements(By.CLASS_NAME, "Nv2PK")[0]
        first_result.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"⚠️ 검색 결과 클릭 실패: {e}")
        return False

def search_place(driver, place_name):
    # 통합된 검색 및 판단 로직
    driver.get("https://www.google.com/maps")
    time.sleep(1.5)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(place_name)
    search_box.send_keys(Keys.ENTER)
    print(f"🔍 '{place_name}' 검색 중...")
    time.sleep(3)

    if is_detail_page(driver):
        print(f"✅ '{place_name}' → 바로 상세 페이지 진입")
        return True

    elif is_list_page(driver):
        print(f"📋 '{place_name}' → 검색 결과 리스트 표시됨")
        if click_first_result(driver):
            if is_detail_page(driver):
                print(f"✅ '{place_name}' → 리스트에서 상세 페이지 진입 성공")
                return True
            else:
                print(f"⚠️ '{place_name}' → 클릭 후에도 상세 페이지 인식 실패")
                return False
        else:
            print(f"❌ '{place_name}' → 첫 결과 클릭 실패")
            return False

    else:
        print(f"❓ '{place_name}' → 상세도 리스트도 아님")
        return False

def click_review_tab(driver):
    try:
        xpath_list = [
            "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]",
            "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]",
            "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]",
            "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]"
        ]

        for xpath in xpath_list:
            try:
                button = driver.find_element(By.XPATH, xpath)
                if "리뷰" in button.text:
                    button.click()
                    print(f"📝 리뷰 탭 클릭 성공: {xpath}")
                    time.sleep(2)
                    return True
            except NoSuchElementException:
                continue

        print("❌ 리뷰 탭 버튼이 존재하지 않거나 '리뷰' 탭이 아님")
        return False

    except Exception as e:
        print(f"🚨 리뷰 탭 클릭 중 오류 발생: {e}")
        return False

def scroll_review_section(driver, max_reviews=50):
    # 스크롤 다운을 통해 리뷰 로드하기
    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf')

    for _ in range(20):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(0.2)

    print(f"📜 리뷰 스크롤 종료")

def extract_reviews(driver, max_reviews=50):
    # 데이터 수집
    # review_elements = driver.find_elements(By.CLASS_NAME, 'wiI7pd')
    try:
        review_elements = driver.find_elements(By.CLASS_NAME, 'wiI7pd')[:max_reviews]
        rating_elements = driver.find_elements(By.CLASS_NAME, 'kvMYJc')[:max_reviews]
        reviews = [element.text for element in review_elements]
        ratings = [element.get_attribute('aria-label') if element.get_attribute('aria-label') else None for element in rating_elements]
        time.sleep(2)
        print(reviews)
        print(ratings)
        return reviews, ratings
    except Exception as e:
        print(f"🚨 리뷰 추출 중 오류 발생: {e}")
        return [], []

def collect_reviews_for_place(driver, max_reviews):
    if not click_review_tab(driver):
        return [], []
    time.sleep(4) # 리뷰 영역 렌더링 대기
    scroll_review_section(driver, max_reviews=max_reviews)
    return extract_reviews(driver, max_reviews=max_reviews)


def main():
    target_name = "무창포타워"  # 🔍 수정할 장소명
    target_url = "https://maps.app.goo.gl/DezCVrez8WdgMYV78"  # 🌐 직접 복사한 Google Maps URL

    # CSV 불러오기
    df = pd.read_csv("./dataset/LES/google_maps_reviews/Chungnam_reviews.csv")

    # 해당 장소 찾기
    idx = df[df["names"] == target_name].index
    if len(idx) == 0:
        print(f"❌ '{target_name}' 해당 행을 찾을 수 없습니다.")
        return
    row_index = idx[0]
    print(f"✅ '{target_name}' 데이터 갱신 시작")

    # 크롬 드라이버 실행 및 URL 접속
    driver = init_driver()
    driver.get(target_url)
    time.sleep(3)

    # 리뷰/평점 크롤링
    try:
        reviews, ratings = collect_reviews_for_place(driver, max_reviews=50)
        df.at[row_index, "reviews"] = ' '.join(reviews)
        df.at[row_index, "rating"] = ' '.join(ratings)
        print(f"📝 리뷰/평점 갱신 완료: {target_name}")
    except Exception as e:
        print(f"⚠️ 크롤링 실패: {e}")
        df.at[row_index, "reviews"] = "?"
        df.at[row_index, "rating"] = "?"

    driver.quit()

    # CSV 덮어쓰기
    df.to_csv("./dataset/LES/google_maps_reviews/Chungnam_reviews.csv", index=False, encoding="utf-8-sig")

    print("✅ 저장 완료")

if __name__ == "__main__":
    main()