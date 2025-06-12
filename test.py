import requests
import trafilatura
from bs4 import BeautifulSoup
import re

# 추천 게시판 URL (원신 갤러리)
url = 'https://gall.dcinside.com/mgallery/board/lists/?id=onshinproject&exception_mode=recommend'

# DC인사이드에서는 User-Agent가 필요할 수 있음
headers = {
    'User-Agent': 'Mozilla/5.0'
}

response = requests.get(url, headers=headers)

# HTML 파싱
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 게시글 번호 추출: <tr> 태그들 중 data-no 속성이 있는 것만 필터링
    post_list = soup.select('tr.ub-content[data-no]')
    post_numbers = [tr['data-no'] for tr in post_list if tr.has_attr('data-no')]

    print("추천 게시글 번호 리스트:")
    for num in post_numbers:
        print(num)
else:
    print("요청 실패:", response.status_code)
