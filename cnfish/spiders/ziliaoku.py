# -*- coding: utf-8 -*-
import scrapy, json

from cnfish.items import CnfishItem

class ZiliaokuSpider(scrapy.Spider):
    name = "ziliaoku"
    allowed_domains = ["cnfish.cn"]
    start_urls = (
        'http://www.cnfish.cn/ZLK/WaterListMore.aspx?TypeId=268435456',
        'http://www.cnfish.cn/ZLK/SeaList.aspx',
        'http://www.cnfish.cn/ZLK/WaterPlants.aspx',
        'http://www.cnfish.cn/ZLK/WaterListJinYu.aspx?TypeId=469762048',
        'http://www.cnfish.cn/ZLK/WaterListJinLi.aspx?TypeId=536870912',
    )

    def parse(self, response):
        if response.xpath('//*[@id="ctl00_ContentPlaceHolder1_div_content"]/p[1]/img/@src').extract():
            item = CnfishItem()

            page = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_div_content"]')

            for i in page.xpath('//p'):
                if i.xpath('//img/@src').extract():
                    pass
                else:
                        if item.get('article'):
                            item['article'] = item.get('article') + i.xpath('//p/text()').extract()[0].encode('utf-8')
                        else:
                            item['article'] = i.xpath('//p/text()').extract()[0].encode('utf-8')
            item['name'] = response.xpath('//div[@id="ctl00_ContentPlaceHolder1_div_NewsTitle"]/text()').extract()[0].encode('utf-8')
            item['imgurl'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_div_content"]/p[1]/img/@src').extract()[0].encode('utf-8')
            item['tag1'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HyperLink7"]/text()').extract()[0].encode('utf-8')
            item['tag2'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_HyperLink4"]/text()').extract()[0].encode('utf-8')
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            print line
            yield item
        next_page = response.xpath('//*[@class="chanpin_name"]/@href').extract()
        if next_page:
            for i in next_page:
                yield scrapy.Request('http://www.cnfish.cn/' + i, self.parse)
