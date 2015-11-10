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
- [待优化](#待优化)

## <a name="目录说明">目录说明</a> ##
```
|———
|---- client 客户端代码
|---- db 数据库表操作
|---- docs 文档说明
|---- helper 存放帮助类[切面日志、数据库连接、豆瓣文章解密、批量下载、发送邮件等]
|---- resources 资源，包含发布插件的图片
|---- static 后台静态资源存放目录
|---- templates 后台管理页面模板
|---- tools 存放工具类[HTML页面生成第三方工具]
|---- trans 接受客户端请求和异步线程处理
|---- webglobal 全局配置
|---- index.py 程序入口
```

## <a name="开发逻辑">开发逻辑</a> ##

### <a name="客户端">客户端</a> ###

### <a name="服务端">服务端</a> ###

#### <a name="主流程">主流程</a> ####
![main_proc](https://raw.githubusercontent.com/jacksyen/gk7-douban/dev/resources/main_.png)


#### <a name="异步进程">异步进程</a> ####

## <a name="安装">安装</a> ##

### <a name="依赖">依赖</a> ###

+ `python` 2.6 or later(but not 3.x)
+ `web.py`
+ `celery`
+ `calibre`
+ `rabbitmq server`

### <a name="git检出">git检出</a> ###

+ dev: 开发分支
+ master: 主干分支，发布后由dev合并
```bash
git clone https://github.com/jacksyen/gk7-douban.git
git checkout dev
```

### <a name="ubuntu下使用服务端">ubuntu下使用服务端</a> ###

首先必须安装好依赖
```bash
pip install -r requirements.txt
sudo apt-get install calibre
sudo apt-get install rabbitmq-server

## mysql
sudo apt-get -y install libmysqlclient-dev python-dev
```

* 初始化数据库
[gk7_douban sql](https://github.com/jacksyen/gk7-douban/blob/dev/docs/gk7_douban.sql)

* 修改全局配置
```bash
// 建议修改rabbitmq默认密码
sudo rabbitmqctl change_password guest <newpwd>
// 修改发送email配置和连接数据库配置
vi webglobal/globals.py
// 修改celery配置
vi webglobal/celeryconfig.py
```
* 启动：
```bash
// celery服务端
su -
mkdir -p /var/log/celery
export C_FORCE_ROOT='root'
celery -A helper.tasks worker -l info -D -f /var/log/celery/gk7-douban.log --pidfile=/var/run/celery.pid
// 启动
sudo python index.py 8000
// 设置数据库权限
sudo chmod 666 <db name>
```

### <a name="chrome下加载开发插件">chrome下加载开发插件</a> ###

1. 修改插件推送的后台地址url，编辑client/scripts/background.js，在 **send** 函数中修改 **url** 地址，和上面服务器端启动的IP/端口对应
2. 在chrome浏览器中的地址栏中输入：[chrome://extensions/](chrome://extensions/)，点击 **加载正在开发的扩展程序**，选择`client`文件夹即可

## <a name="版本历史">版本历史</a> ##

[Changelog](https://github.com/jacksyen/gk7-douban/blob/dev/CHANGELOG.md)


## <a name="待优化">待优化</a> ##

+ 推送至个人邮箱
