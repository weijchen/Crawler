# -*- coding: utf-8 -*-
# PN: apple news crawler, Created Apr. 2017
# Version 1.2 (items fix, can pour into sqlite)
# Link: 
# https://www.youtube.com/watch?v=fnwvYAtCFko&t=197s
# http://www.bertcarremans.be/using-pipelines-in-scrapy/
# --------------------------------------------------- lib import
import scrapy

from appleNews.items import ApplenewsItem
from bs4 import BeautifulSoup
# --------------------------------------------------- Start!
class AppleCrawler(scrapy.Spider):
	# name, start_urls
	name = 'apple'
	start_urls = ['http://www.appledaily.com.tw/realtimenews/section/new/']		# url 可以抓取多個, use list

	def parse(self, response):
		domain = 'http://www.appledaily.com.tw/'
		soup = BeautifulSoup(response.body, 'lxml')	# 利用 BS 做剖析
		for news in soup.select('.rtddt'):
			# print(news.select('h1')[0].text)
			# print(domain + news.select('a')[0]['href'])	# domain + 相對連結
			yield scrapy.Request(domain + news.select('a')[0]['href'], self.parse_detail)	# 針對抓取之連結，抓取更深層的資訊 (yield parse 給 parse_detail)
	def parse_detail(self, response):
		soup = BeautifulSoup(response.body, 'lxml')
		applenewsitem = ApplenewsItem()
		applenewsitem['title'] = soup.select('#h1')[0].text
		applenewsitem['content'] = soup.select('.trans')[0].text
		applenewsitem['time'] = soup.select('.gggs time')[0].text
		print('item', applenewsitem)
		return applenewsitem

# 輸出成json檔, scrapy crawl apple -o apple.json -t json