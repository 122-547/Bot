#импорт библиотек
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import sqlite3

class MusicBot: #создание класса
    def __init__(self): #функция инициализации класса
        logging.basicConfig(level=logging.INFO) #создание отправки логгирования программы
        token = "8059535485:AAFbm_vV3jWk_6CTGii0Zk2GHam9bU6wtrA" #токен бота временный
        self.db = sqlite3.connect("database.db") #подключение к базе данных
        self.cur = self.db.cursor() #создание курсора подключения

        #тут должен быть текст о создателях проекта
        self.admins_info = """ 

        """
        #тут должен быть текст о дополнительной информации, то есть формой сообщения и тд
        self.help = """
        """
        """
        Форма, согласно которой следует писать сообщения:

        Название трека
        Исполнитель

            !!!ВАЖНО!!!
        Важно использовать оригинальное название трека и исполнителя, что бы 
        запрос прошел проверку.

        Если предложение будет написано не по форме, 
        то оно будет являться недействительным.

        Отправить можно ТОЛЬКО 3 сообщения, составленных по форме, после 
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
            await self.send_help_message

    def end(self): #функция окончанию << жизни >> бота
        from aiogram import executor
        executor.start_polling(self.dp, skip_updates=True)
        self.db.close()

    def get_message(self): #функция добавляющия обработку ботом сообщений отправленных пользователем
        @self.dp.message_handler(content_types="text")
        async def get_message1(message: types.Message):
            b_status = self.check_b_status(message) #находится ли в бан листе
            print(b_status)
            if not b_status: #если не в бан листе
                type_message = self.type_message(message) #проверка на тип сообщения
                if type_message == "text_message": #если сообщение - текст
                    is_new_user = self.is_new_user(message) #проверка на нового пользователя
                    if is_new_user: #если новый пользователь
                        self.add_new_user(message) #добавляем нового пользователя
                    self.add_m_count_user(message) #добавляем в базу данных
                    data = self.message_processing(message) #получаем из сообщения данные
                    is_new_track = self.check_track_in_db(data) #находится ли трек в дб
                    if is_new_track: #если не находится
                        self.add_new_track_in_db(data) #добавляем новый трек в дб
                    else: #если находится
                        self.add_existing_track_in_db(data) #добавляем к существующему треку в дб
                    await self.send_m_count_message(message) #отправляем информационное сообщение
            
    def message_processing(self, message): #обработка сообщения, делит сообщение, составленное по форме на имя автора и название трека
        """
        при этом форма сообщения, по которой должно быть составлено предложение такая:

        название трека
        имя автора

        например:

        Тесно
        Aarne, BUSHIDO ZHO, ANIKV

        если сообщение не будет составлено по такой форме, то в будущем такое предложение не будет учитываться при подсчете и выносе решения о выборе трека
                """
        
        message_text = message.text
        message_list = message_text.splitlines()
        data = {
            "name" : message_list[0],
            "author" : message_list[1]
                }
        return data

    def type_message(self, message): #функция, возвращающая тип присланного сообщения (бот-комманда или текст)
        try:
            result = message.entities[0].type
            return result
        
        except:
            return "text_message"

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
        m_count_difference = 3 - m_count
        if m_count_difference != 0:
            return message.answer(f"Ваше сообщение было успешно отправлено на обработку, у вас осталось {m_count_difference} доступных сообщений")
        else: 
            return message.answer("У вас осталось 0 доступных сообщений, спасибо за участие. Ваши последующие сообщения не будут обрабатываться ботом.")

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

    def check_track_in_db(self, data): #функция, проверяющая находится ли предложенный трек в базе данных или нет
        track_name = data['name']
        author = data['author']
        select = self.cur.execute("SELECT name, author FROM tracks WHERE name = ? AND author = ?", (track_name.lower(), author.lower()))
        result = [i for i in select]
        if result == []:
            return True
        else:
            return False
        
        
    def add_new_track_in_db(self, data): #функция, добавляющая новый предложенный трек в базу данных
        track_name = data['name']
        author = data['author']
        self.cur.execute("INSERT INTO tracks (name, author, v_count) VALUES (?, ?, ?)", (track_name.lower(), author.lower(), 1))
        self.db.commit()

    def add_existing_track_in_db(self, data): #функция, добавляющая существующий в базе данных предложенный трек (обновляет колличество предложений данного трека в базе данных)
        track_name = data['name']
        author = data['author']
        v_count = self.cur.execute("SELECT v_count FROM tracks WHERE name = ? AND author = ?", (track_name.lower(), author.lower()))
        v_count = [i for i in [g for g in v_count][0]][0]
        v_count += 1
        self.cur.execute("UPDATE tracks SET v_count = ? WHERE name = ? AND author = ?", (v_count, track_name.lower(), author.lower()))
        self.db.commit()
    

#запуск бота просто
#вызов нужных для работы бота функций, прописанных в классе
bot = MusicBot()
bot.start()
bot.admins()
bot.help_()
bot.get_message()
bot.end()
