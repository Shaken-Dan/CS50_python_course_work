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