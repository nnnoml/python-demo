# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
class CharisPipeline(object):
    def __init__(self):
        # self.db = pymysql.connect("localhost","root","123","django",'utf8')

        self.db =connect = pymysql.connect(
            host='localhost',
            user='root',
            passwd='123',
            db='django',
            charset='utf8'
        )
        self.cursor = self.db.cursor()
        # self.cursor.execute('truncate table novel')
        # self.db.commit()
    def process_item(self, item, spider):
        # if spider.name == 'news':
        curTime = str(datetime.datetime.now())
        title = str(item['title'][0])
        author = str(item['author'][0])
        sql = "select count(id) from novel where title like '%"+title+"%'"
        self.cursor.execute(sql)
        if (self.cursor.fetchone()[0] >= 1 ):
            print('已存在')
        else:
            sql =  "INSERT INTO novel(title, author, date) VALUES  ('"+title+"', '"+author+"', '"+curTime+"')"
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
        return item
    def __del__(self):
        self.db.close()
