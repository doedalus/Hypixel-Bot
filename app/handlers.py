from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.hypixel import get_info
from app.keyboard import main
import datetime

router = Router()

class Check(StatesGroup):
    nickname = State()

@router.message(CommandStart())
async def start(message: Message):
    print(f'[{str(datetime.datetime.now()).split('.')[0]}] User {str(message.from_user.first_name)} used /start.')
    database = open('database.txt','a')
    userlist = [str(u) for u in open('database.txt')]
    if f'{str(message.from_user.id)}|{str(message.from_user.first_name)}\n' not in userlist:
        database.write(f'{str(message.from_user.id)}|{str(message.from_user.first_name)}\n')
    await message.answer('Hello! Use /check.', reply_markup=main)

@router.message(Command('check'))
async def get_nickname(message: Message, state: FSMContext):
    print(f'[{str(datetime.datetime.now()).split('.')[0]}] User {str(message.from_user.first_name)} used /check.')
    await state.set_state(Check.nickname)
    await message.answer('Enter player name: ')

@router.message(Check.nickname)
async def check_nickname(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    data = await state.get_data()
    print(f'[{str(datetime.datetime.now()).split('.')[0]}] User {str(message.from_user.first_name)} tried to get information about the player {data['nickname']}.')
    result = get_info(data['nickname'])
    await message.answer(result)