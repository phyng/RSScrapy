import re
import requests


def get_content(userid):
    url = 'http://rss.weibodangan.com/weibo/rss/' + userid
    r = requests.get(url)
    content = re.sub(r'<ttl>1440</ttl>', r'<ttl>60</ttl>', r.text)
    return content
