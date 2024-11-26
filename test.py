#test
# import requests

# # Ваши данные для авторизации
# client_id = '05fa1ae8bc7948488b739af3ddb38ce1'
# client_secret = 'b671e77626b94bb28ce5b53d123c5110'
# access_token = ''

# # ID трека
# track_id = 'YOUR_TRACK_ID'

# # URL для получения информации о треке
# track_info_url = f'https://music.yandex.ru/handlers/track.jsx?trackId={track_id}'

# # Заголовки для авторизации
# headers = {
#     'Authorization': f'OAuth {access_token}',
#     'Accept': 'application/json'
# }

# # Выполнение запроса
# response = requests.get(track_info_url, headers=headers)

# # Проверка успешности запроса
# if response.status_code == 200:
#     track_info = response.json()
#     print(f"Название трека: {track_info['title']}")
#     print(f"Автор(ы): {track_info['artists']}")
#     print(f"Длительность трека: {track_info['duration']} секунд")
# else:
#     print(f"Ошибка при получении информации о треке: {response.status_code}")
# import requests

# # Ваши данные для авторизации
# client_id = '05fa1ae8bc7948488b739af3ddb38ce1'
# client_secret = 'b671e77626b94bb28ce5b53d123c5110'
# redirect_uri = 'https://my.bot.com/feed'
# authorization_url = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'

# print(f'Please go to the following URL and authorize the application: {authorization_url}')

# # После успешной авторизации вы получите код авторизации
# code = 'YOUR_AUTHORIZATION_CODE'
# token_url = 'https://oauth.yandex.ru/token'
# token_data = {
#     'grant_type': 'authorization_code',
#     'code': code,
#     'redirect_uri': redirect_uri,
#     'client_id': client_id,
#     'client_secret': client_secret
# }

# response = requests.post(token_url, data=token_data)
# tokens = response.json()
# access_token = tokens['access_token']
# print(f'Access Token: {access_token}')

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.options import Options

# import json

# urls = ["https://api.music.yandex.net/albums/18586471", "https://api.music.yandex.net/albums/29436638"]



# try:
#     option = webdriver.FirefoxOptions()
    # option.add_argument("--headless")
    # option.set_preference('dom.webdriver.enabled', False) 
    # option.set_preference('permissions.default.image', 2)
    # option.set_preference('permissions.default.stylesheet', 2)
    
#     for url in urls:
#         driver = webdriver.Firefox(options=option)
#         driver.get(url)
#         json_element = driver.find_element(By.TAG_NAME, 'body')  # или 'div', 'pre' и т.д.
#         json_text = json_element.text
#         json_data = json.loads(json_text)
#         name = json_data['result']['title']
#         artists = json_data['result']['artists']
#         # authors = ''
#         # for artist in artists:
#         #     name1 = artist['name']
#         #     authors = authors + name1 + ", "
#         # author = authors[:-2]
#         print(artists)
#         print(name)
#         driver.quit()
        
# except Exception as e:
#     print(e)

# # finally:
# #     driver


# # # Add the cookies to the WebDriver session
# # cookies = (
# #         (".music.yandex.ru", "true"),
# #         ("music.yandex.ru", "vSlG9GDjitRU9M3kam8TAvG13JbwxOltHM_R4YdEU-yMQjuuhhcAnJgxY50JPduYo1ppcw380kP8P4ynLi46WedM-XI"),
# #         ("music.yandex.ru", "''")
# # )
# # for cookie in cookies:
# #     name, value = cookie
# #     driver.add_cookie({'name': name, 'value': value})

# # # Open the target URL
# # driver.get(url)

# # # Perform the necessary actions
# # # ...

# # # Close the WebDriver






# import requests

# # Функция для получения информации о треке
# def get_track_info(track_id, album_id):
#     # URL для запроса к API Яндекс.Музыки
#     api_url = 

#     # Выполнение запроса
#     response = requests.get(api_url)

#     # Проверка успешности запроса
#     if response.status_code == 200:
#         # Получение данных в формате JSON
#         data = response.json()
#         name = data['result']['title']
#         artists = data['result']['artists']
#         authors = ''
#         print(data)
#         for artist in artists:
#             name1 = artist['name']
#             authors = authors + name1 + ", "
#         authors = authors[:-2]
#         print(name, authors)

        # track_name = track_info.get('title', 'Неизвестно')
        # artist_name = artist_info.get('name', 'Неизвестно')
        # duration = track_info.get('duration', 'Неизвестно')

        # Вывод информации
    #     print(f"Название трека: {track_name}")
    #     print(f"Исполнитель: {artist_name}")
    #     print(f"Длительность: {duration} секунд")
    # else:
    #     print(f"Ошибка при выполнении запроса: {response.status_code}")

# # Пример использования
# track_id = "52622457"
# album_id = "7417212"
# get_track_info(track_id, album_id)

# import logging
# import datetime
# def start_logging():
#     date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#     with open("py.log", "a") as file:
#         file.write(f"[{date}]\n")
#     logging.basicConfig(level=logging.DEBUG, filename="py.log", filemode="a")
#     logging.info("info message")
    
    
# start_logging()

import sqlite3
db = sqlite3.connect("database.db")
cur = db.cursor()

cur.execute("create table users(username text, id text, m_count integer, b_status text)")
cur.execute("create table track(name text, author text, v_count integer, url text)")
# url = "https://music.yandex.ru/album/27144648/track/116818436?utm_source=desktop&utm_medium=copy_link"
# parts = url.split('/')
# track_index = parts.index('track')
# track_id = parts[track_index + 1].split('?')[0]
# print(track_id)