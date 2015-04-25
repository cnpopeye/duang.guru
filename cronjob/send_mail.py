#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, string, socket
import smtplib
import datetime
import gevent
import pymongo
import time
import chardet
#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText
from conf import  mail_host, mail_user, mail_pass, mongo


subject_template = "[duang.guru提示内容有误]:%s"
content_template = '''

Duang的一下，duang.guru 发现以下信息好像不太对哦！提醒您，请检查。

-----
%s,
%s,
%s
-----
duang.guru是挖掘和发现信息偏差的社区。
duang.guru的宗旨是提高信息质量，传递正确的给用户。

联系duang.guru，请邮件{asda@duang.guru}。
请不要直接回复邮件。
http://duang.guru
'''

def send_mail(mailto_list, sub,content):
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = ";".join(mailto_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(mail_user, mailto_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def get_mongo():
    try:
        connection = pymongo.Connection( host = mongo["host"], port = mongo["port"], max_pool_size = mongo["max_pool_size"] )
        db_handler = connection[mongo["dbn"]]
        if mongo["user"]:
            db_handler.authenticate( mongo["user"], mongo["passwd"] )
    except Exception, e:
        print "mongodb init error:" + str( e )
        sys.exit( 1 )
    return db_handler


mongo = get_mongo()

def get_duang():
    ""
    return mongo.duang.find({"verify":True, "sent_at":-1})

def get_channel(host_name):
    return mongo.source.find_one({"website":host_name})

def get_source_email(host_name):
    source = get_channel(host_name)
    return source["support_email"]
    
def set_sent_status(duang_id):
    mongo.duang.update({"_id":duang_id}, {"$set":{"sent_at":datetime.datetime.utcnow()}})

def send():
    duangs = get_duang()
    jobs = []
    for duang in duangs:
        mailto_list = [get_source_email(duang["host_name"])]
        title = duang["title"].encode('utf-8')
        url = duang["url"].encode('utf-8')
        text = duang["text"].encode('utf-8')
        subject = subject_template % title
        content = content_template % (title, url, text)
        if send_mail(mailto_list, subject, content):
            set_sent_status(str(duang["_id"]))
            print "just sent one:",str(duang["_id"]),"let me yo-yo."
            time.sleep(15)


if __name__ == '__main__':
    is_first = False
    while True:
        if not is_first: 
            print "focus on work, hard work!"
            is_first = False
        send()
