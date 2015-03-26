#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 
 AUTHOR: zc  
 HOST: zc@zcdeMacBook-Pro.local
 PATH: /Users/zc/workspace/duang.guru/app/tests.py
 DATE: 2015-03-02 19:52:11  
 
   
 INTRODUCTION:
    <<introduction write on here>>
     
 CHANGLOG:
    # FORMAT: DATE TIME AUTHOR COMMENT
    # etc. 2015-03-02 19:52:11 zc  # comment on here.
    
    <<changelog write on here>> 
    
  
'''


import unittest
import httplib
import urllib

host = 'localhost:8999'
#host = 'api.duang.guru'
post_data = '''{
    "title":"标题",
    "url":"http://sdfa.com/asdf/asdf.html",
    "text":"错别字>>>别字<<<文字",
    "comment":"这里是注解"
}'''

class TestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        "测试完毕清理测试数据"
        pass

class TestRebate(TestCase):
    def test_duang(self):
        res, data = send_request("/duang", post_data, host)
        print "data:", data
        print "res:",res
        self.assertEqual(res.status, 200)

        
def send_request(url, data=None, host='localhost:8082'):
    if data is None:
        params = url
    else:
        #params = urllib.urlencode( data)
        params = data

    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"
    }
    
    conn = httplib.HTTPConnection(host)
    if data is None:
        conn.request("GET", url, headers=headers)
    else:
        conn.request("POST", url, params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response, data


if __name__ == '__main__':
    unittest.main()


