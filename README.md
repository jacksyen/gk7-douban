# 豆瓣阅读推送至kindle，chrome插件及服务端

##Table of Contents

- [目录说明](#目录说明)
- [实现逻辑](#实现逻辑)
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
- [捐助](#捐助)


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

## 实现逻辑 ##

### 客户端 ###

### 服务端 ###

#### 主流程 ####
```flow
st=>start: 客户端请求
e=>end
op=>operation: 解析请求字符串
op_emails=>operation: 存储待发送邮件
cond=>condition: 判断书籍是否存在?
cond_book_file=>condition: 判断书籍文件是否存在?
op_yes_book_file=>operation: 更新待发送邮件附件信息
op_yes_book_file_send=>operation: 发送邮件
op_update_email=>operation: 更新待发送邮件状态
op_page=>operation: 创建书籍HTML页面
op_save_book=>operation: 存储书籍信息
cond_book_img=>condition: 书籍是否存在图片
op_yes_book_img=>operation: 存储书籍图片信息
op_book_wait_html=>operation: 存储书籍待转换信息
op_sync_thread=>operation: 启动异步线程

st->op->op_emails->cond
cond(no)->op_page->op_save_book->cond_book_img
cond(yes)->cond_book_file
cond_book_file(yes)->op_yes_book_file->op_yes_book_file_send->op_update_email->e
cond_book_file(no)->e
cond_book_img(yes)->op_yes_book_img->op_book_wait_html->op_sync_thread->e
cond_book_img(no)->op_book_wait_html
```

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
1. 修改全局配置
```bash
sed -i "s/GLOBAL_EMAIL_USER = 'hyqiu.syen@gmail.com'/GLOBAL_EMAIL_USER = '你的gmail邮箱地址'/g" webglobal/globals.py
sed -i "s/GLOBAL_EMAIL_PWD = ''/GLOBAL_EMAIL_PWD = '你的gmail密码'/g" webglobal/globals.py
```
2. 启动：
```bash
sudo python index.py 8000
```

### chrome下加载开发插件 ###

1. 修改插件推送的后台地址url，编辑client/scripts/background.js，在send函数中修改url地址，和上面服务器端启动的IP/端口对应
2. 在chrome浏览器中的地址栏中输入：[扩展程序](chrome://extensions/)，点击**加载正在开发的扩展程序**，选择`client`文件夹即可

## 版本历史 ##

### v2.3 ###
+ 服务端存储书籍信息，如果存在一样的图书，直接推送
+ 书籍图片多线程抓取
+ 优化图书排版
+ 图书章节按照[class=pagebreak]分割
+ 客户端CSS优化，不干涉主页面

## 待优化 ##
+ 文件路径规范
+ 豆瓣文章ID存储
+ 客户端并发控制
+ HTTP传输数据大太，导致处理比较慢[传输数据压缩；nginx处理]
+ 客户端邮件设置优化

## 捐助 ##
