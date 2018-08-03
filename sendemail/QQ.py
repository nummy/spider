import csv
import json
import time
import requests
from bs4 import BeautifulSoup


def get_qq():
    fp = open("result.txt")
    qq_lst = []
    for line in fp:
        line = line.strip()
        qq_lst.append(line)
    return qq_lst


qq_lst = get_qq()


def getPage(keyword):
    url = "http://tieba.baidu.com/f/search/res?qw="
    url = url +  keyword
    res = requests.get(url)
    return res.text


def parse(page, qq, keyword, output):
    soup = BeautifulSoup(page, "lxml")
    divs = soup.find_all(class_="s_post")
    for div in divs:
        try:
            title = div.a.text
            content = div.div.text
            url = div.a.attrs["href"]
            keyword = div.em.text
            datetime = div.find(class_="p_date").text
            data = {
                "QQ":qq,
                "关键字":keyword,
                "链接":url,
                "标题": title,
                "内容": content,
                "时间": datetime
            }
            print(data)
            output.writerow(data)
        except:
            print(div)


def main():
    fp = open("result.csv", "w", newline="", encoding="utf-8-sig")
    fieldnames = ["QQ", "关键字", "链接", "标题", "内容", "时间"]
    output = csv.DictWriter(fp,fieldnames=fieldnames)
    output.writeheader()

    for qq in qq_lst:
        keyword = qq
        page = getPage(keyword)
        parse(page, qq, keyword, output)
        keyword = "qq" + qq
        page = getPage(keyword)
        parse(page, qq, keyword, output)
    fp.close()

main()