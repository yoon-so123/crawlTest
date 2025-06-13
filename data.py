# # 텍스트 처리
# import pandas as pd
# import re
# from collections import Counter

# # 형태소 분석기 (명사 추출)
# from konlpy.tag import Okt

# # 시각화
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# # -----------------------------------------
# # 1. 데이터 로딩
# # -----------------------------------------

# # 데이터 불러오기
# df = pd.read_csv("dcinside_posts.csv")

# # 모든 텍스트 결합
# all_text = df['title'].fillna('') + ' ' + df['content'].fillna('') + ' ' + df['comments'].fillna('')
# all_text = ' '.join(all_text.tolist())

# # 형태소 분석
# okt = Okt()
# nouns = okt.nouns(all_text)

# # 한 글자 제외하고 상위 키워드 추출
# filtered = [n for n in nouns if len(n) > 1]
# counter = Counter(filtered)
# top_keywords = counter.most_common(50)

# # 출력
# print("📌 상위 50개 키워드:")
# for word, freq in top_keywords:
#     print(f"{word}: {freq}")
# # 워드클라우드 생성


# import shutil
# import os

# # 경로 설정 (data.py 기준으로 상위 폴더로 올라감)
# source_folder = '../genshin_notice_project/'
# target_folder = './'  # 현재 폴더인 crawlTest

# # 복사할 파일 목록
# files_to_copy = ['원신_업데이트_통합본.csv', '원신_이벤트_리스트_정리본.csv']

# # 파일 복사 실행
# for file_name in files_to_copy:
#     src = os.path.join(source_folder, file_name)
#     dst = os.path.join(target_folder, file_name)
#     shutil.copy(src, dst)
#     print(f'{file_name} 복사 완료!')

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import time
# import csv

# # 1. 크롬 옵션 설정
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("user-agent=Mozilla/5.0")

# # 2. 드라이버 실행
# driver = webdriver.Chrome(options=options)

# # 3. 크롤링할 목록 페이지 URL
# base_url = "https://gall.dcinside.com/mgallery/board/lists/?id=onshinproject&page="
# start_page = 37
# num_posts_to_scrape = 50
# post_links = []

# # 4. 목록에서 게시글 링크 수집 (여러 페이지 돌면서)
# while len(post_links) < num_posts_to_scrape:
#     driver.get(base_url + str(start_page))
#     time.sleep(2)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     rows = soup.select('tbody > tr.ub-content')
    
#     for row in rows:
#         a_tag = row.select_one('td.gall_tit > a[href]')
#         if a_tag and 'view' in a_tag['href']:
#             link = "https://gall.dcinside.com" + a_tag['href']
#             post_links.append(link)
#             if len(post_links) >= num_posts_to_scrape:
#                 break
#     start_page += 1

# print(f"✅ {len(post_links)}개의 게시글 링크 수집 완료")

# # 5. 게시글 본문+댓글 추출
# results = []

# for idx, url in enumerate(post_links):
#     driver.get(url)
#     time.sleep(1)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # 본문
#     content_area = soup.select_one('div.write_div')
#     content_text = content_area.get_text(strip=True) if content_area else "[본문 없음]"

#     # 댓글
#     comments = []
#     comment_items = soup.select('ul.cmt_list > li.ub-content')
#     for li in comment_items:
#         text_tag = li.select_one('.usertxt')
#         if text_tag:
#             comments.append(text_tag.get_text(strip=True))
    
#     results.append({
#         'url': url,
#         'content': content_text,
#         'comments': " | ".join(comments) if comments else "[댓글 없음]"
#     })

#     print(f"📄 ({idx+1}) 게시글 수집 완료")

# # 6. CSV 저장 (한글 인코딩 포함)
# csv_filename = "원신_5.6_유저반응_크롤링.csv"
# with open(csv_filename, mode='w', encoding='utf-8-sig', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=['url', 'content', 'comments'])
#     writer.writeheader()
#     for item in results:
#         writer.writerow(item)

