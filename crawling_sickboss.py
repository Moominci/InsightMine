# -*- coding: utf-8 -*-

import pandas as pd
import time
import sys
# import slack_file_upload
import file_date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 현재날짜 기준, 양식에 맞게 날짜 가져오기
today_form = file_date.print_date()

# 검색할 날짜를 입력받아오기
arg = sys.argv
Search_date = arg[1] + arg[2] if len(arg) > 1 else '1d'
print(f"Search_date: {Search_date}")

# 크롤링한 데이터를 저장할 리스트
dataset = []

# 게시글 전처리 함수
def clean_article(list_len):
    while len(list_len) > 4:
        list_len.pop(2)
    try:
        list_len.remove('new')
    except ValueError:
        pass

# 크롬 드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-gpu')
options.add_argument('--lang=ko_KR')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36")

# 드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 로그인 및 초기 설정
def login():
    driver.get('https://www.naver.com/')
    driver.find_element(By.CLASS_NAME, 'link_login').click()
    time.sleep(1)

    # 로그인 정보 입력
    # id : id
    # pw : password
    driver.execute_script("""
        document.getElementById("id").value = "---";
        document.getElementById("pw").value = "---";
    """)
    time.sleep(2)
    driver.find_element(By.ID, 'log.login').click()

# 게시글 수집 함수
def collect_articles(articles_link):
    for i, article in enumerate(articles_link):
        article_texts = driver.find_elements(By.CSS_SELECTOR, 'div > div > table > tbody > tr')[i].text.split('\n')
        clean_article(article_texts)

        article.click()
        time.sleep(1)
        
        # 게시글 내용 수집
        try:
            content = driver.find_element(By.CLASS_NAME, 'se-main-container').text
        except:
            content = driver.find_element(By.CLASS_NAME, 'ContentRenderer').text

        article_texts.append(content.replace('\n', ' '))
        dataset.append(article_texts)
        
        driver.back()
        driver.switch_to.frame('cafe_main')

# 키워드 크롤링 함수
def keyword_search(keyword):
    menu_id_dict = {'음식': 460, '카페': 461, '호프': 463, 'pc방': 464, '편의점': 468}
    key_word_dict = {'식자재': '%BD%C4%C0%DA%C0%E7', '카레': '%EC%B9%B4%EB%A0%88%0A', '추천': '%C3%DF%C3%B5%26'}
    menu_id = menu_id_dict.get('음식', 460)
    key_word = key_word_dict.get(keyword, '%C3%DF%C3%B5%26')

    # 네이버 카페 링크로 이동
    search_url = f'https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=23611966&search.menuid={menu_id}&search.searchdate={Search_date}&search.query={key_word}&search.page=1'
    driver.get(search_url)
    driver.switch_to.frame('cafe_main')

    # 페이지 순회하여 게시글 수집
    for page_num in range(1, 21):
        articles_link = driver.find_elements(By.CSS_SELECTOR, 'a.article')
        collect_articles(articles_link)

        # 다음 페이지로 이동
        try:
            if page_num % 10 == 0:
                driver.find_element(By.LINK_TEXT, '다음').click()
            else:
                driver.find_element(By.LINK_TEXT, str(page_num + 1)).click()
        except:
            break

# 메인 크롤링 실행 함수
def main():
    login()
    keywords = ['강남구', '광진구', '성동구', '마포구', '식자재', '업체', '추천', '어플']
    
    # 페이지가 너무 빠르게 넘어가면 오류 발생
    # delay 
    for keyword in keywords:
        keyword_search(keyword)
        time.sleep(1)
    
    driver.quit()
    # 크롤링 결과 excel 파일로 저장
    pd.DataFrame(dataset, columns=['게시글 번호', '게시글 제목', '작성자', '작성시간/조회수', '게시글 내용']).to_excel(f'sick_boss.xlsx', encoding='utf-8')
    
    # 생성된 파일 Slack에 업로드
    # file_name = f'아프니까사장이다_{Search_date}.xlsx' if len(arg) > 1 else f'아프니까사장이다_{today_form}.xlsx'
    # slack_file_upload.upload('#data_crawling', 'sick_boss.xlsx', file_name, 'xlsx')

# 실행
if __name__ == "__main__":
    main()
