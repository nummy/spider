#! /usr/bin/python
# coding:utf8
import re
import json
import sqlite3
import random
import requests
import traceback
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

path = "/var/local/"
#path = "./"



logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(path + "log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def sendEmail(title, content):
    mail_host = "smtp.163.com"
    mail_user = "allen_li89"
    mail_pass = "8023@liuhui" 
    sender = "allen_li89@163.com"
    receivers = ["1591780418@qq.com"]
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def has_sent(tid):
    conn = sqlite3.connect(path + 'python.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM email WHERE topic_id=%s" % tid)
    conn.commit()
    row = cursor.fetchone()
    conn.close()
    return row is not None

def record(tid):
    conn = sqlite3.connect(path + 'python.db')
    cursor = conn.cursor()
    sql = "INSERT INTO email (topic_id) VALUES (%s)" % tid
    cursor.execute(sql)
    conn.commit()
    conn.close()


def create_db():
    conn = sqlite3.connect(path + 'python.db')
    cursor = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS topic(
        id INT PRIMARY KEY NOT NULL,
        title TEXT NOT NULL,
        url CHAR(100) NOT NULL,
        author CHAR(50) NOT NULL,
        publish_time CHAR(50),
        response_num INT,
        last_reply CHAR(50),
        keyword CHAR(50),
        create_time TIMESTAMP default (datetime('now', 'localtime')),
        update_time TIMESTAMP default (datetime('now', 'localtime'))
    )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS email(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INT NOT NULL
    )
    """
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insert_db(data):
    conn = sqlite3.connect(path + 'python.db')
    cursor = conn.cursor()
    sql = """
    INSERT INTO topic (id,title,url,author,publish_time, response_num, last_reply, keyword)
    VALUES (?,?,?,?,?,?,?,?)
    """
    cursor.execute(sql, data)
    conn.commit()
    conn.close()

def update_db(tid, last_reply, response_num):
    conn = sqlite3.connect(path + 'python.db')
    c = conn.cursor()
    sql = "UPDATE topic set last_reply=?, response_num=?, update_time=datetime('now', 'localtime') where id=?"
    c.execute(sql, (last_reply, response_num, tid))
    conn.close()

def get_topic(tid):
    conn = sqlite3.connect(path + 'python.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM topic WHERE id=%s" % tid)
    conn.commit()
    row = cursor.fetchone()
    conn.close()
    return row

def get_filters():
    words = []
    fp = open(path + "stopwords.txt", "r")
    for line in fp:
        line = line.strip()
        words.append(line)
    return words

def get_blacklist():
    words = []
    fp = open(path + "blacklist.txt", "r")
    for line in fp:
        line = line.strip()
        words.append(line)
    return words

filters = get_filters()
filter_authors = get_blacklist()


def get_total():
    html = requests.get(URL).content
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("a", "last pagination-item ")
    href = link["href"]
    index = href.find("pn=")
    total = href[index+3:]
    return int(total)

def get_page(index, keyword):
    url = "http://tieba.baidu.com/f?kw=%s&pn=%s" % (keyword, index)
    html = requests.get(url).content
    #html = open("a.html", "r", encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    lst = soup.find_all("li", " j_thread_list clearfix")
    for item in lst:
        url = None
        try:
            url = item.find(class_="threadlist_title").find("a").attrs["href"].strip()
            get_detail(item, keyword)
        except Exception as e:
            logger.error(u"链接:%s, 错误原因：%s" % (url, str(e)))
            traceback.print_exc()

def get_detail(item, keyword):
    url = item.find(class_="threadlist_title").find("a").attrs["href"].strip()
    tid = url.split("/")[2]
    url = "http://tieba.baidu.com%s" % url
    title = item.find(class_="threadlist_title").find("a").text.strip()
    for word in filters:
        if word in title:
            return
    publish_time = item.find(class_="is_show_create_time").text.strip()
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    if ":" in publish_time:
        arr = publish_time.split(":")
        hour = int(arr[0])
        minute = int(arr[1])
        publish_time = datetime(year, month, day, hour, minute).strftime("%Y-%m-%d %H:%M")
    elif "-" in publish_time:
        arr = publish_time.split("-")
        if len(arr[0]) == 4:
            year = int(arr[0])
            month = int(arr[1])
            day = 28
        else:
            month = int(arr[0])
            day = int(arr[1])
        publish_time = datetime(year, month, day).strftime("%Y-%m-%d %H:%M")
    author = item.find(class_="frs-author-name").text.strip()
    if author in filter_authors:
        return
    response_num = item.find(class_="threadlist_rep_num").text.strip()
    last_reply = item.find(class_="threadlist_reply_date").text.strip()
    if get_topic(tid):
        update_db(tid, last_reply, response_num)
    else:
        data = (tid,title,url,author,publish_time, response_num, last_reply, keyword)
        insert_db(data)
        keys = [u"作业", u"有偿", u"任务"]
        for key in keys:
            if key in title:
                if not has_sent(tid):
                    print("record" +  str(tid))
                    record(tid)
                    #sendEmail(title, url)
                break


if __name__ == "__main__":
    create_db()
    time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    logger.info(u"调度开始时间:%s" % time)
    for i in range(26):
        logger.info(u"爬取第%s页数据" % i)
        get_page(i*50, "python")
        get_page(i*50, "python3")
        get_page(i*50, "java")
        get_page(i*50, u"python爬虫")
    time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    logger.info(u"调度结束时间:%s" % time)
