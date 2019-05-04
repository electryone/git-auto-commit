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
import time

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
    gcom = subprocess.run(["git", "commit", "-m" + date],shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('commit message:{0}'.format(str(gcom.stdout)))
    return True

def main():
    flag = local_job()
    
print(time.asctime(time.localtime(time.time())))
main()
