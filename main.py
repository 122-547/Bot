#импорт библиотек
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import sqlite3
import requests



class MusicBot: #создание класса
    def __init__(self): #функция инициализации класса
        logging.basicConfig(level=logging.INFO) #создание отправки логгирования программы
        token = "8059535485:AAFbm_vV3jWk_6CTGii0Zk2GHam9bU6wtrA" #токен бота временный
        self.db = sqlite3.connect("database1.db") #подключение к базе данных
        self.cur = self.db.cursor() #создание курсора подключения

        #тут должен быть текст о создателях проекта
        self.admins_info = """ 

        """
        #тут должен быть текст о дополнительной информации, то есть формой сообщения и тд
        self.help = """
        """
        """
        Отправить можно ТОЛЬКО 3 сообщения, после 
        получения ботом 3х сообщений, не включая комманды, бот перестанет как-либо 
        реагировать на ваши сообщения, будьте внимательны, составляя ваши
        предложения.
                """


        #тут должен содержаться текст который будет высвечиваться при запуске бота, то есть при комадне /start
        self.start1 = """

        """


        self.bot = Bot(token) #инициализация бота
        self.dp = Dispatcher(self.bot) #инициализация диспетчера бота
        self.dp.middleware.setup(LoggingMiddleware()) #логгирование процесса

    def start(self): #функция добавляющия обработку ботом коммадны /start
        @self.dp.message_handler(commands=["start"])
        async def start1(message: types.Message):
            await self.send_start_message(message)

    def admins(self): #функция добавляющия обработку ботом коммадны /creators
        @self.dp.message_handler(commands=["creators"])
        async def admins1(message: types.Message):
            await self.send_admins_info_message(message)

    def help_(self): #функция добавляющия обработку ботом коммадны /help (дополнительной информации)
        @self.dp.message_handler(commands=["help"])
        async def help1(message: types.Message):
            await self.send_help_message(message)

    def end(self): #функция окончанию << жизни >> бота
        from aiogram import executor
        executor.start_polling(self.dp)
        self.db.close()

    def get_message(self): #функция добавляющия обработку ботом сообщений отправленных пользователем
        @self.dp.message_handler(content_types="text")
        async def get_message1(message: types.Message):
            b_status = self.check_b_status(message) #находится ли в бан листе
            if not b_status: #если не в бан листе
                    is_new_user = self.is_new_user(message) #проверка на нового пользователя
                    if is_new_user: #если новый пользователь
                        self.add_new_user(message) #добавляем нового пользователя
                    is_new_track = self.check_track_in_db(message) #новый ли трек
                    if is_new_track: #если новый
                        e_status, data = self.message_processing(message) #получаем из сообщения данные
                        if e_status == "error":
                            await data, self.send_m_count_message(message), self.add_m_count_user(message)
                        else:
                            self.add_new_track_in_db(data, message) #добавляем новый трек в дб
                            await self.send_m_count_message(message), self.add_m_count_user(message)
                    else: #если не новый
                        self.add_existing_track_in_db(message) #добавляем к существующему треку в дб
                        await self.send_m_count_message(message), self.add_m_count_user(message)
                    
            
    def message_processing(self, message): #обработка сообщения, делит сообщение, составленное по форме на имя автора и название трека
        url = message.text
        parts = url.split('/')
        track_index = parts.index('album')
        album_id = parts[track_index + 1].split('/')[0]
        api_url = "https://api.music.yandex.net/albums/" + album_id
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                time = None
                response_data = response.json()
                name = response_data['result']['title']
                artists = response_data['result']['artists']
                authors = ''
                for artist in artists:
                    name1 = artist['name']
                    authors = authors + name1 + ", "
                author = authors[:-2]
                data = {
                    "time": time,
                    "name": name.text,
                    "author": author.text
                    }
                return "not-found", data
        except requests.exceptions.MissingSchema:
            return "error", message.answer("Ссылка некорректна.")

        except AttributeError:
            return "error", message.answer("Не так быстро.")
        

    def send_admins_info_message(self, message): #функция, возвращающая отправку ботом сообщения с информацией о создателях проекта
        return message.answer(self.admins_info)

    def send_start_message(self, message): #функция, возвращающая отправку ботом сообщения после запуска
        return message.answer(self.start1)

    def send_help_message(self, message): #функция, возвращающая отправку ботом сообщения-справки
        return message.answer(self.help)
    
    def send_m_count_message(self, message): #функция, возвращающая отправку ботом сообщения о колличестве оставшихся сообщений до блокировки ботом пользователя
        id_ = str(message['from'].id)
        m_count = self.cur.execute(f"SELECT m_count FROM users WHERE id = {id_}")
        m_count = [i for i in [g for g in m_count][0]][0]
        m_count_difference = 2 - m_count
        if m_count_difference != 0:
            return message.answer(f"Ваше сообщение было успешно отправлено на обработку, у вас осталось {m_count_difference} доступных сообщений")
        else: 
            return message.answer("У больше не осталось доступных сообщений, спасибо за участие. Ваши последующие сообщения не будут обрабатываться ботом.")

    def check_b_status(self, message): #функция, проверяющия заблокирован ли пользователь ботом или нет
        id_ = str(message['from'].id)
        select = self.cur.execute(f"SELECT b_status FROM users WHERE id = {id_}")
        try:
            result = [i for i in [g for g in select][0]][0]
            if result == "BAN":
                return True
        except:
            return False
        

    def is_new_user(self, message): #функция, проверяющия пользователь который отправил сообщене новый или нет
        id_ = str(message['from'].id) 
        select = self.cur.execute(f"SELECT id FROM users WHERE id = {id_}")
        result = [i for i in select]
        if result == []:
            return True
        else:
            return False

    def add_new_user(self, message): #функция, добавляющая нового пользователя в базу данных
        username = message['from'].username
        id_ = str(message['from'].id)
        m_count = 0
        self.cur.execute("INSERT INTO users (username, id, m_count) VALUES (?, ?, ?)", (username, id_, m_count))
        self.db.commit()
    
    def add_m_count_user(self, message): #функция обновляющая колличество оставшихся у пользователя сообщений до блокировки ботом
        id_ = str(message['from'].id)
        m_count = self.cur.execute(f"SELECT m_count FROM users WHERE id = {id_}")
        m_count = [i for i in [g for g in m_count][0]][0]
        m_count += 1
        self.cur.execute("UPDATE users SET m_count = ? WHERE id = ?", (m_count, id_))
        if m_count == 3:
            self.cur.execute("UPDATE users SET b_status = ? WHERE id = ?", ('BAN', id_))
        self.db.commit()

    def check_track_in_db(self, message): #функция, проверяющая находится ли предложенный трек в базе данных или нет
        url = message.text
        select = self.cur.execute("SELECT url FROM tracks WHERE url = ?", (url,))
        result = [i for i in select]
        if result == []:
            return True
        else:
            return False
        
        
    def add_new_track_in_db(self, data, message): #функция, добавляющая новый предложенный трек в базу данных
        track_name = data['name']
        author = data['author']
        time = data['time']
        self.cur.execute("INSERT INTO tracks (name, author, time, v_count, url) VALUES (?, ?, ?, ?, ?)", (track_name, author, time, 1, message.text))
        self.db.commit()

    def add_existing_track_in_db(self, message): #функция, добавляющая существующий в базе данных предложенный трек (обновляет колличество предложений данного трека в базе данных)
        url = message.text
        v_count = self.cur.execute("SELECT v_count FROM tracks WHERE url = ?", (url,))
        v_count = [i for i in [g for g in v_count][0]][0]
        v_count += 1
        self.cur.execute("UPDATE tracks SET v_count = ? WHERE url = ?", (v_count, url))
        self.db.commit()
    

