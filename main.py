from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
import asyncio
import openpyxl

API_TOKEN = "7160139348:AAE3cjLCImH9mA1LowlifbH1F7VW6QUtGTo"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


