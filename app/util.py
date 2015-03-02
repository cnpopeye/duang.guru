#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 
 AUTHOR: zc  
 HOST: zc@zcdeMacBook-Pro.local
 PATH: /Users/zc/workspace/duang.guru/app/util.py
 DATE: 2015-03-02 19:32:56  
 
   
 INTRODUCTION:
    <<introduction write on here>>
     
 CHANGLOG:
    # FORMAT: DATE TIME AUTHOR COMMENT
    # etc. 2015-03-02 19:32:56 zc  # comment on here.
    
    <<changelog write on here>> 
    
  
'''

import pymongo
import sys
import redis
import urllib
from config import mongo
from config import redisconf

_pool = None


def new_pool(host=redisconf['host'], \
             port=redisconf['port'], \
             db=redisconf['dbn']):
    '''create a new pool to redis'''
    return redis.ConnectionPool(host=host, port=port, db=db, max_connections=redisconf['redis_max_connections'])


def get_redis():
    global _pool
    if _pool is None:
        _pool = new_pool()
    return redis.Redis(connection_pool=_pool)


def get_mongo():
    '''
    封装mongodb链接对象
    获取对象之后,可自由操作
    '''
    try:
        connection = pymongo.Connection( host = mongo["host"], port = mongo["port"], max_pool_size = mongo["max_pool_size"] )
        db_handler = connection[mongo["dbn"]]
        if mongo["user"]:
            db_handler.authenticate( mongo["user"], mongo["passwd"] )
    except Exception, e:
        print "mongodb init error:" + str( e )
        sys.exit( 1 )
    return db_handler


def get_host(url):
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)
    return host

        
# main function
if __name__ == '__main__':
    pass

