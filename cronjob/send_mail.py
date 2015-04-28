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

def send_mail(mailto_list, sub, content):
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

def set_channel(host_name):
    new_source = dict(
        name=host_name,
        website=host_name,
        support_email=host_name,
        created_at=datetime.datetime.utcnow(),
        duang=0,
        verify=0,
        response=0)
    mongo.source.save(new_source)

def get_source_email(host_name):
    mailto = []
    source = get_channel(host_name)
    if source is None:
        #添加渠道信息
        set_channel()
    else:
        support_email = source.get("support_email",None)
    if mailto is not None:
        mailto = [support_email]
    return mailto
    
def set_sent_status(duang_id):
    mongo.duang.update({"_id":duang_id}, {"$set":{"sent_at":datetime.datetime.utcnow()}})

def send():
    os.environ["DUANG_SENDING"]="Y"
    duangs = get_duang()
    for duang in duangs:
        mailto_list = get_source_email(duang["host_name"])
        if not mailto_list:
            print "to be continue."
            continue 
        title = duang["title"].encode('utf-8')
        url = duang["url"].encode('utf-8')
        text = duang["text"].encode('utf-8')
        subject = subject_template % title
        content = content_template % (title, url, text)
        if send_mail(mailto_list, subject, content):
            set_sent_status(duang["_id"])
            print "just sent one:",str(duang["_id"]),"let me yo-yo."
            time.sleep(15)
    os.environ["DUANG_SENDING"]="N"


if __name__ == '__main__':
    if os.environ.get('DUANG_SENDING', "N" )=="N":
        print "focus on work, hard work!"
        send()
    else:
        print "Not Found Duang, let me yo-yo ^_^!"

