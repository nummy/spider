# coding:utf-8
import re
import csv
import json
import random
import requests
import threading
from bs4 import BeautifulSoup

URL = "http://tieba.baidu.com/f?kw=python"

def get_total():
    html = requests.get(URL).content
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("a", "last pagination-item ")
    href = link["href"]
    index = href.find("pn=")
    total = href[index+3:]
    return int(total)

def get_page(index, output):
    url = URL + "&pn=%s" % index
    html = requests.get(URL).content.decode("utf-8")
    #html = open("a.html", "r", encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    lst = soup.find_all("li", " j_thread_list clearfix")
    for item in lst:
        get_detail(item, output)

def get_detail(item, output):
    url = item.find(class_="threadlist_title").find("a").attrs["href"].strip()
    tid = url.split("/")[2]
    url = "http://tieba.baidu.com%s" % url
    title = item.find(class_="threadlist_title").find("a").text.strip()
    create_time = item.find(class_="is_show_create_time").text.strip()
    author = item.find(class_="frs-author-name").text.strip()
    response_num = item.find(class_="threadlist_rep_num").text.strip()
    last_reply = item.find(class_="threadlist_reply_date").text.strip()
    data = {
        "ID": tid,
        "链接": url, 
        "标题": title,
        "作者": author,
        "发布时间": create_time,
        "回复数":response_num,
        "最后回帖时间":last_reply
    }
    output.writerow(data)


def get_ips():
    r = requests.get('http://192.168.137.28:5000/')
    ip_ports = json.loads(r.text)
    return ip_ports

def get_random_proxy(ip_ports):
    ip_port = random.choice(ip_ports)
    ip = ip_port[0]
    port = ip_port[1]
    proxies={
        'http':'http://%s:%s'%(ip,port),
        'https':'http://%s:%s'%(ip,port)
    }
    return proxies



if __name__ == "__main__":
    fp = open("result.csv", "w",encoding="utf-8-sig", newline="")
    headers = ["ID","链接","标题","作者","发布时间","回复数","最后回帖时间"]
    output = csv.DictWriter(fp, fieldnames=headers)
    output.writeheader()
    for i in range(50):
        print(i)
        get_page(i, output)
    fp.close()
