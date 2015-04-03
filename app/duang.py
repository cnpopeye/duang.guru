#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 
 AUTHOR: zc  
 HOST: zc@zcdeMacBook-Pro.local
 PATH: /Users/zc/workspace/duang.guru/app/duang.py
 DATE: 2015-03-02 19:22:09  
 
   
 INTRODUCTION:
    <<introduction write on here>>
     
 CHANGLOG:
    # FORMAT: DATE TIME AUTHOR COMMENT
    # etc. 2015-03-02 19:22:09 zc  # comment on here.
    
    <<changelog write on here>> 
    
  
'''

import os.path
import tornado.web
import tornado.auth
from tornado import httpserver, ioloop
from tornado.options import define, options
from bson.objectid import ObjectId
import hashlib
import datetime
from util import get_mongo, get_redis, get_host
from config import DEBUG, ip_expires


define("port", default=8999, help="run on the given port", type=int)


class Application( tornado.web.Application ):
    def __init__( self ):

        urls = [
            ( r"/duang", DuangHandler),
            ( r"/index", DuangListHandler),
            ( r"/channel-list", ChannelListHandler),
            ]

        settings = dict(
            autoescape = None,
            xsrf_cookies=False,
            debug = DEBUG,
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),              
            )
        if settings.get("debug"):
            print "ATTENTION:running in DEBUG...!!!"
        tornado.web.Application.__init__( self, urls, **settings )
        self.mongo = get_mongo()
        self.redis = get_redis()
              
    
class BaseHandler(tornado.web.RequestHandler ):
    @property
    def mongo(self):
        return self.application.mongo

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        # 通过IP检测是否刷量
        if self.cracker_controller(self.request.remote_ip):
            raise tornado.web.HTTPError(400)

    #刷量控制器
    def cracker_controller(self, key):
        '''每次api请求都检查请求来源ip与设备信息，根据防止数量。
           相同IP每1分钟允许1次
        '''
        cc_key = hashlib.md5(key).hexdigest()
        if not self.redis.get(cc_key):
            self.redis.setex(cc_key, self.request.body, ip_expires)
            return False
        else:
            return True

class DuangHandler(BaseHandler):
    def get(self):
        self.write("duang.guru is work!")
        
    def post(self):
        try:
            arguments = eval(self.request.body)
            print type(arguments)
            text = arguments["text"]
            url = arguments["url"]
            title = arguments["title"]
            comment = arguments["comment"]
        except Exception,e:
            print "***add duang error(in DuangHandler.post())***:",e
            raise tornado.web.HTTPError(405)
        else:
            if not self.add_duang(title, url, text, comment):
                raise tornado.web.HTTPError(406)
            self.finish()

    def add_duang(self, title, url, text, comment):
        _duang=dict(title=title, url=url, text=text, comment=comment)
        #获取UA信息
        _duang["user_agent"] = self.request.headers["User-Agent"]
        #获取IP地址
        _duang["ip"] = self.request.remote_ip
        #解析域名
        _duang["host_name"] = get_host(url)
        #设置created_at
        _duang["created_at"] = datetime.datetime.utcnow()
        #存储数据
        return self.mongo.duang.save(_duang, w=1)
    
class DuangListHandler(BaseHandler):
    def get(self):
        items = self.mongo.duang.find()
        if self.request.arguments == {}:
            self.render('index.html',items=items)
        else:
            _id = ''.join(self.request.arguments['_id'])
            verify = self.request.arguments['verify'][0]
            verify_at = datetime.datetime.utcnow()
            self.mongo.duang.update({'_id':ObjectId(_id)},{'$set':{'verify':verify,'verify_at':verify_at}})                  
        
class ChannelListHandler(BaseHandler):
    def get(self):
        items = self.mongo.channel.find()
        if self.request.arguments == {}:
            self.render('channel-list.html', items=items, items_=items)        
        elif self.request.arguments['type'][0] == 'addRecord':
            self.mongo.channel.save({
                'name':self.request.arguments['name'][0],
                'website':self.request.arguments['website'][0],
                'email':self.request.arguments['email'][0],
                'duang':int(0),
                'verify':int(0),
                'created_at':datetime.datetime.utcnow()
            })   
        elif self.request.arguments['type'][0].split('_')[0] == 'edit':
            _id = self.request.arguments['type'][0].split('_')[1]
            self.mongo.channel.update({
            '_id':ObjectId(_id)}, {
            '$set': {'name':self.request.arguments['name'][0],
                'website':self.request.arguments['website'][0],
                'email':self.request.arguments['email'][0]}
            }, w=1)
        else:
            _id = self.request.arguments['type'][0].split('_')[1]
            self.mongo.channel.remove({'_id':ObjectId(_id)})
            

def main():
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen( options.port )
    print  "PORT: %d " % (options.port)
    ioloop.IOLoop.instance().start()

    
if __name__ == '__main__':
    print "Starting server..."
    main()
    print "Started."



# main function
if __name__ == '__main__':
    pass

