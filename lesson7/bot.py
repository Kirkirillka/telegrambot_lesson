# -*- coding:utf-8 -*-
__author__ = 'kirill'

import telebot
import re
from telebot import types
import config

bot = telebot.TeleBot(config.token)



plus_icon = "https://pp.vk.me/c627626/v627626512/2a627/7dlh4RRhd24.jpg"
minus_icon = "https://pp.vk.me/c627626/v627626512/2a635/ILYe7N2n8Zo.jpg"
divide_icon = "https://pp.vk.me/c627626/v627626512/2a620/oAvUk7Awps0.jpg"
multiply_icon = "https://pp.vk.me/c627626/v627626512/2a62e/xqnPMigaP5c.jpg"
error_icon = "https://pp.vk.me/c627626/v627626512/2a67a/ZvTeGq6Mf88.jpg"

digits_pattern = re.compile(r'[0-9]+ [0-9]+$', re.MULTILINE)


@bot.inline_handler(lambda query: len(query.query) is 0)
def empty_query(query):
    hint = 'Put here 2 int and pick up the result!'
    try:
        r = types.InlineQueryResultArticle(
            id='1',
            input_message_content=types.InputTextMessageContent(message_text='Please,type here!',
                                                                parse_mode='Markdown'),
            title='Bot \"Math\"',
            description=hint
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as ex:
        print(ex)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    try:
        matches = re.match(digits_pattern, query.query)
        num1, num2 = matches.group().split()
    except AttributeError as ex:
        return

    try:
        m_sum = int(num1) + int(num2)
        r_sum = types.InlineQueryResultArticle(
            id='1',
            title='Sum',
            description='Result is {!s}'.format(m_sum),
            input_message_content=types.InputTextMessageContent("{!s} + {!s} = {!s}".format(num1, num2, m_sum)),
            thumb_url=plus_icon,thumb_width=48,thumb_height=48
        )
        m_sub = int(num1) - int(num2)
        r_sub = types.InlineQueryResultArticle(id='2',
                                               title='Substination',
                                               description='Result is {!s}'.format(m_sub),
                                               input_message_content=types.InputTextMessageContent(
                                                   "{!s} - {!s} = {!s}".format(num1, num2, m_sub)),
                                               thumb_width=48,thumb_height=48,thumb_url=minus_icon
                                               )
        if num2 is not u"0" and num2 is not '0':
            m_div = float(num1) / float(num2)
            r_div = types.InlineQueryResultArticle(id='3',
                                                   title='Division',
                                                   description='Result is {0:.2f}'.format(m_div),
                                                   input_message_content=types.InputTextMessageContent(
                                                       "{0!s} / {1!s} = {2:.2f}".format(num1, num2, m_div)),
                                                   thumb_width=48,thumb_height=48,thumb_url=divide_icon
                                                   )
        else:
            r_div = types.InlineQueryResultArticle(id='3',
                                                   title='Division',
                                                   description='I cannot perform it!',
                                                   input_message_content=types.InputTextMessageContent(
                                                       "I am a good bot and dont perform division at zero"),
                                                   thumb_width=48,thumb_height=48,thumb_url=error_icon,
                                                   url="https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BD%D0%B0_%D0%BD%D0%BE%D0%BB%D1%8C",
                                                   disable_web_page_preview=True,
                                                   hide_url=True
                                                   )
        m_mul = int(num1) * int(num2)
        r_mul = types.InlineQueryResultArticle(
            id='4',
            title='Multiplication',
            description='Result is {!s}'.format(m_mul),
            input_message_content=types.InputTextMessageContent('{!s} *{!s} ={!s}'.format(num1, num2, m_mul)),
            thumb_width=48,thumb_height=48,thumb_url=multiply_icon
        )
        bot.answer_inline_query(query.id, [r_sum, r_sub, r_div, r_mul],cache_time=300)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


if __name__ == '__main__':
    bot.polling(none_stop=True)