# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# 获取要存储的字段
class UserItem(scrapy.Item):
        id = scrapy.Field()
        name = scrapy.Field()
        answer_count = scrapy.Field()
        articles_count = scrapy.Field()
        follower_count = scrapy.Field()
        url_token = scrapy.Field()
        user_type = scrapy.Field()
        avatar_url_template = scrapy.Field()