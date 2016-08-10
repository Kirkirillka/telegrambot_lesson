__author__ = 'kirill'

import os
import logging

import psycopg2 as pg_driver
import psycopg2.extras


logger=logging.getLogger(__name__)

db = pg_driver.connect(os.getenv('DATABASE_URL'))
logger.info('[DB] Connection has been established')
cur=db.cursor(cursor_factory=psycopg2.extras.DictCursor)

def get_group_by_domain(domain):
    cur.execute("SELECT last_id FROM vk_group WHERE name=%s",(domain,))
    result=cur.fetchone()
    if result==None:
         cur.execute(""" INSERT INTO vk_group VALUES (%s,0)""",(domain,))
         db.commit()
         logger.info("[DB] There wasn't any records with name='%s'.New record has been addedd"%domain)
         return 0
    else:
        logger.info('[DB] SELECT to %s has been processed'%domain)
        return result[0]



def set_group_by_domain(domain,last_id):
        cur.execute(" UPDATE vk_group SET last_id=%s WHERE name=%s",(last_id,domain,))
        db.commit()
        logger.info("[DB] UPDATE to '%s' with ID up to '%s' has been processed "%(domain,last_id))
        return True






