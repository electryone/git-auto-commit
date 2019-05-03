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
    message['From'] = "*****@163.com"  # 邮件发送人
    message['To'] = "*****@163.com"  # 邮件接收人
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


def job():
    f = open('content.txt', 'a')
    f.write(time.asctime(time.localtime(time.time())) + '\n')
    date = datetime.datetime.today().isoformat()[0:10]
    status = subprocess.run(["git", "status"])
    print(status)
    print('**********start git add.**********')
    gadd = subprocess.run(["git", "add", "."])
    print('**********git add done.**********')
    print('**********start git commit.**********')
    gcom = subprocess.run(["git", "commit", "-m" + date])
    print('**********git commit done.**********')
    print('**********start git push.**********')
    gpush = subprocess.run(["git", "push", "origin", "master"])
    print('**********git push done.**********')
    send_mail("git a commit", str(date))  # 发送邮件
    time.sleep(61)


def main(h, m):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        job()
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            print(now.hour, ' ', now.minute, ' ', now.microsecond)
            # 到达设定时间，结束内循环
            if now.hour == h and now.minute == m:
                break
            # 不到时间就等20秒之后再次检测
            time.sleep(20)
        # 做正事，一天做一次
        #job()


print(time.asctime(time.localtime(time.time())))
main(23, 55)
