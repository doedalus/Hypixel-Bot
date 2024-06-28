import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from art import tprint

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    tprint('Hypixel BOT')
    print('>>> The bot started its work <<<<')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')