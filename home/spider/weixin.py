# coding: utf8
# 实现 weixin 部分输出转成全文输出

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import re
import json
import time
import requests
from bs4 import BeautifulSoup
import xmltodict
from buildxml import Feed


def pretty_json(obj):
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)


class Weixin():
    def __init__(self):
        pass

    def search(self, name):
        self.name = name
        url = 'http://weixin.sogou.com/weixin'
        payload = {'query': name, 'type': 1}
        r = requests.get(url, params=payload)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        items = soup.find_all('div', 'wx-rb')
        di = dict(openid='', name='', id='', v='')
        self.search_result = []
        rec = re.compile(ur'openid=([^"^\s]+?)"[\s\S]+?<h3>(.+?)</h3>\n<h4>\n<span>(.+?)</span>\n</h4>')
        for item in items:
            rer = rec.findall(unicode(item))
            rer = list(rer[0])
            # 判断是否认证
            if re.search(ur'class="ico-r"', unicode(item)):
                rer.append(True)
            else:
                rer.append(False)
            #过滤
            for i in range(len(rer)):
                rer[i] = re.sub(r'<.+?>', r'', unicode(rer[i]))
                rer[i] = re.sub(ur'微信号：', r'', unicode(rer[i]))
            #rer = [re.sub(r'<.+?>', r'', unicode(s)) for s in rer]
            #rer = [re.sub(r'<.+?>', r'', unicode(s)) for s in rer]
            di['openid'] = rer[0]
            di['name'] = rer[1]
            di['id'] = rer[2]
            di['v'] = rer[3]
            self.search_result.append(di.copy())

    def get_content(self, url):

        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        content = soup.find_all('div', 'rich_media_inner')[0]
        return content

    def build(self, openid, destination='build/test.xml', render=False):
        """从openid获取文章列表"""

        openid = str(openid)
        f = Feed()

        url = 'http://weixin.sogou.com/gzh?openid=%s' % openid
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        header = soup.find_all('div', 'wx-rb wx-rb2 _item')[0]

        f.feed['title'] = u'微信：' + header.find_all(id="weixinname")[0].get_text()
        f.feed['description'] = header.find_all('div', 's-p2')[0].get_text()
        f.feed['link'] = 'http://rss.phyng.com/home/template/weixin/?openid=%s' % openid
        # 获取items
        jsurl = 'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb'
        payload = {'openid': openid, 'page': 1}
        r = requests.get(jsurl, params=payload)
        r.encoding = 'utf-8'

        rer = re.findall(r'\nsogou.weixin.gzhcb\((\{.+\})\)', r.text)

        items = json.loads(rer[0])['items']
        for item in items:
            item = xmltodict.parse(item)

            #print pretty_json(item)
            f.item['title'] = item['DOCUMENT']['item']['display']['title']
            f.item['link'] = item['DOCUMENT']['item']['display']['url']
            f.item['guid'] = item['DOCUMENT']['item']['display']['docid']
            f.item['description'] = item['DOCUMENT']['item']['display']['content168']
            f.item['creator'] = item['DOCUMENT']['item']['display']['sourcename']

            pubdate = time.localtime(float(item['DOCUMENT']['item']['display']['lastModified']))
            f.item['pubDate'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", pubdate)
            f.item['content'] = self.get_content(f.item['link'])

            f.feed['item'].append(f.item.copy())


        if render == True:
            return f.render()
        else:
            f.build(destination)


def test():
    w = Weixin()
    w.search('小道消息')
    # print w.search_result
    w.build(w.search_result[0]['openid'])
    print w.build(w.search_result[0]['openid'], render=True)


if __name__ == '__main__':
    test()
