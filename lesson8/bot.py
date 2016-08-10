# -*- coding:utf-8 -*-
__author__ = 'kirill'

import telebot
import re
import config
from telebot import types

token = config.knrtu_kai_token
bot = telebot.TeleBot(config.token)

digits_pattern = re.compile(r'[0-9]+ [0-9]+$', re.MULTILINE)


@bot.message_handler(content_types=['text'])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Press me!',switch_inline_query='Telegram',)
    keyboard.add(switch_button)
    bot.send_message(message.chat.id, 'I am message from standart mode', reply_markup=keyboard)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Press me', callback_data='test'))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id='1',
        title='Press me',
        input_message_content=types.InputTextMessageContent(
            message_text='I am message from inline mode'
        ),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'test':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Pufff!')
            bot.answer_callback_query(callback_query_id=call.id,
                                      show_alert=True,
                                      text='Pufffff!')
    elif call.inline_message_id:
        if call.data == 'test':
            bot.edit_message_text(inline_message_id = call.inline_message_id,
                                text = 'Skupfff!')

if __name__ == '__main__':
    bot.polling(none_stop=True)