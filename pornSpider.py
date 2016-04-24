# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os
import uuid

class PornSpider(object):
    def __init__(self, index):
        self.base_url = "http://www.nianhua03.net/"
        self.base_index = str(index)
        self.index_url = self.base_url + "news/articlelist/" + str(index) + ".html"
        
    def getPage(self, url):
        # 获取页面信息
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode("gbk")
        except urllib2.URLError as e:
            return ""
    
    def getIMGArea(self, page):
        # 获取页面中包含图片网页链接的区域
        pattern_area = re.compile(r'<div class="listBoxCenter">(.*?)</div>', re.S)
        items = re.findall(pattern_area, page)
        if items:
            return items[0]
  
    def getIMGPages(self, area):
        # 获取列表页中图片网页的链接信息
        pattern = re.compile(r'/news/article/(.*?).html.*?title="(.*?)"', re.S)
        items = re.findall(pattern, area)
        data = []
        for item in items:
            infos = {}
            infos["url"] = item[0]
            infos["title"] = item[1]
            data.append(infos)
        return data
    
    def getIMGS(self, page):
        # 获取图片网页中的图片URL
        pattern_area = re.compile(r'<div class="tukucontent">(.*?)</div>', re.S)
        pattern_url =re.compile(r'<img src="(.*?)" border="0"', re.S)
        area = re.findall(pattern_area, page)
        if area:
            urls = []
            items = re.findall(pattern_url, area[0])
            if items:
                for item in items:
                    urls.append(item)
                return urls
            else:
                return []
        else:
            return []
        
    
    def getPageNums(self, page):
        # 获取列表页的总数
        pattern = re.compile(r'<span>..</span><a.*?>(.*?)</a>', re.S)
        items = re.findall(pattern, page)
        if items:
            return int(items[0])
        else:
            return 0
    
    def saveIMG(self, imgURL, filename):
        # 保存图片
        try:
            img = urllib2.urlopen(imgURL)
            data = img.read()
            with open(filename, "wb")  as f:
                f.write(data)
        except urllib2.URLError as e:
            print str(e)
    
    def start(self):
        indexPage = self.getPage(self.index_url)
        pageNum = self.getPageNums(indexPage)
        count = 1
        if pageNum > 0:
            for page in range(1, pageNum+1):
                if page == 1:
                    url = self.index_url
                else:
                    url = self.base_url +"news/articlelist/" + self.base_index + "_" + str(page) +".html"
                page = self.getPage(url)
                img_area = self.getIMGArea(page)
                if img_area:
                    url_infos = self.getIMGPages(img_area)
                    for url_info in url_infos:
                        page_url = self.base_url + "news/article/" + url_info["url"] + ".html"
                        print u"正在下载页面%s中的图片 :%s" % (url_info["url"], url_info["title"])
                        img_page = self.getPage(page_url)
                        img_urls = self.getIMGS(img_page)
                        for img_url in img_urls:
                            print u"正在下载图片：%d" % count
                            filename = "./img/" + str(uuid.uuid4()) + ".jpg"
                            self.saveIMG(img_url, filename)
                            count += 1
                            
spider = PornSpider(29)
spider.start()