# print(f"\n✅ CSV 저장 완료: {csv_filename}")

# # 드라이버 종료
# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

# 1. 크롬 옵션 설정
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")

# 2. 드라이버 실행
driver = webdriver.Chrome(options=options)

# 3. 크롤링할 목록 페이지 URL
base_url = "https://gall.dcinside.com/mgallery/board/lists/?id=onshinproject&page="
start_page = 37
num_posts_to_scrape = 50
post_links = []

# 4. 목록에서 제목 + 링크 수집
while len(post_links) < num_posts_to_scrape:
    driver.get(base_url + str(start_page))
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.select('tbody > tr.ub-content')
    
    for row in rows:
        a_tag = row.select_one('td.gall_tit > a[href]')
        if a_tag and 'view' in a_tag['href']:
            link = "https://gall.dcinside.com" + a_tag['href']
            title = a_tag.text.strip()
            post_links.append({
                'title': title,
                'url': link
            })
            if len(post_links) >= num_posts_to_scrape:
                break
    start_page += 1

print(f"✅ {len(post_links)}개의 게시글 제목+링크 수집 완료")

# 5. 게시글 본문+댓글 수집
results = []

for idx, post in enumerate(post_links):
    url = post['url']
    title = post['title']
    
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 본문
    content_area = soup.select_one('div.write_div')
    content_text = content_area.get_text(strip=True) if content_area else "[본문 없음]"

    # 댓글
    comments = []
    comment_items = soup.select('ul.cmt_list > li.ub-content')
    for li in comment_items:
        text_tag = li.select_one('.usertxt')
        if text_tag:
            comments.append(text_tag.get_text(strip=True))
    
    results.append({
        'title': title,
        'content': content_text,
        'comments': " | ".join(comments) if comments else "[댓글 없음]"
    })

    print(f"📄 ({idx+1}) {title[:30]}... 수집 완료")

# 6. CSV 저장
csv_filename = "원신_5.6_유저반응_크롤링.csv"
with open(csv_filename, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'content', 'comments'])
    writer.writeheader()
    for item in results:
        writer.writerow(item)

print(f"\n✅ CSV 저장 완료: {csv_filename}")


additional_links = []
start_page = 39  # 기존 마지막 페이지보다 +1

while len(additional_links) < 50:
    driver.get(base_url + str(start_page))
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.select('tbody > tr.ub-content')
    
    for row in rows:
        a_tag = row.select_one('td.gall_tit > a[href]')
        if a_tag and 'view' in a_tag['href']:
            link = "https://gall.dcinside.com" + a_tag['href']
            title = a_tag.text.strip()
            additional_links.append({
                'title': title,
                'url': link
            })
            if len(additional_links) >= 50:
                break
    start_page += 1

print(f"➕ 추가 50개 게시글 링크 수집 완료")

# 50개 더 본문/댓글 크롤링
for idx, post in enumerate(additional_links):
    url = post['url']
    title = post['title']
    
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 본문
    content_area = soup.select_one('div.write_div')
    content_text = content_area.get_text(strip=True) if content_area else "[본문 없음]"

    # 댓글
    comments = []
    comment_items = soup.select('ul.cmt_list > li.ub-content')
    for li in comment_items:
        text_tag = li.select_one('.usertxt')
        if text_tag:
            comments.append(text_tag.get_text(strip=True))
    
    results.append({
        'title': title,
        'content': content_text,
        'comments': " | ".join(comments) if comments else "[댓글 없음]"
    })

    print(f"📄 ({idx+51}) 추가 게시글 수집 완료")

# 다시 CSV 저장
csv_filename = "원신_5.6_유저반응_크롤링_100개.csv"
with open(csv_filename, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'content', 'comments'])
    writer.writeheader()
    for item in results:
        writer.writerow(item)

print(f"\n✅ 전체 100개 CSV 저장 완료: {csv_filename}")
driver.quit()