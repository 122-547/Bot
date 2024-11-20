# from bs4 import BeautifulSoup
# import requests
# url = "https://music.yandex.ru/album/33000988/track/130423345?utm_source=desktop&utm_medium=copy_link"
# soup = BeautifulSoup(requests.get(url).text, "html.parser")

# name = soup.find(class_="sidebar__title sidebar-track__title deco-type typo-h2")
# author = soup.find(class_="sidebar__info sidebar__info-short")
# print(name.text, author.text)

import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()

cur.execute("CREATE TABLE tracks(name TEXT, author TEXT, v_count INTEGER, url TEXT)")
db.close()