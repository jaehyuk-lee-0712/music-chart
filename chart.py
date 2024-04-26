import requests as req 
from bs4 import BeautifulSoup as bs
import pandas as pd 

res = req.get("https://music.bugs.co.kr/chart")

soup = bs(res.text , 'lxml')

ranking = soup.select(".ranking > strong")
title = soup.select(".title > a")
artist = soup.select(".artist >a:nth-child(1)")

#test

rankingList = []
titleList = []
artistList = []

rankingList = [rank.text.strip() for rank in ranking]
titleList = [title.text.strip() for title in title]
artistList = [art.text.strip() for art in artist]

chart_df = pd.DataFrame({
    "Ranking" : rankingList,
    "Title" : titleList , 
    "Artist" : artistList
})

chart_df.to_json("bugsMusicChart100.json", force_ascii=False , orient="records")
    
