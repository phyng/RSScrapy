import re
import requests
from bs4 import BeautifulSoup


def get_content(userid):
    url_yahoo = 'https://pipes.yahoo.com/pipes/pipe.run?_id=2ce237471d3147beee230f6eedb2f65a&_render=rss&collection=' + userid
    url_zhihu = 'http://www.zhihu.com/collection/' + str(int(userid))
    r_yahoo = requests.get(url_yahoo)

    r_zhihu = requests.get(url_zhihu)
    soup = BeautifulSoup(r_zhihu.text)
    title = unicode(soup.title)

    content = re.sub(ur'<title>RSS for Zhihu collection</title>', title, r_yahoo.text)


    return content
