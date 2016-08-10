#!/usr/bin/python
#-*- coding:utf-8 -*-
__author__ = 'kirill'

import os

import telebot
from flask import Flask,request


token='Your TOKEN must be here'

WEBHOOK_HOST = 'kaiechobot.herokuapp.com'
WEBHOOK_URL_PATH = '/bot'
WEBHOOK_PORT = os.environ.get('PORT',5000)
WEBHOOK_LISTEN = '0.0.0.0'


WEBHOOK_URL_BASE = "https://%s/%s"% (WEBHOOK_HOST,WEBHOOK_URL_PATH)

bot = telebot.TeleBot(token)
server=Flask(__name__)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


# Получение сообщений
@server.route("/bot", methods=['POST'])
def getMessage():
    # Чтение данных от серверов telegram
    bot.process_new_messages(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8")).message
        ])
    return "!", 200

# Установка webhook
@server.route("/")
def webhook():
    bot.remove_webhook()
    # Если вы будете использовать хостинг или сервис без https
    # то вам необходимо создать сертификат и
    # добавить параметр certificate=open('ваш сертификат.pem')
    return "%s" %bot.set_webhook(url=WEBHOOK_URL_BASE), 200

@server.route("/remove")
def remove_hook():
    bot.remove_webhook()
    return "Webhook has been removed"

# Запуск сервера
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
webhook()