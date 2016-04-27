# -*- coding:utf-8 -*-
"""
爬妹子图(www.meizitu.com)上的图片
"""
import requests
from bs4 import BeautifulSoup
import uuid

class GirlSpider(object):
    def __init__(self):
        self.baseURL = "http://www.meizitu.com/"
    
    def getPage(self, url):
        """
        获取页面信息
        """
        res = ""
        try:
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"}
            res = requests.get(url, headers=headers)
            return res.text.encode("ISO-8859-1",'ignore')
        except Exception as e:
            print str(e)
            return res
       
    
    def getCategories(self, page):
        """
        获取图片分类
        """
        soup = BeautifulSoup(page, "lxml")
        div = soup.find("div", class_="tags")
        links = div.select("a")
        categories = {}
        for link in links:
            if link["href"] not in categories:
                categories[link["href"]] = link["title"]
        return categories
    
    def getPageList(self, page):
        """
        获取分页链接
        """
        soup = BeautifulSoup(page, "lxml")
        div = soup.find("div", id="wp_page_numbers")
        if div:
            links = div.select("a")
            res = []
            for link in links:
                res.append(link["href"])
            return res
        else:
            return []
    
    def getListInfo(self, page):
        """
        获取页面的目录链接
        """
        soup = BeautifulSoup(page, "lxml")
        ArticleDivs = soup.find_all("div", class_="pic")
        res = []
        for div in ArticleDivs:
            temp = {}
            temp["url"] = div.find("a")["href"]
            h3 = div.find_next_sibling("h3")
            if h3:
                temp["title"] = h3.string
                res.append(temp)
        return res
    
    def getIMGList(self, page):
        """
        获取每个目录下面的图片列表
        """
        soup = BeautifulSoup(page, "lxml")
        picDiv = soup.find("div", id="picture")
        if picDiv:
            imgs = picDiv.find_all("img")
            urls = []
            for img in imgs:
                urls.append(img["src"])
            return urls
        else:
            return []
        
    def saveIMG(self, url, filename):
        """
        保存图片
        """
        try:
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"}       
            img = requests.get(url, headers=headers, stream=True)
            data = img.content
            with open(filename, "wb")  as f:
                f.write(data)
            print u'下载成功'
        except Exception as e:
            print str(e)
    
    def mkdir(self, path):
        path = path.strip().replace("*", "")
        import os
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False
    
    def start(self):
        index_page = self.getPage(self.baseURL)
        categories = self.getCategories(index_page)
        count = 1
        for cate_url, title in categories.iteritems():
            if title == u'比基尼' or title == u'嫩模':
                continue
            first_part = "./img/" + title + "/"
            page = self.getPage(cate_url)
            page_list = self.getPageList(page)
            if page_list:
                for url in page_list:
                    url = self.baseURL + "a/" + url
                    dir_list = self.getListInfo(self.getPage(url))
                    for dir in dir_list:
                        href = dir["url"]
                        dir_name = dir["title"]
                        second_part = first_part + dir_name + "/"
                        img_page = self.getPage(href)
                        img_list = self.getIMGList(img_page)
                        for img in img_list:
                            path = second_part
                            self.mkdir(path)
                            img__file_name = path + str(uuid.uuid4()) + ".jpg"
                            print u'正在下载图片' +  str(count)
                            count = count + 1
                            self.saveIMG(img, img__file_name)                            
 

spider = GirlSpider()
spider.start()
