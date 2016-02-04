ALTER TABLE `gk7_douban`.`gk7_douban_wait_emails` 
ADD COLUMN `email_user_id` VARCHAR(512) NULL COMMENT '用户ID，格式：13位时间戳_用户kindle邮箱' AFTER `email_to_user`;
