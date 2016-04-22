# -*- coding:utf-8 -*-

import re
import urllib
import urllib2


class TiebaSpider(object):
	def __init__(self, baseURL, flag, floorTag=False):
		self.baseURL = baseURL
		self.flag = "?see_lz=" + str(flag)
		self.tool = Tool()
		self.file = None
		self.floor = True
		self.defautlTitle = u"百度贴吧"
		self.floorTag  = floorTag
		

	def getPage(self, index):
		try:
			url = self.baseURL + self.flag + '&pn=' + str(index)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			return response.read()
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"Connection error , reason:", e.reason
				return None


	def getTitle(self, page):
		pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None
		
	def getPageNum(self, page):
		pattern = re.compile(r'<span class="red">(.*?)</span>', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None
		
	def getContent(self, page):
		pattern = re.compile(r'<div id="post_content.*?>(.*?)</div>', re.S)
		items = re.findall(pattern, page)
		contents = []
		for item in items:
			item = self.tool.replace(item)
			content = "\n" + item + "\n"
			contents.append(content)
		return contents
	
	def  setFileTitle(self, title):
		if title is not None:
			self.file = open(title + ".txt", "a+")
		else:
			self.file = open(self.defautlTitle + ".txt", "w+")
	
	def writeData(self, contents):
		for item in contents:
			if self.floorTag:
				floorLine = "\n" + str(self.floor) + u"-------------------------------------"
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1
	
	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title.decode("utf-8"))
		if pageNum == None:
			print u"URL已失效，请重试"
			return
		try:
			print u"该帖子共有" + str(pageNum) + u"页"
			for i in range(1, int(pageNum)+1):
				print u"正在写入" + str(i) + u"页数据"
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError, e:
			print u'写入异常，原因:', e.message
		finally:
			print u"写入任务完成"
			
class Tool(object):
	removeIMG = re.compile(r'<img.*?>| {7}|')
	removeAddr = re.compile(r'<a.*?>|</a>')
	replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
	replaceTD = re.compile(r'<td>')
	replacePara = re.compile(r'<p.*?>')
	replaceBR = re.compile(r"<br><br>|<br>")
	removeExtraTag = re.compile(r'<.*?>')
	
	def replace(self, x):
		x = re.sub(self.removeIMG, "", x)
		x = re.sub(self.removeAddr, "", x)
		x = re.sub(self.replaceLine, "\n", x)
		x = re.sub(self.replaceTD, "\t", x)
		x = re.sub(self.replacePara, "\n	", x)
		x = re.sub(self.replaceBR, "\n", x)
		x = re.sub(self.removeExtraTag, "", x)
		return x.strip()


baseURL = 'http://tieba.baidu.com/p/4465934295' 
spider = TiebaSpider(baseURL, 1)
spider.start()