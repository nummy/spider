# coding:utf-8
import requests
import threading
from pymongo import MongoClient
from bs4 import BeautifulSoup

url = "http://tieba.baidu.com/f/index/forumpark"

def get_page(page):
    payload = {"cn":u"海外院校", "ci":0, "pci":0, "pcn":u"高等院校","ct":1, "st":"new", "pn":page}
    res = requests.get(url,params=payload)
    html = res.content
    return html

def get_info(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find(id="ba_list")
    contents = div.find_all("div", "ba_content")
    infos = []
    for content in contents:
        name = content.find("p", "ba_name").string  # name
        m = content.find("span", "ba_m_num").string # member
        p = content.find("span", "ba_p_num").string # tiezi
        desc = content.find("p", "ba_desc").string  # description
        if name is None:
            name = ""
        else:
            name = name.strip()
        if m is None:
            m = 0
        else:
            m = m.strip()
        if p is None:
            p = 0
        else:
            p = p.strip()
        if desc is None:
            desc = ""
        else:
            desc = desc.strip()
        infos.append([name, m, p, desc])
    return infos
    
def get_all(page, db):
    page = get_page(page)
    infos = get_info(page)
    for info in infos:
        campus = {"name":info[0], "m":int(info[1]), "p":int(info[2]), "desc":info[3]}
        db.insert(campus)

def main():
    client = MongoClient('localhost', 27017)
    db = client["demo"]
    campus = db["campus"]
    for i in range(1,19):
        threading.Thread(target=get_all, args=(i, campus)).start()
    

main()

