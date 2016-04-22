# -*- coding:utf-8 -*-

import re
import urllib
import urllib2


class TiebaSpider(object):
	def __init__(self, baseURL, flag):
		self.baseURL = baseURL
		self.flag = "?see_lz=" + str(flag)
		

	def getPage(self, index):
		try:
			url = self.baseURL + self.flag + '&pn=' + str(index)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			return response.read().decode("utf-8")
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"Connection error , reason:", e.reason
				return None


	def getTitle(self, index):
		page = self.getPage(index)
		pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None

baseURL = 'http://tieba.baidu.com/p/3138733512'
spider = TiebaSpider(baseURL, 1)
spider.getPage(1);
print spider.getTitle(1)