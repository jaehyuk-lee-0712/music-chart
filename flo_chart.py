import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import selenium 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime

import json
from collections import OrderedDict

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"chart_flo100_{current_date}.json"

# Chrome 옵션 설정
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

browser.get('https://www.music-flo.com/browse')

WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "chart_lst"))
)

# "더보기" 버튼을 찾아 클릭
try:
    more_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn_list_more"))
    )
    if more_button:
        browser.execute_script("arguments[0].click();", more_button)
        print("Clicked '더보기' button.")
        time.sleep(3)
except Exception as e:
    print("Error clicking '더보기':", e)


# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
music_data = []
tracks = soup.select(".chart_lst .track_list_table tbody tr")
for track in tracks:
    rank = track.select_one(".num").text.strip()
    title = track.select_one(".tit__text").text.strip()
    artist = track.select_one(".artist__link").text.strip()
    album = track.select_one(".album").text.strip()
    image_url = track.select_one(".thumb img").get('src')

    music_data.append({
        "rank": rank,
        "title": title,
        "artist": artist,
        "imageURL": image_url,
        "album": album
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(music_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()

time.sleep(10)
