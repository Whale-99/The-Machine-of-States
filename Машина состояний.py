import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

API_TOKEN = 'YOUR_BOT_API_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Класс состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Обработчик текстового сообщения "Calories" для ввода возраста
@dp.message(lambda message: message.text == "Calories")
async def set_age(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

# Обработчик для состояния UserState.age, получает рост
@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))  # сохраняем возраст
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)

# Обработчик для состояния UserState.growth, получает вес
@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=int(message.text))  # сохраняем рост
    await message.answer("Введите свой вес:")
    await state.set_state(UserState.weight)

# Обработчик для состояния UserState.weight, вычисляет калории
@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))  # сохраняем вес

    # Получаем все данные
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Формула Миффлина-Сан Жеора для расчета калорийности
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    # Отправляем результат пользователю
    await message.answer(f"Ваша дневная норма калорий: {calories:.2f} ккал.")

    # Завершаем машину состояний
    await state.clear()

# Запуск бота
async def main():
    try:
        print("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
