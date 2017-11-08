# -*- coding: utf-8 -*-
import scrapy
import json #json包
from zhihuuser.items import UserItem #用于获取item 联合pipe 保存数据字段

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}' #用户个人信息获取api
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics' #用户个人信息获取api参数
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&amp;offset={offset}&amp;limit={limit}' #获取关注用户api
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics' #关注用户api参数
    start_user = 'excited-vczh' #种子选手

    def start_requests(self): #请求开始
        yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user) # format替换参数，拼接url 开始爬取第一个用户个人信息
        yield scrapy.Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),self.parse_follows) #替换参数，爬取第一个用户的粉丝列表

    def parse_user(self, response): #爬取个人信息回调
        result = json.loads(response.text) #json解析
        item = UserItem()                  #获取item
        for field in item.fields:          #循环item的字段
            if field in result.keys():     #item字段在json结果内
                item[field] = result.get(field) #赋值
        yield item  #数据
        yield scrapy.Request(
            self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),
            self.parse_follows)

    def parse_follows(self, response): #爬取粉丝列表回调
        results = json.loads(response.text) #json解析

        if 'data' in results.keys(): #json里如果有data
            for result in results.get('data'): #循环data里的数据
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),self.parse_user) #组装成url,抓取粉丝的个人信息

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False: #获取下一页粉丝列表 ， 如果paging存在，并且is_end标志位为false
            next_page = results.get('paging').get('next')   #获取下一页粉丝列表url
            yield scrapy.Request(next_page, self.parse_follows) #爬取粉丝列表

    def parse(self, response): #废弃
        pass
