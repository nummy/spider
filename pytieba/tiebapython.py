#! /usr/bin/python
# coding:utf-8
import re
import json
import sqlite3
import random
import requests
import traceback
import logging
from datetime import datetime
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def create_db():
    conn = sqlite3.connect('python.db')
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
        create_time TIMESTAMP default (datetime('now', 'localtime')),
        update_time TIMESTAMP default (datetime('now', 'localtime'))
    )
    """
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insert_db(data):
    conn = sqlite3.connect('python.db')
    cursor = conn.cursor()
    sql = """
    INSERT INTO topic (id,title,url,author,publish_time, response_num, last_reply)
    VALUES (?,?,?,?,?,?,?)
    """
    cursor.execute(sql, data)
    conn.commit()
    conn.close()

def update_db(tid, last_reply, response_num):
    conn = sqlite3.connect('python.db')
    c = conn.cursor()
    sql = "UPDATE topic set last_reply=?, response_num=?, update_time=datetime('now', 'localtime') where id=?"
    c.execute(sql, (last_reply, response_num, tid))
    conn.close()

def get_topic(tid):
    conn = sqlite3.connect('python.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM topic WHERE id=%s" % tid)
    conn.commit()
    row = cursor.fetchone()
    conn.close()
    return row


URL = "http://tieba.baidu.com/f?kw=python"

filters = [u"资料", u"免费", u"广告", u"培训", u"分享",u"资源", u"心得",
u"学好", u"交流", u"视频",u"教程",u"福音", u"心得", u"最热", u"教材", u"实战", u"进阶"]
filter_authors = [u"qq191501000", u"飞凡5520", u"z7912846",u"啊贤哥仔"]


def get_total():
    html = requests.get(URL).content
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("a", "last pagination-item ")
    href = link["href"]
    index = href.find("pn=")
    total = href[index+3:]
    return int(total)

def get_page(index):
    url = URL + "&pn=%s" % index
    html = requests.get(url).content
    #html = open("a.html", "r", encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    lst = soup.find_all("li", " j_thread_list clearfix")
    for item in lst:
        url = None
        try:
            url = item.find(class_="threadlist_title").find("a").attrs["href"].strip()
            get_detail(item)
        except Exception as e:
            logger.error(u"链接:%s, 错误原因：%s" % (url, str(e)))
            traceback.print_exc()

def get_detail(item):
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
        data = (tid,title,url,author,publish_time, response_num, last_reply)
        insert_db(data)


if __name__ == "__main__":
    create_db()
    time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    logger.info(u"调度开始时间:%s" % time)
    for i in range(26):
        logger.info(u"爬取第%s页数据" % i)
        get_page(i*50)
    time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    logger.info(u"调度结束时间:%s" % time)
