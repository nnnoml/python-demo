#coding:utf-8
import requests
import re
from bs4 import BeautifulSoup

class qsbk:
    def __init__(self):
        self.page = 1
        self.enable = False
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
        }
        self.session = requests.session()
        self.url = 'http://www.qiushibaike.com/hot/page'
        self.baseurl = 'https://www.qiushibaike.com'

    def load(self):
        response = self.session.get(self.url +'/'+ str(self.page), headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for article in soup.find_all(class_='article',limit=1):
            for h2 in article.find_all('h2',limit=1):
                print('作者：'+h2.get_text())
            for a in article.find_all(class_="contentHerf",limit=1):
                respons2 = self.session.get(self.baseurl+a.get('href'), headers=self.headers)
                soup2 = BeautifulSoup(respons2.content, "html.parser")
                print(self.baseurl+a.get('href'))
                print(str(soup2.find(class_='content').string).strip())
            for stats in article.find_all(class_='stats',limit=1):
                for vote in stats.find_all(class_='stats-vote',limit=1):
                    print('投票：'+vote.find('i').string)
                for comment in stats.find_all(class_='stats-comments',limit=1):
                    print('评论：'+comment.find('i').string)

#开始方法
    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        self.enable = True
        while self.enable:
            self.page = self.page + 1
            #等待用户输入
            rrr = input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.load()
            #如果输入Q则程序结束
            if rrr == "Q" or rrr == 'q':
                self.enable = False
                return

if __name__ == '__main__':
    qsbk().start();
