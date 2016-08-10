__author__ = 'kirill'

from contextlib import closing
import shelve
from random import shuffle

from telebot import types

from lesson2.SQLigther import SQLigther
from config import shelve_name,count_db_name, database_name



class AnswerUtils():

    def count_rows(self):
        db = SQLigther(database_name)
        rowsnum = db.count_rows()
        with closing(shelve.open(shelve_name)) as storage:
            storage['rows_count'] = rowsnum


    def get_rows_count(self):
        with closing(shelve.open(shelve_name)) as storage:
            rowsnum = storage['rows_count']
        return rowsnum


    def finish_user_game(self,chat_id,user_id):
         with closing(shelve.open(shelve_name)) as storage:
             del storage[str(chat_id)][str(user_id)]

    def set_user_game(self,chat_id, user_id, answer):
        with closing(shelve.open(shelve_name)) as storage:
            storage[str(chat_id)]={str(user_id):{'answer':answer}}

    def get_answer_for_user(self,chat_id, user_id):
        with closing(shelve.open(shelve_name)) as storage:
            try:
                answer=storage[str(chat_id)][str(user_id)]['answer']
                return answer
            except KeyError:
                return None

    def generate_markup(self,right_answer, wrong_answers):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True)
        list_items = []
        list_items.append(right_answer)
        for item in wrong_answers.split(','):
            list_items.append(item)
        print(list_items)
        shuffle(list_items)
        for item in list_items:
            markup.add(item)
        return markup


class CountUtils():

    def set_count_user(self,chat_id,user_id,count=0):
        with closing(shelve.open(count_db_name)) as storage:
            try:
                count=storage[str(chat_id)][str(user_id)]['count']
                print(count)
                storage[str(chat_id)][str(user_id)]['count']=count
            except KeyError:
                storage[str(chat_id)]={str(user_id):{'count':count}}

    def increase_count_user(self,chat_id,user_id,set=1):
        with closing(shelve.open(count_db_name)) as storage:
            try:
                count=storage[str(chat_id)+'-'+str(user_id)]
                storage[str(chat_id)+'-'+str(user_id)]=count+set
                print(count)
            except KeyError:
               storage[str(chat_id)+'-'+str(user_id)]=0

    def get_count_user(self,chat_id,user_id):
        with closing(shelve.open(count_db_name)) as storage:
            try:
                return storage[str(chat_id)+'-'+str(user_id)]
            except KeyError:
                return 0