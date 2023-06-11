from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .button import menu


route = Router()

@route.message(Command('start'))
async def start(message: Message):
    await message.answer('Hello World!', reply_markup=menu())