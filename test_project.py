import pytest
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from project import load_schedule, send_welcome, class_processing


def test_load_schedule():
    assert load_schedule()['10B']['Monday'][1]['lesson'] == 'Chemistry'


@pytest.mark.asyncio
async def test_send_welcome():
    message = AsyncMock()
    await send_welcome(message)

    message.answer.assert_called_with("Hello! Please enter your class: ")


# Sample data for mocking
schedule_data = ["9A", "10B"]
user_class = {}


@pytest.mark.asyncio
async def test_class_processing_class_exists():
    # Mocking the message and the InlineKeyboardMarkup
    message = AsyncMock(Message)
    message.text = "9A"
    message.chat = AsyncMock()
    message.chat.id = 12345
    message.answer = AsyncMock()

    # Mocking schedule_data and user_class
    with patch("project.schedule_data", schedule_data), patch("project.user_class", user_class):
        await class_processing(message)

    # Checking if the user's class was saved correctly
    assert user_class[message.chat.id] == "9A"

    # Checking if the InlineKeyboardMarkup was sent with the right options
    message.answer.assert_called_with(
        "Select day: ",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Monday", callback_data='weekday:Monday')],
            [InlineKeyboardButton(text="Tuesday", callback_data='weekday:Tuesday')],
            [InlineKeyboardButton(text="Wednesday", callback_data='weekday:Wednesday')],
            [InlineKeyboardButton(text="Thursday", callback_data='weekday:Thursday')],
            [InlineKeyboardButton(text="Friday", callback_data='weekday:Friday')],
        ])
    )


from unittest.mock import AsyncMock, patch
import pytest
from project import handle_weekday_selection, schedule_data, user_class, MyCallback


@pytest.mark.asyncio
async def test_handle_weekday_selection_valid():
    # Mocking the callback query and message
    callback = AsyncMock()
    callback.message.chat.id = 12345
    callback.message.answer = AsyncMock()

    callback_data = MyCallback(day="Monday")

    user_class[12345] = "9A"

    # Mocking schedule_data with lessons for "9A" on Monday
    schedule_data["9A"] = {
        "Monday": [{"lesson": "Math", "time": "08:00", "room": "101", "teacher": "Mr. Smith"}]
    }

    with patch("project.schedule_data", schedule_data):
        await handle_weekday_selection(callback, callback_data)

    callback.message.answer.assert_called_with(
        "Schedule for 9A on Monday: \n\nLesson 1: Math\nTime: 08:00\nRoom: 101\nTeacher: Mr. Smith\n\n"
    )
