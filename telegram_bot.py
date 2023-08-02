import telebot
from telebot import types

from model import parser
from model_news import get_top_news


__all__ = {"start", "callback", "save_data"}

bot = telebot.TeleBot('6085646343:AAG8P-aoU8VCCrhYv_Xxs8LZ6NvUVmvC8VY')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Давай подберем матчи", callback_data="Давай подберем матчи")
    btn2 = types.InlineKeyboardButton("Новости футбола", callback_data="Новости футбола")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} :)\nС чего начнем?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "Давай подберем матчи":
        bot.send_message(call.message.chat.id, "Введи количество забитых и пропущенных голов. Например '9:10'")
        bot.register_next_step_handler(call.message, save_data)
    else:
        news = get_top_news()
        for title, link in news.items():
            bot.send_message(call.message.chat.id, f'[{title}]({link})', parse_mode='Markdown')


def save_data(message):
    try:
        scored, missed = message.text.split(":")
        parser.get_form_goals_dict(scored, missed)
        file = open("matches.xlsx", "rb")
        bot.send_document(message.chat.id, file)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова!")
        bot.register_next_step_handler(message, save_data)


bot.polling(none_stop=True)
