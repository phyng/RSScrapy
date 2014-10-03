import json
import time
import requests
from readability.readability import Document
from buildxml import Parse
from multiprocessing.dummy import Pool as ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def pretty_json(obj):
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)


def get_by_readability(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    content = Document(r.text).summary()
    return content

def get_by_bs(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)
    content = soup.find('div', 'rich_media_inner')

def output(url, onlycontent=False):
    r = requests.get(url)
    r.encoding = 'utf-8'

    p = Parse(str(r.text))

    feed = p.f.feed
    urls = [ item['link'] for item in feed['item'] ][:10]
    if onlycontent:
        return get_by_readability(urls[0])
    else:
        pool = ThreadPool(5)
        results = pool.map(get_by_readability, urls)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()

        for i in range(len(feed['item'][:10])):
            feed['item'][i]['content'] = results[i]
        p.f.feed = feed
        return p.render()




def test():
    ul = [
        'http://www.ifanr.com/feed',
        'http://rss.weibodangan.com/weibo/rss/1691472820/',
        'http://www.v2ex.com/index.xml',
        'http://www.chromi.org/feed',
        'http://bucee.net/feed',
        'http://octopress.org/atom.xml',
    ]
    for url in ul:
        t0 = time.clock()
        print output(url)
        print time.clock() - t0, url
        time.sleep(1000)


if __name__ == '__main__':
    test()
