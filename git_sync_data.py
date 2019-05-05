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

#origin1_arr =['https://github.com/electryone/git-auto-commit.git','origin','master','连接96端网络']
origin2_arr = ['http://admin@127.0.0.1:10010/r/git_sync.git','origin2','master','连接云中心端网络']
send_flag =True
mail_host = "smtp.163.com"  # 设置邮件服务器
mail_user = "*******@163.com"  # 用户名
mail_pass = "*******"  # 口令
sender = 'electrycache1@163.com'  # 发送邮件的邮箱
receivers = 'electrycache1@163.com'  # 接收邮件的邮箱，可设置为你的QQ邮箱或者其他邮箱，多个邮箱用,分隔开来

def send_mail(subject, message):
    # 创建一个带附件的实例
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = sender  # 邮件发送人
    message['To'] = receivers  # 邮件接收人
    # subject = '测试监测结果'  # 邮件主题
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print("Error: 无法发送邮件:{0}".format(e))


def remote_job(arr):
    date =time.asctime(time.localtime(time.time())) # datetime.datetime.today().isoformat()[0:10]
    pull_status = subprocess.run(["git", "pull",'-f',arr[1],arr[2]],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "fatal: unable to access" in str(pull_status.stdout):
        print("network error")
        return False
    
    #判别是否提交本地版本
    status = subprocess.run(["git", "status"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "fatal: unable to access" in str(status.stdout):
        print("network error")
        return False
    elif "nothing to commit" in str(status.stdout):
        print("nothing to commit, return")
        return True
    else:
        gadd = subprocess.run(["git", "add", "."],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    gcom = subprocess.run(["git", "commit", "-m" + date],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('commit message:{0}'.format(str(gcom.stdout)))
    push_status = subprocess.run(["git", "push",'-u',arr[1],arr[2]],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "fatal: unable to access" in str(push_status.stdout):
        print("network error")
        return False
    return True


def main():
    while True:
        flag = remote_job(origin1_arr)
        if(flag):
            print("check {0} ok".format(origin1_arr[0]))
            
        else:
            time.sleep(5)
            flag = remote_job(origin1_arr)
            if(flag == Flase):
                print("network fail count1 {0} count2{1}, send message".format(count1,count2))
                date =time.asctime(time.localtime(time.time()))
                if(send_flag):
                    string = '出现同步问题---'
                    string += "网络出现错误: {0} \n".format(origin1_arr[3])
                    send_mail('同步问题', string)  # 发送邮件
            else:
                print("check ok")
        break

print(time.asctime(time.localtime(time.time())))
main()