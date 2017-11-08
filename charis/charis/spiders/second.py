# -*- coding: utf-8 -*-
import scrapy
import re
from charis.items_second import SecondItem

class SecondSpider(scrapy.Spider):
    name = 'second'
    start_urls = ['http://www.23us.cc/class/1_1.html'] #/class/7_1.html
    base_url = 'http://www.23us.cc'

    # def start_requests(self):
    #     for i in range(1, 8):
    #         url = self.base_url +'/class/'+ str(i) + '_1.html'
    #         yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for href in response.xpath('//ul[@class="item-con"]/li/span[@class="s2"]/a/@href'):
            url = self.base_url + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents,meta={'url':url})

    def parse_dir_contents(self, response):
        for quote in response.xpath('//div[@id="container"]'):
            item = SecondItem()
            aa = ''
            item['url'] = response.meta['url']
            for info in quote.xpath('div[@class="bookinfo"]'):
                item['title'] = info.xpath('div[@class="btitle"]/span/h1/text()').extract()
                item['author'] = info.xpath('div[@class="btitle"]/span/em/text()').re(u'作者[:|：]\s*(.*)')
                item['new_article'] = info.xpath('p[@class="stats"]/span/a/text()').extract()
            # for main in quote.xpath('.//dl[@class="chapterlist"]/dd'):
            #     aa += str(main.xpath('a/text()').extract()) + str(',')
            item['zhangjie'] = aa
            yield item
