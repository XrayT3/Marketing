import telebot
import base


def step_1():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn1 = telebot.types.InlineKeyboardButton(text="Конечно) Что я должен сделать?", callback_data="registr")
    btn2 = telebot.types.InlineKeyboardButton(text="Да, давайте", callback_data="registr")
    btn3 = telebot.types.InlineKeyboardButton(text="Согласен!", callback_data="registr")
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    return markup


def menu():
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("🔎О нас", "💌Хочу также")
    markup.row("🤖Примеры работ", "👥Пригласить друзей")
    return markup


def project():
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("Категория 1", "Категория 2")
    markup.row("Назад")
    return markup


def doing():
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row("🤓 Только планирую начать")
    markup.row("😎 Уже занимаюсь бизнесом")
    return markup


def phone():
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    button_phone = telebot.types.KeyboardButton(text="🤖Активировать бота", request_contact=True)
    markup.row(button_phone)
    return markup


def phone1():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn3 = telebot.types.InlineKeyboardButton(text="Согласен!", callback_data="phone", request_contact=True)
    markup.row(btn3)
    return markup
