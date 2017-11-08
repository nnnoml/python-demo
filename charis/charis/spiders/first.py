# -*- coding: utf-8 -*-
import scrapy
from charis.items_first import FirstItem

class FirstSpider(scrapy.Spider):
    name = 'first'
    allowed_domains = ['segmentfault.com']
    start_urls = ['http://segmentfault.com']

    def parse(self, response):
        for href in response.xpath('//ul/li/a/@href'):
        # for href in response.css("ul > li > a::attr('href')"):
            url = response.url +  href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for quote in response.xpath('//ul/li'):
            item = FirstItem()
            item['title'] = quote.xpath('a/text()').extract(),
            item['link'] =  quote.xpath('a/@href').extract()
            yield item

        # for quote in response.css("ul > li"):
        #     item = CharisItem()
        #     item['title'] = quote.css("a::text").extract_first()
        #     item['link'] = quote.css("a::attr(href)").extract_first()
        #     yield item
        #-----
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
