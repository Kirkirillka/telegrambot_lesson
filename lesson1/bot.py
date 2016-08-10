__author__ = 'kirill'
import config
import telebot
from telebot import types


bot=telebot.TeleBot(config.token)
markup=types.ReplyKeyboardMarkup()
markup.row('Send me!',"Dont't ask me else!")

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    print(message.text)
    bot.send_message(message.chat.id,message.text,reply_markup=markup)

if __name__=='__main__':
    bot.polling(none_stop=True)

