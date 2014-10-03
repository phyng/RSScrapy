# coding: utf-8
# date: 2014-09-28

from jinja2 import Template
import time
import os
import sys
import speedparser as feedparser
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Feed():

    def __init__(self, template=os.path.join(BASE_DIR, 'spider/templates/simplerss.xml')):
        self.template = template
        builddate = time.strftime(u"%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        self.feed = {
            'title': '',
            'link': '',
            'description': '',
            'lastBuildDate': builddate,
            'language': 'zh-cn',
            'item': [],
        }
        self.item = {
            'title': '',
            'link': '',
            'guid': '',
            'comments': '',
            'pubDate': builddate,
            'creator': 'RSScrapy',
            'category': [],
            'description': '',
            'content': '',
        }

    def build(self, destination='build/test.xml'):
        template = Template(open(self.template, 'r').read())
        render = template.render(feed=self.feed)
        with open(destination, 'w') as f:
            f.write(render)

    def render(self):
        template = Template(open(self.template, 'r').read())
        render = template.render(feed=self.feed)
        return render


class Parse():

    def __init__(self, obj):
        self.d = feedparser.parse(obj)
        f = Feed()
        feedattr = {
            'title': 'title',
            'link': 'link',
            'description': 'subtitle',
        }
        for k, v in feedattr.items():
            if hasattr(self.d.feed, v):
                f.feed[k] = getattr(self.d.feed, v)
        if hasattr(self.d.feed, 'updated_parsed'):
            t = time.strftime(u"%a, %d %b %Y %H:%M:%S +0000", self.d.feed.updated_parsed)
            f.feed['lastBuildDate'] = t

        #print f.feed
        itemattr = {
            'title': 'title',
            'link': 'link',
            'description': 'summary',
            'guid': 'id',
            'creator': 'author',
        }
        for i in self.d.entries:
            for k, v in itemattr.items():
                if hasattr(i, v):
                    f.item[k] = getattr(i, v)
            if hasattr(i, 'content'):
                f.item['content'] = i.content[0]['value']
            if hasattr(i, 'updated_parsed'):
                t = time.strftime(u"%a, %d %b %Y %H:%M:%S +0000", i.updated_parsed)
                f.item['pubDate'] = t
            #print f.item
            f.feed['item'].append(f.item.copy())
        self.f = f

    def build(self):
        self.f.build()

    def render(self):
        return self.f.render()


def test_Feed():
    f = Feed()
    f.feed['item'].append(f.item.copy())
    print f.feed
    f.item['content'] = 'test'
    f.feed['item'].append(f.item)
    print f.feed
    f.build()
    print f.render()

def test_parse():
    url_list = [
        'http://www.ifanr.com/feed',
        'http://www.omgubuntu.co.uk/feed',
        'http://rss.weibodangan.com/weibo/rss/1691472820/',
        'https://pipes.yahoo.com/pipes/pipe.run?_id=2ce237471d3147beee230f6eedb2f65a&_render=rss&collection=30718027',
        'http://www.v2ex.com/index.xml',
        'http://www.douban.com/feed/people/Fenng/interests',
        'http://www.chromi.org/feed',
        'http://www.chromi.org/comments/feed',
        'http://bucee.net/feed',
        'http://octopress.org/atom.xml',
        ]
    for url in url_list:
        r = requests.get(url)
        r.encoding = 'utf-8'
        print url,
        p = Parse(str(r.text))
        p.build()
        print 'OK'



if __name__ == '__main__':
    test_parse()
