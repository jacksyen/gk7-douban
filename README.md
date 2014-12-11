#豆瓣阅读推送至kindle，chrome插件及服务端#

##使用说明
```
python
sudo pip install web.py
sudo pip install sh
```


##实现逻辑
1. 客户端读取豆瓣阅读具体文章内容
  + 豆瓣内容存储在localStore中(使用豆瓣自定义加密)
  + 获取文章加密内容使用豆瓣加密js解密，然后使用base64编码
2. 客户端使用post请求至服务器
3. 服务器接收请求，使用base64解密，获取json数据
4. 根据kindle html规法生成html文件
5. 将待转换的数据信息存储在表中
6. 使用邮件服务发送至用户kindle邮件中
7. 返回状态

##待优化
+ 文件路径规范
+ 邮件服务用户存储
+ 豆瓣文章ID存储
+ CloundConvert服务调用次数存储
+ 客户端提示优化

##Change log
+ 推送至email先存储在sqlite表中，例如定时巡检发送邮件
+ 图书信息存储在sqlite中
+ 格式转换使用calibre中的`ebook-convert`命令
+ 使用python sh模块调用系统命令
