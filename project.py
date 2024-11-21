import asyncio

import openpyxl
from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton

API_TOKEN = "7160139348:AAE3cjLCImH9mA1LowlifbH1F7VW6QUtGTo"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_class = {}


async def main():
    await dp.start_polling(bot)

class MyCallback(CallbackData, prefix="weekday"):
    day: str


# Welcome message handler
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Hello! Please enter your class: ")


# Reads Excel file which serves as a database
def load_schedule():
    workbook = openpyxl.load_workbook("schedule_1.xlsx")
    sheet = workbook.active
    schedule = {}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        class_name = row[0]
        day = row[1]
        if class_name not in schedule:
            schedule[class_name] = {}
        schedule[class_name][day] = []

        for item in range(2, len(row), 4):
            lesson = row[item]
            time = row[item + 1]
            room = row[item + 2]
            teacher = row[item + 3]

            if lesson and time and room and teacher:
                schedule[class_name][day].append({
                    'lesson': lesson,
                    'time': time,
                    'room': room,
                    'teacher': teacher
                })
    return schedule


schedule_data = load_schedule()


# Handle class input: checks if user entered class number and literal exists in DB
@dp.message(F.text)
async def class_processing(message: Message):
    # User enters class name
    class_name = message.text.strip().upper()

    # Checks if user entered class exists in Excel file
    if class_name in schedule_data:
        user_class[message.chat.id] = class_name

        # Inline keyboard with weekdays listed
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Monday", callback_data=MyCallback(day="Monday").pack())],
            [InlineKeyboardButton(text="Tuesday", callback_data=MyCallback(day="Tuesday").pack())],
            [InlineKeyboardButton(text="Wednesday", callback_data=MyCallback(day="Wednesday").pack())],
            [InlineKeyboardButton(text="Thursday", callback_data=MyCallback(day="Thursday").pack())],
            [InlineKeyboardButton(text="Friday", callback_data=MyCallback(day="Friday").pack())],
        ])
        await message.answer("Select day: ", reply_markup=keyboard)
    else:
        await message.answer("Class not found, please enter again!")


@dp.callback_query(MyCallback.filter())
async def handle_weekday_selection(callback: CallbackQuery, callback_data: MyCallback):
    class_name = user_class.get(callback.message.chat.id)
    selected_day = callback_data.day

    if class_name and selected_day in schedule_data[class_name]:
        lessons = schedule_data[class_name][selected_day]
        if lessons:
            response = f"Schedule for {class_name} on {selected_day}: \n\n"
            for idx, lesson in enumerate(lessons, start=1):
                response += (
                    f"Lesson {idx}: {lesson['lesson']}\n"
                    f"Time: {lesson['time']}\n"
                    f"Room: {lesson['room']}\n"
                    f"Teacher: {lesson['teacher']}\n\n"
                )
            await callback.message.answer(response)
        else:
            await callback.message.answer(f"No lessons found for {class_name} on {selected_day}")
    else:
        await callback.message.answer(f"No lessons found for {class_name} on {selected_day}")


if __name__ == "__main__":
    asyncio.run(main())
