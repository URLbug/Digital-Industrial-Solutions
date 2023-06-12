from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import  Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from database.database import session, Reviews
from .button import menu_reviews, menu_order, menu
from .state import ReviewsState


route = Router()

reviews_arr = []

index = 0

@route.message(Text(text='Отзовы'))
async def reviews_all(message: Message):
    reviews_arr.clear()

    for x in session.query(Reviews.id).distinct():
        id = session.query(Reviews).filter(Reviews.id == x.id)

        for i in id:
            reviews_arr.append(f'Имя: {i.name_user}\n\nОтзыв: {i.reviews}')
    
    await message.answer(reviews_arr[index], reply_markup=menu_reviews(index))

@route.callback_query(Text(startswith="reviews_one"))
async def reviews_one(call: CallbackQuery):
    calls = call.data.split(':')
    index = int(calls[1]) - 1

    if index <= len(reviews_arr) and index >= 0:
        types = reviews_arr[index]

        await call.message.answer(types, reply_markup=menu_reviews(index))

@route.callback_query(Text(startswith="reviews_two"))
async def reviews_two(call: CallbackQuery):
    calls = call.data.split(':')
    index = int(calls[1]) + 1

    if index < len(reviews_arr):
        types = reviews_arr[index]

        await call.message.answer(types, reply_markup=menu_reviews(index))


#### Тут мы оставляем отзыв ####

@route.callback_query(Text(startswith='reviews'))
async def reviews_1(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Вы точно хотите оставить отзыв?', reply_markup=menu_order())
    
    await state.set_state(ReviewsState.one)

@route.message(ReviewsState.one, Text(startswith='Да'))
async def reviews_2(message: Message, state: FSMContext):
    await message.answer('Отлично! Тогда оставти рецензию на нашу работу <3', reply_markup=ReplyKeyboardRemove())
    
    await state.set_state(ReviewsState.two)

@route.message(ReviewsState.two)
async def reviews_2(message: Message, state: FSMContext):
    user_data = await state.get_data()

    review = Reviews(id_user=message.from_user.id, 
                    name_user=message.from_user.username, 
                    reviews=message.text)
    
    session.add(review)
    session.commit()
    session.close()


    await state.clear()
    await message.answer('Мы очень благодарны Вашему отзову! Надеямся, что Вы сможете закажите ещё у нас.', reply_markup=menu())

@route.message(ReviewsState.one, Text(startswith='Нет'))
async def reviews_2(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Очень жаль. Надеямся, что Вам все понравилось и Вы сможете оставить отзыв в другой раз.', reply_markup=menu())