#!/usr/bin/python
#coding=utf8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from uyusky.items import UyuItem

class UyuSky(CrawlSpider):
	name = 'uyusky'
	start_urls = ['http://www.eyusky.net/']
	url = 'http://www.eyusky.net/'

	#获取首页电影分类列表
	def parse(self,response):
		selector = Selector(response)
		Moive_Cate_Url = selector.xpath('//div[@class="aside"]/ul/li/a/@href').extract()
		# req = []
		# for Each_Cate_Url in Moive_Cate_Url:
		# 	r = Request(Each_Cate_Url,callback=self.parse_content)
		# 	req.append(r)
		# return req
		url = 'http://www.eyusky.net/dianyingdianshi'
		r = Request(url,callback=self.parse_content)
		return r


	#获取content内容页
	def parse_content(self,response):
		item = UyuItem()
		selector_content = Selector(response)
		req = []
		Article_Content = selector_content.xpath('//div[@class="content"]/article[@class="excerpt"]')
		for article in Article_Content:
			article_names = article.xpath('//div[@class="content"]/article[@class="excerpt"]/header/h2/a/text()').extract()
			article_urls = article.xpath('//div[@class="content"]/article[@class="excerpt"]/header/h2/a/@href').extract()
			
			#文章简介标题
			for article_name in article_names: 
				item['article_name'] = article_name

			for url in article_urls:
				r = Request(url,callback=self.parse_article)
				r.meta['item'] = item
				req.append(r)

			nextLink = article.xpath('//li[@class="next-page"]/a/@href').extract()
			if nextLink:
				nr =  Request(nextLink[0],callback=self.parse_content)
				req.append(nr)

		return req

	#获取内页详情和链接
	def parse_article(self,response):
		item = response.meta['item']
		selector_article = Selector(response)
		article_intro = selector_article.xpath('//article[@class="article-content"]/p[1]/text()').extract()
		item['article_intro'] = article_intro
		
		#定义图片地址
		imgurl = selector_article.xpath('//article[@class="article-content"]/p/a/img/@data-original | //article[@class="article-content"]/p/img/@data-original').extract()
		item['imgurl'] = imgurl

		#定义下载电影名字
		item['download'] = {}
		item['download']['downloadname'] = {}
		item['download']['downloadinfo'] = {}
		download_dom = selector_article.xpath('//div[@class="down shortcodestyle add-icon-download"]')
		for index in range(len(download_dom)):
			index = index + 1
			download_info = selector_article.xpath('//div[@class="down shortcodestyle add-icon-download"][position()=%s]/a[@href]/text()'%index).extract()
			download_name = selector_article.xpath('//div[@class="down shortcodestyle add-icon-download"][position()=%s]//preceding-sibling::p[1]'%index).extract()
			item['download']['downloadname'][str(index)] = download_name
			item['download']['downloadinfo'][str(index)] = download_info


		return item





