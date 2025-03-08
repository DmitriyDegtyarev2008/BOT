from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔹 Главное меню
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")],
        [InlineKeyboardButton(text="Вернуться в главное меню", callback_data="back")]
    ]
)

# 🔹 Кнопка "Перейти" после успешной регистрации
success_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти", url="https://www.harvard.edu")]
    ]
)

start_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="▶ Начать", callback_data="start")]
    ]
)

@dp.message(Command("start"))
async def start(message: types.Message):
    text = "Привет! Чтобы зарегистрироваться, следуй этим шагам:\n\n"
    text += "1️⃣ Нажми кнопку **Зарегистрироваться** ниже.\n"
    text += "2️⃣ Введи **токен**.\n"
    text += "3️⃣ Если токен верный – появится кнопка **Перейти** ✅"

    await message.answer(text, reply_markup=main_menu)

# ✅ Обработчик для inline-кнопки "Зарегистрироваться"
@dp.callback_query(lambda callback: callback.data == "register")
async def ask_token(callback: CallbackQuery):
    await callback.message.answer("Введите токен:")
    await callback.answer()

# ✅ Обработчик для inline-кнопки "Вернуться в главное меню"
@dp.callback_query(lambda callback: callback.data == "back")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)
    await callback.answer()

# ✅ Обработчик ввода токена
@dp.message(lambda message: message.text and message.text != "Перейти")  
async def check_token(message: types.Message):
    if message.text == SECRET_TOKEN:
        await message.answer("✅ Вы успешно зарегистрированы!", reply_markup=success_menu)
    else:
        await message.answer("❌ Неверный токен. Попробуйте снова.")

async def main():
    await bot.delete_webhook()  # Очищаем вебхук
    await dp.start_polling(bot)  # ✅ Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
