#!/usr/bin/python

import os
import time

DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'root'
DB_NAME = 'note'
BACKUP_PATH = '/tmp'

file_name = time.strftime('%Y-%m-%d-%H_%M_%S') + '.sql'
backup_file = os.path.join(BACKUP_PATH, file_name)
tar_name = '%s.tar.gz' % (DB_NAME,)

dumpcmd = "mysqldump -u %s -p%s %s > %s" % (DB_USER, DB_USER_PASSWORD, DB_NAME, backup_file)
dump_result = os.system(dumpcmd)

if dump_result == 0:
    tar_cmd = 'tar zcf %s %s' % (tar_name, backup_file)
    os.system(tar_cmd)

##########################send email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

sender = ''
receiver = ''
smtpserver = ''
username = ''
password = ''

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'Backup'
msgRoot['From'] = 'Backup <%s>' % (sender, )
# 构造附件
att = MIMEText(open(tar_name, 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/x-compressed'
att["Content-Disposition"] = 'attachment; filename="backup.tar.gz"'
msgRoot.attach(att)
smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msgRoot.as_string())
smtp.quit()
# 删除tar文件
os.remove(tar_name)
