__author__ = 'kirill'

import os
import random
import telebot
from telebot import types
import utils
import config
from SQLigther import SQLigther
import lesson2.utils


from flask import Flask,request


WEBHOOK_HOST = 'musicalbot.herokuapp.com'
WEBHOOK_PORT = os.environ.get('PORT',5000)
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s"% (WEBHOOK_HOST)
WEBHOOK_URL_PATH = '/bot'

server=Flask(__name__)
bot=telebot.TeleBot(config.token)
Answer=utils.AnswerUtils()
Count=utils.CountUtils()

@bot.message_handler(commands=['update'])
def update(message):
    for music in os.listdir('lesson2/music/'):
        with open(os.getcwd()+'/lesson2/music/'+music) as file:
            out_msg=bot.send_audio(message.chat.id,file)
            print(music)
            print(out_msg.voice.file_id)

@bot.message_handler(commands=['game'])
def game(message):
    print(message.chat)
    db_worker = SQLigther(config.database_name)
    row = db_worker.select_single(random.randint(1, Answer.get_rows_count()))
    markup = Answer.generate_markup(row[2], row[3])
    Answer.set_user_game(message.chat.type,message.chat.id, row[2])
    bot.send_voice(message.chat.id, row[1], reply_markup=markup,duration=20)
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
        answer= Answer.get_answer_for_user(message.chat.type,message.chat.id)
        if not answer:
            bot.send_message(message.chat.id,'Type "/game" to start the game ')
        else:
            keyboard_hider=types.ReplyKeyboardHide()
            if message.text==answer:
                Count.increase_count_user(message.chat.type,message.chat.id)
                win_count=Count.get_count_user(message.chat.type,message.chat.id)
                bot.send_message(message.chat.id,'Right! You have won %s times!'%win_count)
            else:
                bot.send_message(message.chat.id,"That's wrong,please,send again",reply_markup=keyboard_hider)
            Answer.finish_user_game(message.chat.type,message.chat.id)


@server.route("/bot", methods=['POST'])
def getMessage():
    # Чтение данных от серверов telegram
    bot.process_new_messages(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8")).message
        ])
    return "!", 200


@bot.message_handler(commands=['help'])
def help_message(message,arguments):
    response={'chat_id':message['chat']['id']}
    result=["Hey, %s!" % message['from'].get("first_name")]
    bot.send_message(message.chat.id)
    if arguments:
        print(arguments)

@server.route("/")
def webhook():
    bot.remove_webhook()
    # Если вы будете использовать хостинг или сервис без https
    # то вам необходимо создать сертификат и
    # добавить параметр certificate=open('ваш сертификат.pem')
    return "%s" %bot.set_webhook(url="https://kaiechobot.herokuapp.com/bot"), 200

@server.route("/remove")
def remove_hook():
    bot.remove_webhook()
    return "Webhook has been removed"

# Запуск сервера

if __name__=='__main__':
    Answer.count_rows()
    random.seed()
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    webhook()
