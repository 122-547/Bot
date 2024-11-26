#импорт библиотек
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import sqlite3
import requests
import datetime
import validators



class MusicBot: #создание класса
    def __init__(self): #функция инициализации класса
        logging.basicConfig(filename="bot.log", filemode="a", level=logging.INFO) #настройка логирования программы
        token = "7876319768:AAE0ywpZz1UHYFZoH4Ylv5UmPn1dacHiN2k" #токен бота временный
        
        self.db = sqlite3.connect("database.db") #подключение к базе данных
        self.cur = self.db.cursor() #создание курсора подключения
        try:
            self.cur.execute("create table users(username text, id text, m_count integer, b_status text)")
            self.cur.execute("create table tracks(name text, author text, v_count integer, url text)")
        except sqlite3.OperationalError:
            pass
        self.last_message = """ 
У Вас больше не осталось доступных сообщений, спасибо за участие\. Ваши последующие сообщения не будут обрабатываться ботом\.
        
Дополнительную информацию о проведении дискотеки вы можете получить в нашем [телеграмм канале](https://t.me/discoterr)\.

\[ *Бот создан при поддержке президента лицейского парламента и глав лицейских комитетов* \]
        """
        
        self.info = """
Данный проект работает в паре с сервисом *Яндекс Музыка*, следовательно вам нужно просто отправить ссылку на трек, который вы хотите услышать\.

Для этого вам следует: _перейти в_ *Яндекс Музыку* \=\> _найти нужный вам трек_ \=\> _нажать на_ *⋮* \=\> *Поделиться* \=\> *Скопировать ссылку* \=\> _отправить полученную ссылку боту_\.

Предупреждение:

• Отправить можно ТОЛЬКО 3 сообщения, после получения ботом 3х сообщений, он перестанет как\-либо реагировать на ваши действия, будьте внимательны\!

• Нам нужны треки без пошлостей, желательно без мата, в любом случае треки будут подвергаться цензуре\.

• Личное желание одного из создателей проекта\: 
> Молю, не более одной песни nkeeei
        """
        

        self.start1 = """
Этот бот создан для подбора треков на новогоднюю дискотеку, учитывая вкус каждого из присутствующих. 

Мы будем рады, если вы поможете оставить приятное впечатление об этом событии!

        """


        self.bot = Bot(token) #инициализация бота , parse_mode=ParseMode.HTML
        self.dp = Dispatcher(self.bot) #инициализация диспетчера бота
        self.dp.middleware.setup(LoggingMiddleware()) #логгирование процесса
        
    def main_kb(self, message):
        kb_list = [[KeyboardButton(text="📖 Доп. Информация 📖")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard

    def start(self): #функция добавляющия обработку ботом коммадны /start
        @self.dp.message_handler(commands=["start"])
        async def start1(message: types.Message):
            
            await self.send_start_message(message)

    def info_(self): #функция добавляющия обработку ботом коммадны /help (дополнительной информации)
        @self.dp.message_handler(commands=["help"])
        async def help1(message: types.Message):
            await self.send_help_message(message)

    def end(self): #функция окончанию << жизни >> бота
        from aiogram import executor
        executor.start_polling(self.dp)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("bot.log", "a") as file:
            file.write(f"[end] [{date}]\n\n")
        self.db.close()

    def get_message(self): #функция добавляющия обработку ботом сообщений отправленных пользователем
        @self.dp.message_handler(content_types="text")
        async def get_message1(message: types.Message):
            b_status = self.check_b_status(message) #находится ли в бан листе
            if not b_status: #если не в бан листе
                    if message.text == "📖 Доп. Информация 📖":
                        await self.send_info_message(message)
                    else:
                        is_new_user = self.is_new_user(message) #проверка на нового пользователя
                        if is_new_user: #если новый пользователь
                            self.add_new_user(message) #добавляем нового пользователя
                        is_new_track = self.check_track_in_db(message) #новый ли трек
                        if is_new_track: #если новый
                            e_status, data = self.message_processing(message) #получаем из сообщения данные
                            if e_status == "error":
                                if data != None:
                                    await data, self.send_m_count_message(message), self.add_m_count_user(message)
                            else:
                                self.add_new_track_in_db(data, message) #добавляем новый трек в дб
                                await self.send_m_count_message(message), self.add_m_count_user(message)
                        else: #если не новый
                            self.add_existing_track_in_db(message) #добавляем к существующему треку в дб
                            await self.send_m_count_message(message), self.add_m_count_user(message)

            
    def message_processing(self, message): #обработка сообщения
        url = message.text
        if validators.url(url) == True:
            parts = url.split('/')
            track_index = parts.index('track')
            track_id = parts[track_index + 1].split('?')[0]
            api_url = "https://api.music.yandex.net/tracks/" + track_id
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    response_data = response.json()
                    name = response_data['result'][0]['title']
                    artists = response_data['result'][0]['artists']
                    authors = ''
                    for artist in artists:
                        name1 = artist['name']
                        authors = authors + name1 + ", "
                    author = authors[:-2]
                    data = {
                        "name": name,
                        "author": author
                        }
                    return "not-found", data
            except Exception as e:
                return "error", e
        else:
            return "error", message.answer("Ссылка некорректна, либо ваше сообщение не является ссылкой.")
        

    @staticmethod
    def start_logging():
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("bot.log", "a") as file:
            file.write(f"[start] [{date}]\n")

    def send_start_message(self, message): #функция, возвращающая отправку ботом сообщения после запуска
        return message.answer(self.start1, reply_markup=self.main_kb(message.from_user.id))

    def send_info_message(self, message): #функция, возвращающая отправку ботом сообщения-справки
        return message.answer(self.info, parse_mode=types.ParseMode.MARKDOWN_V2)
    
    def send_m_count_message(self, message): #функция, возвращающая отправку ботом сообщения о колличестве оставшихся сообщений до блокировки ботом пользователя
        id_ = str(message['from'].id)
        m_count = self.cur.execute(f"SELECT m_count FROM users WHERE id = {id_}")
        m_count = [i for i in [g for g in m_count][0]][0]
        m_count_difference = 2 - m_count
        if m_count_difference != 0:
            return message.answer(f"Ваше сообщение было успешно отправлено на обработку, у вас осталось {m_count_difference} доступных сообщений")
        else: 
            return message.answer(self.last_message, parse_mode=types.ParseMode.MARKDOWN_V2)

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
        self.cur.execute("INSERT INTO tracks (name, author, v_count, url) VALUES (?, ?, ?, ?)", (track_name, author, 1, message.text))
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
try:
    bot = MusicBot()
    bot.start_logging()
    bot.start()
    bot.info_()
    bot.get_message()
finally:
    bot.end()


