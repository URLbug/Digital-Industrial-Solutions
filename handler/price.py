from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery

from .button import menu_price
from __init__ import project


projects = list(project['project_for_make'].keys())

route = Router()

@route.message(Text(text="Ассортимент"))
async def price_one(message: Message):
    price = 1
    
    types = project['project_for_make'][projects[price-1]]['name']

    await message.answer_photo(project['project_for_make'][projects[price-1]]['image'], 
                               caption=f"{project['project_for_make'][projects[price-1]]['name']}\n{project['project_for_make'][projects[price-1]]['description']}",
                               reply_markup=menu_price(price, types))

@route.callback_query(Text(startswith="one"))
async def price_one(call: CallbackQuery):
    calls = call.data.split(':')
    price = int(calls[1]) - 1

    types = project['project_for_make'][projects[price-1]]['name']

    if price <= len(projects)+1 and price > 0:
        await call.message.answer_photo(project['project_for_make'][projects[price-1]]['image'], 
                               caption=f"{project['project_for_make'][projects[price-1]]['name']}\n{project['project_for_make'][projects[price-1]]['description']}",
                               reply_markup=menu_price(price, types))

@route.callback_query(Text(startswith="two"))
async def price_two(call: CallbackQuery):
    calls = call.data.split(':')
    price = int(calls[1]) + 1

    types = project['project_for_make'][projects[price-1]]['name']

    if price <= len(projects):
        await call.message.answer_photo(project['project_for_make'][projects[price-1]]['image'], 
                               caption=f"{project['project_for_make'][projects[price-1]]['name']}\n{project['project_for_make'][projects[price-1]]['description']}",
                               reply_markup=menu_price(price, types))