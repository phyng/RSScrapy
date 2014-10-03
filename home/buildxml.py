# coding: utf-8
# date: 2014-09-28

from jinja2 import Template
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Feed():

    def __init__(self, template='templates/simplerss.xml'):
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


def test():
    f = Feed()
    f.feed['item'].append(f.item.copy())
    print f.feed
    f.item['content'] = 'test'
    f.feed['item'].append(f.item)
    print f.feed
    f.build()


if __name__ == '__main__':
    test()
