- 写在前面
> - 协议: HTTP 1.1
> - 数据交互：json

**API请求通过HTTP Status Code来区分:**
> - status =200为请求成功，错误信息参考返回信息。
> - status!=200为非正常结果，需要做对应处理。


- API有效性验证
pass

- HTTP状态码

HTTP Status Code |  返回值 | 说明
----------------------|----------|---------
200 | 返利操作结果 |  请求成功，返回操作结果及状态码
403 | API验证失败信息提示 | API验证失败
500 | 错误信息提示 |系统错误

- Add Duang
> - uri: /duang
> - method: POST

> - 鼠标选中错别字，获取错别字前后100个字。
post数据时，错别字使用`>>><<<`标注。

 - 参数:
```
   {
     "title":"网页标题",
     "url":"http:/sdfa.com/asdf/asdf.html",
     "text":"错别字>>>别字<<<文字",
     "comment":"正确的字和理由"
   }
```

 - 返回值:
 >  http status 200
