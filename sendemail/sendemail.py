# coding:utf-8
import smtplib
from email.header import Header
from email.mime.text import MIMEText
 

mail_host = "smtp.163.com"
mail_user = "allen_li89"
mail_pass = "8023@liuhui"
 
sender = 'allen_li89@163.com' 
receivers = ['1591780418@qq.com'] 
 
content = """
招人代写，数学，统计，python，java，C++，数据库、js，excel，html,R，机器学习，算法等作业，要求熟悉英文，
能写英文report更佳，群号122348080
"""
title = "持续招人代写留学生作业"
 
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
    fp = open("result1.txt")
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
    sendEmail("1591780418@qq.com")
