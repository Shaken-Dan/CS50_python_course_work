from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schedule import schedule_data
import asyncio
import openpyxl

API_TOKEN = "7160139348:AAE3cjLCImH9mA1LowlifbH1F7VW6QUtGTo"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_class = {}

class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int

def create_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="demo",
        callback_data=MyCallback(foo="demo", bar=42)
        # Value can be not packed to string inplace, because builder knows what to do with callback instance
    )
    builder.button(
        text="demo2",
        callback_data=MyCallback(foo="demo2", bar=42)
        # Value can be not packed to string inplace, because builder knows what to do with callback instance
    )

    return builder.as_markup()

# Filter callback by type and value of field :code:`foo`
@dp.callback_query(MyCallback.filter(F.foo == "demo"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    await query.message.answer(f"button pressed {callback_data}")

# Welcome message handler
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Hello! Please enter your class: ", reply_markup=create_keyboard())

# Handle class input
@dp.message(F.text)
async def class_processing(message: Message):
    # Checks if user entered class exist in Excel file
    class_name = message.text.strip().upper()
    """
    if class_name in schedule_data:
        user_class[message.chat.id] = class_name
        # Keyboard with days
        days_buttons = ReplyKeyboardMarkup(
            [KeyboardButton("Monday")],
            [KeyboardButton("Tuesday")],
            [KeyboardButton("Wednesday")],
            [KeyboardButton("Thursday")],
            [KeyboardButton("Friday")]
            , resize_keyboard=True
        )
    
        await message.answer("Select day: ", reply_markup=days_buttons)
        
    else:
        await message.answer("No such a class, please enter correct one!")
    """


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
