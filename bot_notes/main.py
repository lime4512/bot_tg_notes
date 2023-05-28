from aiogram import Bot, Dispatcher, executor,types, Bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import TOKEN_API
from keyboard import get_start_ikb, get_cancel_kb, get_edit_ikb, notes_cb 
import sqlite_db


bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class NotesStatesGroup(StatesGroup):
    name = State()

    new_name = State()

#Подключение к бд
async def on_start_bd(_):
    await sqlite_db.db_connect()
    print("Успешное подключение к БД")


#Команды
@dp.message_handler(commands=["start"])
async def start_commdand(message: types.Message):
    await message.answer("Добро пожаловать в бот с заметками!!!", reply_markup=get_start_ikb())


    user_id = message.from_user.id
    await sqlite_db.create_new_table(user_id)

@dp.message_handler(commands =  ["Назад"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer("Вы отменили заметку",reply_markup=get_start_ikb())


#Все заметки
@dp.message_handler(text = "Просмотреть все заметки")
async def get_all_notes(message: types.Message):
    user_id = message.from_user.id
    notes = await sqlite_db.get_all_notes(user_id)
    if not notes:
        await message.answer("У вас нет записей в заметках")
    else:
        text = ""
        i = 1
        for ret in notes:
            text = text + f"{i})"+f"{ret[1]}\n"
            i += 1
        await message.answer(text)

#Удаление/изменение заметок
@dp.message_handler(text = "Удаление/Изменение заметок")
async def get_all_notes(message: types.Message):
    user_id = message.from_user.id
    notes = await sqlite_db.get_all_notes(user_id)
    if not notes:
        await message.answer("У вас нет записей в заметках")
    else:
        text = ""
        i = 1
        for ret in notes:
            text = f"{i})"+f"{ret[1]}\n"
            i += 1
            await message.answer(text, reply_markup=get_edit_ikb(ret[0]))

#Удаление
@dp.callback_query_handler(notes_cb.filter(action ="delete"))
async def cb_delete_notes(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    await sqlite_db.delete_notes(user_id,callback_data['id'])
    await callback.message.reply("Заметка удалена")
    await callback.answer()

#Изменение
@dp.callback_query_handler(notes_cb.filter(action ="edit"))
async def cb_edit_notes(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.message.answer("Отправь новую заметку", reply_markup=get_cancel_kb())

    await NotesStatesGroup.new_name.set()
    async with state.proxy() as data:
        data["name_id"] = callback_data["id"]

    await callback.answer()

@dp.message_handler(state=NotesStatesGroup.new_name)
async def load_new_name(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    async with state.proxy() as data:
        await sqlite_db.edit_notes(user_id, data['name_id'], message.text)
        await message.reply("Новая заметка установлена!!!", reply_markup=get_start_ikb())

        await state.finish()



#Добавление заметки
@dp.message_handler(text = "Добавить новую запись")
async def create_new_notes(message: types.Message):
    await message.answer("Напиши новую заметку", reply_markup=get_cancel_kb())
    await NotesStatesGroup.name.set()

@dp.message_handler(state=NotesStatesGroup.name)
async def handle_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data["name"] = message.text

    await sqlite_db.create_new_notes(state,user_id)
    await message.reply("Заметка успешно создана :)",reply_markup=get_start_ikb())

    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_start_bd)