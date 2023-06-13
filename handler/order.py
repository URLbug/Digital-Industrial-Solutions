from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .state import Order
from .button import menu_order, menu
from database.database import User, Admin, session
from __init__ import bot


route = Router()

order_me = {}

@route.callback_query(Text(startswith='order'))
async def user_order(call: CallbackQuery, state: FSMContext):
    calls = call.data.split(':')

    order_me['id_user'] = call.from_user.id
    order_me['user_name'] = call.from_user.username
    order_me['type'] = calls[1]

    await call.message.answer('Вы точно хотите заказать этот заказ?', reply_markup=menu_order())
    await state.set_state(Order.one)

@route.message(Order.one, Text(text="Да"))
async def user_order_2(message: Message, state: FSMContext):
    await state.update_data(one=message.text)

    await message.answer('Напишит описание вашей услуги.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Order.two)

@route.message(Order.two)
async def user_order_3(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    order_me['description'] = message.text

    users = User(id_user=order_me['id_user'], name_user=order_me['user_name'], types=order_me['type'], description=order_me['description'])

    session.add(users)
    session.commit()
    session.close()
    
    await state.clear()
    await message.answer('Отлично! Ожидайте ответа от нашего менеджера.', reply_markup=menu())

    text = f'Поступил новый заказ от {order_me["user_name"]}({order_me["id_user"]})\n\nОписание и наименование заказа:\n{order_me["type"]}\n{order_me["description"]}'

    for i in session.query(Admin.id_user).distinct():
        try:
            await bot.send_message(i.id_user, text)
        except:
            print(f'Not activiti {i.id_user}')
    
    order_me.clear()

@route.message(Order.one, Text(text="Нет"))
async def user_order_4(message: Message, state: FSMContext):
    order_me.clear()

    await state.clear()
    await message.answer('Если вам не понравился это услуга, тогда Вы можете посмотреть друге услуги которые мы предоставляем.', reply_markup=menu())