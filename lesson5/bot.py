#!/usr/bin/python3
#-*- coding:utf-8 -*-
__author__ = 'kirill'

import time
import logging

import eventlet
import requests
import telebot

import config
from postgre import set_group_by_domain,get_group_by_domain


VK_GROUPS=['dean4','pkkai','grint_kai']

URL_VK='https://api.vk.com/method/wall.get?domain=%s&count=2&filter=owner'
FILENAME_VK='last_known_id'
BASE_POST_URL='https://vk.com/wall-%s_%s'
SINGLE_RUN=False


CHANNEL_NAMES={'@kaihostel3',
              '@knrtu_kai'
              }

bot=telebot.TeleBot(config.token)
bot.remove_webhook()



def get_data(vk_group):
    #timeout=eventlet.Timeout(10)
    try:
        feed=requests.get(URL_VK%vk_group)
        return feed.json()
    except eventlet.timeout.Timeout:
        logging.warning('Got Timeout while retrieving VK JSON data.cancelling...')
        return None
    #finally:
        #timeout.cancel()



def send_new_posts(items,last_id):
    for item in reversed(items):
        if item['id']<last_id:
            break
        link=BASE_POST_URL %(-item['from_id'],item['id'])
        text=item['text']
        post="""%s"""
        request=post %(link)
        for channel in CHANNEL_NAMES:
            bot.send_message(channel,request)
            #time.sleep(1)
    return

def check_new_posts_vk():
    logging.info('[VK] Started scanning for new post')
    for vk_group in VK_GROUPS:
            feed=get_data(vk_group)
            try:
                last_id=get_group_by_domain(vk_group)
                if last_id>=feed['response'][1]['id']:
                    logging.info("[VK] '%s' hasn't any actual news" % vk_group)
                    continue
            except Exception as ex:
                print(ex)
                last_id=feed['response'][1]['id']
                #logging.error('Could not read from storage.Skipped iteration')
                #print('Could not read from storage.Skipped iteration')
            logging.info('Last ID {!s} (VK)={!s}'.format(vk_group,last_id))
            try:
                if feed is not None:
                    entries=feed['response'][1:]
                    send_new_posts(entries,last_id)
                    set_group_by_domain(str(vk_group),str(entries[0]['id']))
                    logging.info('New last_id {!s} (VK) is {!s}'.format(vk_group,(entries[0]['id'])))
            except Exception as ex:
                logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(ex).__name__,str(ex)))
                print(str(ex))
                pass
    logging.info('[VK] Finished scanning')
    return True


if __name__=='__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO
                        , datefmt='%d.%m.%Y %H:%M:%S')
    if not SINGLE_RUN:
        while True:
            print('Post has been checked with response-%s'%check_new_posts_vk())
            # Пауза в 4 минуты перед повторной проверкой
            logging.info('[App] Script went to sleep.')
            time.sleep(60*3)
    else:
        check_new_posts_vk()
    logging.info('[App] Script exited.\n')
