import requests
import trafilatura
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

# -----------------------------------------
# 1. 게시글 번호 수집 (trafilatura 사용)
# -----------------------------------------

def get_post_numbers_with_trafilatura(gallery_id='onshinproject'):
    url = f'https://gall.dcinside.com/mgallery/board/lists/?id={gallery_id}&exception_mode=recommend'
    downloaded = trafilatura.fetch_url(url)
    
    if downloaded:
        soup = BeautifulSoup(downloaded, 'html.parser')
        post_list = soup.select('tr.ub-content[data-no]')
        return [tr['data-no'] for tr in post_list if tr.has_attr('data-no')]
    else:
        print("트라필라투라 다운로드 실패")
        return []

# -----------------------------------------
# 2. 본문 + 댓글 수집 (Selenium 사용)
# -----------------------------------------

def scrape_post_content_and_comments(post_number, gallery_id='onshinproject'):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)

    url = f'https://gall.dcinside.com/mgallery/board/view/?id={gallery_id}&no={post_number}&exception_mode=recommend'
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 제목
    title_tag = soup.select_one('span.title_subject')
    title_text = title_tag.get_text(strip=True) if title_tag else "[제목 없음]"

    # 본문
    content_area = soup.select_one('div.write_div')
    content_text = content_area.get_text(strip=True) if content_area else "[본문 없음]"

    # 댓글
    comments = []
    comment_items = soup.select('ul.cmt_list > li.ub-content')
    for li in comment_items:
        text_tag = li.select_one('.usertxt')
        if text_tag:
            comment = text_tag.get_text(strip=True)
            comments.append(comment)

    driver.quit()
    return title_text, content_text, comments

# -----------------------------------------
# 3. 실행 로직 + CSV 저장
# -----------------------------------------

if __name__ == "__main__":
    gallery_id = 'onshinproject'
    post_numbers = get_post_numbers_with_trafilatura(gallery_id)

    print(f"✅ 추천 게시글 {len(post_numbers)}개 수집됨\n")

    # CSV 파일 열기
    with open('dcinside_posts.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['게시번호', '제목', '본문내용', '댓글내용'])  # 헤더

        for i, post_no in enumerate(post_numbers, 1):
            print(f"📥 ({i}/{len(post_numbers)}) 게시글 번호: {post_no}")
            try:
                title, content, comments = scrape_post_content_and_comments(post_no, gallery_id)
                comment_text = " || ".join(comments) if comments else "[댓글 없음]"
                writer.writerow([post_no, title, content, comment_text])
            except Exception as e:
                print(f"❌ 오류 (게시글 번호 {post_no}): {e}")
