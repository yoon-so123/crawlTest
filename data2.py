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
base_url = "https://gall.dcinside.com/mgallery/board/lists/?id=onshinproject&page=2&exception_mode=recommend"
start_page = 37
num_posts_to_scrape = 100
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
csv_filename = "원신_5.7_유저반응_크롤링.csv"
with open(csv_filename, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'content', 'comments'])
    writer.writeheader()
    for item in results:
        writer.writerow(item)

print(f"\n✅ CSV 저장 완료: {csv_filename}")

# 드라이버 종료
driver.quit()