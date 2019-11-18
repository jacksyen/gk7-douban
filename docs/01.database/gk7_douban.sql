/*
MySQL Data Transfer
Source Host: localhost
Source Database: gk7_douban
Target Host: localhost
Target Database: gk7_douban
Date: 6/4/2015 下午 1:59:22
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for gk7_douban_book_img
-- ----------------------------
DROP TABLE IF EXISTS `gk7_douban_book_img`;
CREATE TABLE `gk7_douban_book_img` (
  `images_id` varchar(32) NOT NULL COMMENT '图片ID',
  `book_id` varchar(32) NOT NULL COMMENT '书籍ID(关联Books主键)',
  `book_images_remote_path` longtext NOT NULL COMMENT '书籍图片远程路径字符串',
  `book_images_local_path` longtext COMMENT '书籍图片本地路径字符串',
  `addtime` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '新增时间',
  `updatetime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY  (`images_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for gk7_douban_books
-- ----------------------------
DROP TABLE IF EXISTS `gk7_douban_books`;
CREATE TABLE `gk7_douban_books` (
  `id` varchar(32) NOT NULL COMMENT '表ID',
  `ebook_id` varchar(32) NOT NULL COMMENT '豆瓣书籍ID',
  `book_title` varchar(512) NOT NULL COMMENT '书籍标题',
  `book_subtitle` varchar(512) default NULL COMMENT '书籍副标题',
  `book_author` varchar(32) default NULL COMMENT '书籍作者',
  `book_file_path` varchar(1024) default NULL COMMENT '书籍本地文件路径',
  `book_size` int(11) NOT NULL COMMENT '书籍大小',
  `book_cover_local_path` varchar(1024) default NULL COMMENT '书籍封面本地路径',
  `book_cover_remote_path` varchar(1024) default NULL COMMENT '书籍封面远程路径',
  `addtime` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '新增时间',
  `updatetime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for gk7_douban_wait_converts
-- ----------------------------
DROP TABLE IF EXISTS `gk7_douban_wait_converts`;
CREATE TABLE `gk7_douban_wait_converts` (
  `convert_id` varchar(32) NOT NULL COMMENT '转换ID',
  `request_user` varchar(512) NOT NULL COMMENT '请求用户',
  `book_html_local_path` varchar(1024) NOT NULL COMMENT '书籍本地HTML路径',
  `book_convert_file_path` varchar(1024) default NULL COMMENT '转换后的书籍本地文件路径',
  `convert_status` varchar(32) NOT NULL COMMENT '转换状态',
  `addtime` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '新增时间',
  `updatetime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY  (`convert_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for gk7_douban_wait_emails
-- ----------------------------
DROP TABLE IF EXISTS `gk7_douban_wait_emails`;
CREATE TABLE `gk7_douban_wait_emails` (
  `email_id` varchar(32) NOT NULL,
  `email_to_user` varchar(512) NOT NULL,
  `email_attach_file` varchar(512) default NULL,
  `email_title` varchar(512) NOT NULL,
  `email_auth` varchar(32) default NULL,
  `email_send_status` varchar(32) NOT NULL,
  `addtime` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '新增时间',
  `updatetime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY  (`email_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
