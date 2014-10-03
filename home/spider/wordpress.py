# coding: utf8
# 实现 Wordpress 部分输出转成全文输出

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import xmltodict
from bs4 import BeautifulSoup
from buildxml import Feed


class Wordpress():
    def __init__(self, url):

        r = requests.get(url)
        try:
            self.doc = xmltodict.parse(r.text)
            content = self.doc['rss']['channel']['item'][0]['content:encoded']
        except KeyError:
            self.notFullText = True

    def get_content(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        content = soup.find_all('div', 'entry-content')[0]
        return unicode(content)

    def build(self):
        f = Feed()
        for k, v in f.feed.items():
            if k in self.doc['rss']['channel'] and k != 'item':
                f.feed[k] = self.doc['rss']['channel'][k]

        for item in self.doc['rss']['channel']['item']:

            for k, v in f.item.items():
                if k in item:
                    f.item[k] = item[k]
            url = item['link']

            f.item['content'] = self.get_content(url)
            f.feed['item'].append(f.item.copy())

        f.build()


def test():
    url = 'http://www.omgubuntu.co.uk/feed'
    url1 = 'http://www.ifanr.com/feed'
    w = Wordpress(url)
    w.build()


if __name__ == '__main__':
    test()
