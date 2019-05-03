#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 22:49
# @Author  : Huyd
# @Site    : 
# @File    : git-auto-commit.py
# @Software: PyCharm
import datetime
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import re
import schedule
import time


def send_mail(subject, message):
    mail_host = "smtp.163.com"  # 设置邮件服务器
    mail_user = "electrycache1@163.com"  # 用户名
    mail_pass = "21897594"  # 口令

    sender = 'electrycache1@163.com'  # 发送邮件的邮箱
    receivers = 'electrycache1@163.com'  # 接收邮件的邮箱，可设置为你的QQ邮箱或者其他邮箱，多个邮箱用,分隔开来

    # 创建一个带附件的实例
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = "electrycache1@163.com"  # 邮件发送人
    message['To'] = "electrycache1@163.com"  # 邮件接收人
    # subject = '测试监测结果'  # 邮件主题
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def local_job():
    date =time.asctime(time.localtime(time.time())) # datetime.datetime.today().isoformat()[0:10]
    #status = subprocess.run(["git", "status"])
    status = subprocess.run(["git", "status"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "fatal: unable to access" in str(status.stdout):
        print("network error")
        return False
    elif "nothing to commit" in str(status.stdout):
        print("nothing to commit, return")
        return True
    elif "no changes added to commit" in str(status.stdout):
        gadd = subprocess.run(["git", "add", "."],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#        print('add message:{0}'.format(str(gadd.stdout)))
    gcom = subprocess.run(["git", "commit", "-m" + date],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('commit message:{0}'.format(str(gcom.stdout)))
    return True

def main():
    flag = local_job()
    
print(time.asctime(time.localtime(time.time())))
main()
