__author__ = 'kirill'
#-*- coding:utf-8 -*-
import telebot
import random
import config
from lesson6 import botan

random.seed()

bot=telebot.TeleBot(config.token)
bot.remove_webhook()

@bot.message_handler(commands=['random'])
def cmd_random(message):
    bot.send_message(message.chat.id,random.randint(1,10))
    botan.track(config.botan_key,message.chat.id,'Случайное число')
    return

@bot.message_handler(commands=['yesorno'])
def cmd_yesorno(message):
    bot.send_message(message.chat.id,random.choice(strings))
    botan.track(config.botan_key,message.chat.id,'Да или нет')


if __name__=='__main__':
    global strings
    strings=['Yes','No']
    bot.polling(none_stop=True)