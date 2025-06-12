from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# 크롬 드라이버 자동 설치 (없다면 주석 제거하고 사용)
# pip install webdriver-manager
# from webdriver_manager.chrome import ChromeDriverManager

# 크롬 옵션 설정
options = Options()
options.add_argument("--headless")  # 창 띄우지 않음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")

# 크롬 드라이버 실행
driver = webdriver.Chrome(options=options)  # ChromeDriverManager().install() 사용 가능

# 크롤링할 게시글 URL
url = 'https://gall.dcinside.com/mgallery/board/view/?id=onshinproject&no=14868890&exception_mode=recommend&page=1'
driver.get(url)

# 페이지 로딩 대기
time.sleep(2)  # 필요시 늘리세요

# 페이지 소스 파싱
soup = BeautifulSoup(driver.page_source, 'html.parser')

### ✅ 본문 추출
content_area = soup.select_one('div.write_div')  # 게시글 본문 영역
content_text = content_area.get_text(strip=True) if content_area else "[본문 없음]"

print("📄 본문 내용:\n", content_text)

### ✅ 댓글 추출
comments = []
comment_items = soup.select('ul.cmt_list > li.ub-content')

for li in comment_items:
    text_tag = li.select_one('.usertxt')
    if text_tag:
        comment = text_tag.get_text(strip=True)
        comments.append(comment)

print("\n💬 댓글 목록:")
for i, comment in enumerate(comments, 1):
    print(f"{i}. {comment}")

driver.quit()
