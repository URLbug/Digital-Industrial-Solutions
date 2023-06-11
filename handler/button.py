from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def menu():
    build = ReplyKeyboardBuilder()

    build.button(text='Ассортимент')
    build.button(text='Отзовы')

    build.adjust(2)

    return build.as_markup(resize_keyboard=True)

def menu_order():
    build = ReplyKeyboardBuilder()

    build.button(text='Да')
    build.button(text='Нет')

    build.adjust(2)

    return build.as_markup(resize_keyboard=True)

# def menu_order_2():
#     build = ReplyKeyboardBuilder()

#     build.button(text='Описать услугу позже')

#     build.adjust(2)

#     return build.as_markup(resize_keyboard=True)

def menu_price(price, types):
    build = InlineKeyboardBuilder()

    build.button(text="<", callback_data=f"one:{price}"),
    build.button(text=str(price), callback_data="null"),
    build.button(text=">", callback_data=f"two:{price}")
    build.button(text="Заказать", callback_data=f"order:{types}")

    build.adjust(3)

    return  build.as_markup()