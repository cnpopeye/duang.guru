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


import tornado.web
import tornado.auth
from tornado import httpserver, ioloop
from tornado.options import define, options
import hashlib
import datetime
from util import get_mongo, get_redis, get_host
from config import DEBUG, ip_expires


define("port", default=8999, help="run on the given port", type=int)


class Application( tornado.web.Application ):
    def __init__( self ):

        urls = [
            ( r"/duang", DuangHandler),
            ]

        settings = dict(
            autoescape = None,
            xsrf_cookies=False,
            debug = DEBUG,
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
            text = arguments["text"]
            url = arguments["url"]
            title = arguments["title"]
        except Exception,e:
            print "add duang error(DuangHandler.post):",e
            raise tornado.web.HTTPError(405)
        else:
            if not self.add_duang(title, url, text):
                raise tornado.web.HTTPError(406)
            self.finish()

    def add_duang(self, title, url, text):
        _duang=dict(title=title, url=url, text=text)
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

