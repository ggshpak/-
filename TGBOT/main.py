from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = "6536490824:AAHEiK-rF90tM7LCmLZfHIYrOzjvSifCHz8"
data_file = "marathon_registrations.txt"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
class MarathonRegistration(StatesGroup):
    name = State()
    marathon_type = State()
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton("Полный марафон"), types.KeyboardButton("Полумарафон"))
keyboard.add(types.KeyboardButton("10 км"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! 👋\nЯ бот для записи на марафон. 🏃‍♀️🏃\n"
        "Введите ваше ФИО:",
        reply_markup=types.ReplyKeyboardRemove())
    await MarathonRegistration.name.set()
@dp.message_handler(state=MarathonRegistration.name)
async def handle_name(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(
        f"Запомнил ваше ФИО: {user_name}\n"
        "Теперь выберите тип забега:",
        reply_markup=keyboard)
    await MarathonRegistration.next()
@dp.message_handler(state=MarathonRegistration.marathon_type)
async def handle_marathon_type(message: types.Message, state: FSMContext):
    marathon_type = message.text
    data = await state.get_data()
    user_name = data.get('name')
    with open(data_file, "a", encoding='utf-8') as f:
        f.write(f"ФИО: {user_name}. Тип забега: {marathon_type}\n")
    await message.answer(
        f"Отлично! Вы записались на {marathon_type}! 👍\n"
        "Ваши данные сохранены. До встречи на марафоне! 🎉")
    await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)