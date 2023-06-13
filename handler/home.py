from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .button import menu
from database.database import User_2, session


route = Router()

@route.message(Command('start'))
async def start(message: Message):
    arr = [i.id_user for i in session.query(User_2.id_user).distinct()]

    if message.from_user.id not in arr:
        user_2 = User_2(id_user=message.from_user.id, name_user=message.from_user.username)

        session.add(user_2)
        session.commit()
        session.close()

    await message.answer('Вас приветствует компания Digital Industrial Solutions!\n\nДля начала, выберите интересующий Вас продукт, кликнув на кнопку "Ассортимент".\n\nТакже мы предлагаем Вам ознакомиться с нашим портфолио:\nGitHub - https://github.com/URLbug\nСайты - RuiHelp.pythonanywhere.com, amin445.pythonanywhere.com\n\nПриятного выбора!', reply_markup=menu())