__author__ = 'kirill'

import telebot
import config

import urllib
destination = 'logo3w.png'
url = 'http://www.google.com/images/srpr/logo3w.png'
urllib.urlretrieve(url, destination)


bot=telebot.TeleBot(config.token)
bot.send_photo('@kaihostel3',open(destination))