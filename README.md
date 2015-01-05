# 豆瓣阅读推送至kindle
chrome插件及服务端

安装使用，请戳：[gk7-豆瓣阅读推送](https://chrome.google.com/webstore/detail/lmiobbkpdjmkfhgagdkpgbgonkogbllb)

---------

##Table of Contents

- [目录说明](#目录说明)
- [开发逻辑](#开发逻辑)
  - [客户端](#客户端)
  - [服务端](#服务端)
    - [主流程](#主流程)
    - [异步进程](#异步进程)
- [安装](#安装)
  - [依赖](#依赖)
  - [git检出](#git检出)
  - [ubuntu下使用服务端](#ubuntu下使用服务端)
  - [chrome下加载开发插件](#chrome下加载开发插件)
- [版本历史](#版本历史)
  - [v2.4](#v2.4)
  - [v2.3.3](#v2.3.3)
  - [v2.3.2](#v2.3.2)
  - [v2.3.1](#v2.3.1)
- [待优化](#待优化)

## 目录说明 ##
```
|———
|---- client 客户端代码
|---- db 数据库表操作
|---- helper 存放帮助类[切面日志、数据库连接、豆瓣文章解密、批量下载、发送邮件等]
|---- resources 资源，包含发布插件的图片
|---- static 后台静态资源存放目录
|---- templates 后台管理页面模板
|---- tools 存放工具类[HTML页面生成第三方工具]
|---- trans 接受客户端请求和异步线程处理
|---- webglobal 全局配置
|---- index.py 程序入口
```

## 开发逻辑 ##

### 客户端 ###

### 服务端 ###

#### 主流程 ####
![main_proc](https://raw.githubusercontent.com/jacksyen/gk7-douban/dev/resources/main_.png)


#### 异步进程 ####

## 安装 ##

### 依赖 ###

+ `git`
+ `python` 2.6 or later(but not 3.x)
+ `web.py`
+ `calibre`

### git检出 ###

+ dev: 开发分支
+ master: 主干分支，发布后由dev合并
```bash
git clone https://github.com/jacksyen/gk7-douban.git
git checkout dev
```

### ubuntu下使用服务端 ###

首先必须安装好依赖

* 修改全局配置
```bash
sed -i "s/GLOBAL_EMAIL_USER = 'hyqiu.syen@gmail.com'/GLOBAL_EMAIL_USER = '你的gmail邮箱地址'/g" webglobal/globals.py
sed -i "s/GLOBAL_EMAIL_PWD = ''/GLOBAL_EMAIL_PWD = '你的gmail密码'/g" webglobal/globals.py
```
* 启动：
```bash
sudo python index.py 8000
```

### chrome下加载开发插件 ###

1. 修改插件推送的后台地址url，编辑client/scripts/background.js，在 **send** 函数中修改 **url** 地址，和上面服务器端启动的IP/端口对应
2. 在chrome浏览器中的地址栏中输入：[chrome://extensions/](chrome://extensions/)，点击 **加载正在开发的扩展程序**，选择`client`文件夹即可

## 版本历史 ##

### v2.4.1 ###
+ 客户端书籍数据split优化

### v2.4 ###
+ 日志分割优化[按照midnight分割; error级别日志单独输出]
+ 书籍解析添加对contents->headline->text优化
+ 书籍中的posts有多组文章解析
+ 客户端email添加正则校验
+ 添加后台管理登录界面

### v2.3.3 ###
+ 书籍源文件和输出文件存储目录更改，格式：[主目录/作者/书名标题/书籍大小/]
+ 书籍表SQL更改，增加书籍唯一ID、书籍大小字段(主要是为了防止用户第一次推送为购买的书籍，第二次推送购买过的书籍出现缓存)

### v2.3.2 ###
+ 修复服务端抓取书籍图片bug

### v2.3.1 ###
+ 服务端存储书籍信息，如果存在一样的图书，直接推送
+ 书籍图片多线程抓取
+ 图书章节按照`[class=pagebreak]`分割
+ 客户端CSS优化，不干涉主页面

## 待优化 ##
+ 客户端并发控制
+ HTTP传输数据大太，导致处理客户端请求太慢
+ sqlite3库锁，写入并发导致数据库临时锁住
+ 配置移至配置文件中
+ 报刊内书籍解析有问题（部分内容丢失）
+ 使用rabbitmq抓取图片
+ 客户端gallery类书籍解析
+ HTML页面样式规范
