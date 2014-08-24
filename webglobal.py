# -*- coding:utf-8 -*-
# webglobal.py --- 
# 
# Filename: webglobal.py
# Description: 
# Author: jacksyen
# Maintainer: 
# Created: 二  8月  5 23:15:01 2014 (+0800)
# Version: 
# Package-Requires: ()
# Last-Updated: 周三 八月  6 09:54:53 2014 (+0800)
#           By: Administrator
#     Update #: 11
# URL: 
# Doc URL: 
# Keywords: 
# Compatibility: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change Log:
# 更新缴费号码信息
# 
# 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
# 
# 

# Code:
class Global:

    GLOBAL_ACCOUNT = [
        # 水费
        # 直接成功
        {'userCode': '1000001', 'userName': '东家', 'queryStatus': 'true', 'queryResultCode': '0000000', 'address': '重庆市渝中区88号', 'memo': '缴费成功', 'paymentMoney': 120.00, 'paymentStatus': 'SUCCESS', 'paymentResultCode': '0000000', 'paymentType': '000010'},
        # 直接失败
        {'userCode': '1000002', 'userName': '李嘉家', 'queryStatus': 'true', 'queryResultCode': '0000000', 'address': '重庆市江北区999号', 'memo': '缴费失败', 'paymentMoney': 20.00, 'paymentStatus': 'FAIL', 'paymentResultCode': '0000106', 'paymentType': '000010'},
        # 挂起转失败
        {'userCode': '1000003', 'userName': '李嘉家', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市江北区999号', 'memo': '缴费处理中', 'paymentMoney': 10.90, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'paymentType': '000010', 'rechangeStatus': 'FAIL'},
        # 挂起转成功
        {'userCode': '1000004', 'userName': '李家', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市渝北区109号', 'memo': '缴费处理中', 'paymentMoney': 101.01, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'paymentType': '000010', 'rechangeStatus': 'SUCCESS'},
        # 一直挂起
        {'userCode': '1000005', 'userName': '郑中', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市江北区999号', 'memo': '缴费处理中', 'paymentMoney': 10.90, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'isHangup': 1, 'paymentType': '000010'},
        # 异常
        {'userCode': '1000006', 'userName': '阿訇', 'queryStatus': 'false', 'queryResultCode': '0000205', 'paymentType': '000010'},
        # 没有欠费信息
        {'userCode': '1000008', 'userName': '周博', 'queryStatus': 'true', 'queryResultCode': '0000121', 'paymentType': '000010'},

        # 气费
        # 直接成功
        {'userCode': '2000001', 'userName': '么么', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市渝中区门店8号', 'memo': '缴费成功', 'paymentMoney': 312.88, 'paymentStatus': 'SUCCESS', 'paymentResultCode': '0000000', 'paymentType': '000020'},
        # 直接失败
        {'userCode': '2000002', 'userName': '刘尼', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市江北区洋河北路10号', 'memo': '缴费失败', 'paymentMoney': 39.09, 'paymentStatus': 'FAIL', 'paymentResultCode': '0000106', 'paymentType': '000020'},
        # 挂起转失败
        {'userCode': '2000003', 'userName': '哈格', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市九龙坡区12号', 'memo': '缴费处理中', 'paymentMoney': 19.10, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'paymentType': '000020', 'rechangeStatus': 'FAIL'},
        # 挂起转成功
        {'userCode': '2000004', 'userName': '哈格', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市九龙坡区12号', 'memo': '缴费处理中', 'paymentMoney': 19.10, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'paymentType': '000020', 'rechangeStatus': 'SUCCESS'},
        # 一直挂起
        {'userCode': '2000005', 'userName': '郑中', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市江北区999号', 'memo': '缴费处理中', 'paymentMoney': 10.90, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'isHangup': 1, 'paymentType': '000020'},
        # 异常
        {'userCode': '2000006', 'userName': '阿訇', 'queryStatus': 'false', 'queryResultCode': '0000205', 'paymentType': '000020'},
        # 没有欠费信息
        {'userCode': '2000008', 'userName': '张尼', 'queryStatus': 'true', 'queryResultCode': '0000121', 'paymentType': '000020'},

        # 电费
        # 直接成功
        {'userCode': '3000001', 'userName': '占方式', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市渝中区11号', 'memo': '缴费成功', 'paymentMoney': 81.20, 'paymentStatus': 'SUCCESS', 'paymentResultCode': '0000000', 'paymentType': '000030'},
        # 直接失败
        {'userCode': '3000002', 'userName': '张三丰', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市江北区健康路121号', 'memo': '缴费失败', 'paymentMoney': 9.02, 'paymentStatus': 'FAIL', 'paymentResultCode': '0000106', 'paymentType': '000030'},
        # 挂起转失败
        {'userCode': '3000003', 'userName': '杨富', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市渝中区龙组路89号', 'memo': '缴费处理中', 'paymentMoney': 190.90, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'paymentType': '000030', 'rechangeStatus': 'FAIL'},
        # 挂起转成功
        {'userCode': '3000004', 'userName': '高建', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市渝中区龙组路89号', 'memo': '缴费处理中', 'paymentMoney': 190.90, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'paymentType': '000030', 'rechangeStatus': 'SUCCESS'},
        # 一直挂起
        {'userCode': '3000005', 'userName': '郑中', 'queryStatus': 'true', 'queryResultCode': '0000000','address': '重庆市江北区999号', 'memo': '缴费处理中', 'paymentMoney': 10.90, 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'isHangup': 1, 'paymentType': '000030'},
        # 异常
        {'userCode': '3000006', 'userName': '阿訇', 'queryStatus': 'false', 'queryResultCode': '0000205', 'paymentType': '000030'},
        # 没有欠费信息
        {'userCode': '3000008', 'userName': '王博', 'queryStatus': 'true', 'queryResultCode': '0000121', 'paymentType': '000030'},

        # 手机充值
        # 直接成功
        {'userCode': '13983479195', 'paymentStatus': 'SUCCESS', 'paymentResultCode': '0000000', 'paymentType': '000040'},
        # 直接失败
        {'userCode': '18580238256', 'paymentStatus': 'FAIL', 'paymentResultCode': '0000106', 'paymentType': '000040'},
        # 挂起转失败
        {'userCode': '18523380869', 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'rechangeStatus': 'FAIL', 'paymentType': '000040'},
        # 挂起转成功
        {'userCode': '13164449448', 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'rechangeStatus': 'SUCCESS', 'paymentType': '000040'},
        # 一直挂起
        {'userCode': '15102355288', 'paymentStatus': 'HANGUP', 'paymentResultCode': '0000107', 'isHangup': 1, 'paymentType': '000040'}
    ]

    # 商户key
    GLOBAL_MERCHANTS = {'lencee': '9a7520152a7a97cfc76c82454463a83c'}

    '''sqlite3 数据表名称'''
    # 缴费表
    GLOBAL_TABLE_PAYMENT = 'easylife_payment_order'
    # 预存款表
    GLOBAL_TABLE_BALANCE = 'easylife_merchant_balance'
    # 缴费用户表
    GLOBAL_TABLE_PAYMENT_USER = 'easylife_payment_user'

    # 结果码
    GLOBAL_RESP_CODE = {
        '0000000': u'执行成功',
        '0000100': u'参数不合法',
        '0000101': u'可用余额小于缴费金额',
        '0000102': u'当前机构不可用或当前用户无此机构使用权限',
        '0000103': u'订单创建失败',
        '0000104': u'担保交易创建失败',
        '0000105': u'缴费过程中校验失败',
        '0000106': u'缴费失败',
        '0000107': u'缴费处理中',
        '0000108': u'缴费部分失败',
        '0000109': u'缴费前的处理失败',
        '0000110': u'数据未找到',
        '0000111': u'外部订单号已存在',
        '0000120': u'缴费用户不存在',
        '0000121': u'没有欠费信息',
        '0000122': u'缴费用户账户状态不正常',
        '0000123': u'没有抄表或缴费账单未生成',
        '0000124': u'用户上月未交费',
        '0000125': u'卡或表故障',
        '0000126': u'超过限定金额',
        '0000127': u'撤销缴费出错',
        '0000128': u'路由失败',
        '0000129': u'支付金额不能小于欠费金额',
        '0000130': u'支付金额必须等于欠费金额',
        '0000131': u'不在缴费时间段',
        '0000132': u'业务前置条件不满足',
        '0000133': u'返销处理中',
        '0000134': u'业务状态异常',
        '0000201': u'缴费系统远端执行异常',
        '0000202': u'缴费系统参数异常',
        '0000204': u'缴费系统远端返回系统级异常',
        '0000205': u'缴费系统远端返回未知异常',
        '0000300': u'账户金额冻结失败',
        '0000302': u'退款失败',
        '0000303': u'分润退款失败',
        '0000400': u'未知异常',
        '0000401': u'数据库访问异常',
        '0000402': u'交易系统网络异常',
        '0000403': u'缴费系统网络异常',
    }

    def __init__(self):
        pass

# 
# webglobal.py ends here