#запуск бота просто
#вызов нужных для работы бота функций, прописанных в классе

bot = MusicBot()
bot.start()
bot.admins()
bot.help_()
bot.get_message()
bot.end()


#upd 22.11.24
"""
на данный момент времени не получается добиться постоянного парсина информации с сайта без угрозы капчи
и перевода на другую страницу

что делать с переводом на другую страницу:
1. оформить скрипт через selenium
то есть:
если нужных нам элементов не находится на странице, то мы с помощью silenium находим элемент для закрытия данной страницы
и получаем код страницы, которая нам нужна для дальнейшего парса

что делать с капчей:
1. попробовать пострадать херней с куки файлами, потому что можно получить куки после личного прохода капчи и после чего
просто подгружать корректные куки при попадании на капчу, но с этим нужно еще разобраться

2. каким-либо другим способом попытаться реализоавть либо обход либо еще что-то с капчей

3. программу поиска можно попробовать реализовать на api яндекс музыки, не думаю что там будет присутствовать капча при постоянных запросах
но в этом так же нужно будет разобраться. для этого способа нам нужно как либо получать информацию именно из ссылки, то есть id трека и id альбома
после чего через них нахоидть по api такие данные как (название трека, его исполнитель, длительнойсть) если это все получится реализовать, то это
простейшим из всех способов, но это при условии если не будет капчи на api-шке

"""