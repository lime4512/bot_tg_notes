from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

notes_cb = CallbackData("notes", "id", "action")



def get_start_ikb() -> ReplyKeyboardMarkup:
    ikb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("Просмотреть все заметки")],
        [KeyboardButton("Добавить новую запись")],
        [KeyboardButton("Удаление/Изменение заметок")]
    ], resize_keyboard=True)
    return ikb


def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/Назад")]
    ], resize_keyboard=True)
    return kb

def get_edit_ikb(notes_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Редактировать заметку", callback_data = notes_cb.new(notes_id,"edit"))],
        [InlineKeyboardButton("Удалить заметку", callback_data = notes_cb.new(notes_id, "delete"))]
    ])
    return ikb