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


origin2_arr =['https://github.com/electryone/git-auto-commit.git','origin','master']
origin1_arr = ['http://admin@127.0.0.1:10010/r/git_sync.git','origin2','master']

def remote_job(arr):
    #date =time.asctime(time.localtime(time.time())) # datetime.datetime.today().isoformat()[0:10]
    #处理origin1_arr
    flag1 = True
    pull_status = subprocess.run(["git", "pull",'-f',arr[1],arr[2]],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "fatal: unable to access" in str(pull_status.stdout):
        print("network error")
        return False
    
    push_status = subprocess.run(["git", "push",'-u',arr[1],arr[2]],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if "fatal: unable to access" in str(push_status.stdout):
        print("network error")
        flag1 = False
    return flag1


def main(h, m):
    '''h表示设定的小时，m为设定的分钟'''
    count1= 0
    count2= 0
    while True:
        flag = remote_job(origin1_arr)
        if(flag == False):
            count1 +=1
        else:
            print("check {0} ok".format(origin1_arr[0]))
       
        flag = remote_job(origin2_arr)
        if(flag == False):
            count2 +=1
        else:
            print("check {0} ok".format(origin2_arr[0]))

        time.sleep(5)
        #重新检查一遍，防止网络问题导致失败
        if(count1 >1):
             flag = remote_job(origin1_arr)
             if(flag == True):
                 count1 = 0
                 
        if(count2 >1):
             flag = remote_job(origin2_arr)
             if(flag == True):
                 count2 = 0       
        
        if(count1 >0 or count2 >0):
            print("network fail count1 {0} count2{1}, send message".format(count1,count2))
            date =time.asctime(time.localtime(time.time()))
            string = 'git issue:'
            if(count1 >0):
                string += "network error: {0} \n".format(origin1_arr[0])
            if(count2 >0):
                string += "network error: {0} \n".format(origin2_arr[0])   
            send_mail('git issue', string)  # 发送邮件
        else:
            print("check ok")
        break


print(time.asctime(time.localtime(time.time())))
main(23, 55)
