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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import keyboard

url = "https://music.yandex.ru/album/18382176/track/91983912?utm_source=desktop&utm_medium=copy_link"


# Path to the cookies file
cookie_file = 'Cookies'

# Create a new instance of the Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Read the cookies from the file


# Add the cookies to the WebDriver session
cookies = (
        (".music.yandex.ru", "true"),
        ("music.yandex.ru", "vSlG9GDjitRU9M3kam8TAvG13JbwxOltHM_R4YdEU-yMQjuuhhcAnJgxY50JPduYo1ppcw380kP8P4ynLi46WedM-XI"),
        ("music.yandex.ru", "''")
)
for cookie in cookies:
    name, value = cookie
    driver.add_cookie({'name': name, 'value': value})

# Open the target URL
driver.get(url)

# Perform the necessary actions
# ...

# Close the WebDriver

keyboard.wait("Esc")
driver.quit()
quit()