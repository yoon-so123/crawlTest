import requests
import trafilatura
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# -----------------------------------------
# 1. 게시글 번호 수집 (trafilatura 사용)
# -----------------------------------------

def get_post_numbers_with_trafilatura(gallery_id='onshinproject'):
    url = f'https://gall.dcinside.com/mgallery/board/lists/?id={gallery_id}&exception_mode=recommend'
    downloaded = trafilatura.fetch_url(url)
    
    if downloaded:
        html = trafilatura.bare_extraction(downloaded, include_comments=False, include_tables=False)
        # 하지만 게시글 번호는 html 구조에서 가져와야 하므로 BeautifulSoup도 함께 사용
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
    return content_text, comments

# -----------------------------------------
# 3. 실행 로직
# -----------------------------------------

if __name__ == "__main__":
    gallery_id = 'onshinproject'
    post_numbers = get_post_numbers_with_trafilatura(gallery_id)

    print(f"✅ 추천 게시글 {len(post_numbers)}개 수집됨\n")

    for i, post_no in enumerate(post_numbers, 1):  # 상위 3개만 예시로 실행
        print(f"\n📌 {i}. 게시글 번호: {post_no}")
        content, comments = scrape_post_content_and_comments(post_no, gallery_id)

        print("📄 본문:\n", content)
        print("💬 댓글:")
        for idx, comment in enumerate(comments, 1):
            print(f"  {idx}. {comment}")
        print("-" * 60)
