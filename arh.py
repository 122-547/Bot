
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '8059535485:AAFbm_vV3jWk_6CTGii0Zk2GHam9bU6wtrA'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(content_types="text")
async def on_start(message: types.Message):
    print(message)
    # print(message.entities[0].type)
    await message.answer("Command")
# @dp.message_handler(content_types="text")
# async def text(message: types.Message):
#     try:
#         result = message.entities[0].type
        
#     except:
#         print(None)
#     await message.answer("Text")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
    #