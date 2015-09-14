from scrapy import Item,Field

class UyuItem(Item):
	category = Field()
	article_name = Field()
	article_intro = Field()
	title = Field()
	score = Field()
	movieinfo = Field()
	imgurl = Field()
	movieinfo2 = Field()
	download = Field()

