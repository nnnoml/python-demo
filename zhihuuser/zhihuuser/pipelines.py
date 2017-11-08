# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# 管道获取数据并存储
class ZhihuuserPipeline(object):
    # 初始化链接库
    def __init__(self):
        self.db =connect = pymysql.connect(
            host='localhost',
            user='root',
            passwd='123',
            db='python_scrapy',
            charset='utf8'
        )
        self.cursor = self.db.cursor()
    # 分析数据
    def process_item(self, item, spider):
        zhihuid = str(item['id'])
        name = str(item['name'])
        answer_count = str(item['answer_count'])
        articles_count = str(item['articles_count'])
        follower_count = str(item['follower_count'])
        token = str(item['url_token'])
        user_type = str(item['user_type'])
        avatar = str(item['avatar_url_template']).format(size='xll') #将size替换成xll

        sql = "INSERT INTO zhihu ( `zhihuid`, `name`, `answer_count`, `articles_count`, `follower_count`, `token`,\
`user_type`, `avatar`)  VALUES('"+zhihuid+"','"+name+"','"+answer_count+"','"+articles_count+"', \
'"+follower_count+"','"+token+"','"+user_type+"','"+avatar+"') ON DUPLICATE KEY UPDATE answer_count='"+answer_count+"', \
articles_count='"+articles_count+"',follower_count='"+follower_count+"',avatar='"+avatar+"'" # 拼接sql,如果存在则update

        try: #事务提交
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

        return item
