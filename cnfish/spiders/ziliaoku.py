# -*- coding: utf-8 -*-
import scrapy, json, pymongo
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Response
from cnfish.items import CnfishItem
from cnfish import settings

class ZiliaokuSpider(CrawlSpider):
    name = "cnfish"
    allowed_domains = ["cnfish.cn"]
    start_urls = (
        'http://www.cnfish.cn/ZLK/WaterListMore.aspx?TypeId=268435456',
        'http://www.cnfish.cn/ZLK/SeaList.aspx',
        'http://www.cnfish.cn/ZLK/WaterPlants.aspx',
        'http://www.cnfish.cn/ZLK/WaterListJinYu.aspx?TypeId=469762048',
        'http://www.cnfish.cn/ZLK/WaterListJinLi.aspx?TypeId=536870912',
    )
    rules = (
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow='/htm/news/'), callback='parse_item', process_links='link_filter', follow=True),
        Rule(LinkExtractor(allow='/ZLK/'), follow=True, process_links='link_filter'),
    )


    def __init__(self, category=None, *args, **kwargs):
        super(ZiliaokuSpider, self).__init__(*args, **kwargs)
        self.mongo_url = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DB
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def closed():
        self.client.close()


    def link_filter(self, links):
        ret = []
        for link in links:
            if link and self.db['CnfishItem'].find_one({"crawl_from": link.url}):
                print '丢弃', link.url
            else:
                ret.append(link)
        return ret

    def parse_item(self, response):
        type_str = [u'淡水热带鱼', u'金鱼', u'锦鲤', u'海水资料库', u'水草']
        if response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HyperLink7"]/text()').extract()[0] in type_str:
            item = CnfishItem()
            item['crawl_from'] = response.url
            item['title'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_div_NewsTitle"]/text()').extract()
            item['article_info'] = response.xpath('//div[@class="news_info"]/text()').extract()
            item['article'] = response.xpath('//*[@class="dianpu_intro"]//p/text()').extract()
            item['imgurl'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_div_content"]//img/@src').extract()
            item['tag'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HyperLink7"]/text()').extract()
            item['tag'] += response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HyperLink4"]/text()').extract()
            yield item
