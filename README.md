# 豆瓣阅读推送至kindle
chrome插件及服务端

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
  - [v2.3](#v2.3)
- [待优化](#待优化)

## 目录说明 ##
```
|———
|---- client 客户端代码
|---- db 数据库表操作
|---- helper 存放帮助类[切面日志、数据库连接、豆瓣文章解密、批量下载、发送邮件等]
|---- resources 资源，包含发布插件的图片
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

### v2.3.1 ###
+ 服务端存储书籍信息，如果存在一样的图书，直接推送
+ 书籍图片多线程抓取
+ 图书章节按照`[class=pagebreak]`分割
+ 客户端CSS优化，不干涉主页面

## 待优化 ##
+ 文件路径规范
+ 客户端并发控制
+ HTTP传输数据大太，导致处理客户端请求太慢
