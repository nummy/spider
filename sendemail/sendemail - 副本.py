# coding:utf-8
import smtplib
from email.header import Header
from email.mime.text import MIMEText
 

mail_host = "smtp.163.com"
mail_user = "用户名"
mail_pass = "用户密码"
 
sender = '发送者邮箱' 

 
content = """
正文内容
"""
title = "标题"
 
def sendEmail(email_addr):
    message = MIMEText(content, 'plain', 'utf-8') 
    message['From'] = "{}".format(sender)
    message['To'] = ",".join([email_addr])
    message['Subject'] = title
 
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465) 
        smtpObj.login(mail_user, mail_pass) 
        smtpObj.sendmail(sender, [email_addr], message.as_string()) 
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

def get_qq_lst():
    fp = open("result1.txt")  #  QQ号列表，一行一个
    qq_lst = []
    for line in fp:
        line = line.strip()
        qq_lst.append(line)
    return qq_lst

if __name__ == '__main__':
    qq_lst = get_qq_lst()
    for qq in qq_lst:
        email_addr = "%s@qq.com" % qq
        sendEmail(email_addr)
