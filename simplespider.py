# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import thread
import time

class SimpleSpider(object):
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
        self.headers = {"User-Agent": self.user_agent}
        self.stories = []
        self.enable = False
    
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode("utf-8")
            return pageCode
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                print "connection error", e.reason
                return None
            
    
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "Loading error"
            return None
        patterns = re.compile(r'<div.*?author clearfix">.*?<h2>(.*?)' + 
                              '</h2>.*?<div.*?content">(.*?)<!--.*?</div>'+
                              '(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(patterns, pageCode)
        pageStories = []
        for item in items:
            haveImg = re.search("img", item[2])
            if not haveImg:
                replaceBR = re.compile("<br/>")
                text = re.sub(replaceBR, "\n", item[1])
                pageStories.append([item[0].strip(), text.strip(), item[3].strip()])
        return pageStories
    
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
                
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            if int(story[2]) > 1000:
                input = raw_input()
                self.loadPage()
                if input == "Q":
                    self.enable = False
                    return
                try:
                    print u"第%d页\t发布人:%s\t赞:%s\n%s" % (page, story[0], story[2], story[1])
                except UnicodeError as e:
                    pass
        
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)
        
spider = SimpleSpider()
spider.start()


