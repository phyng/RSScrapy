import json
import requests
import markdown
import json

from buildxml import Parse


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def pretty_json(obj):
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)

def output(url):
    r = requests.get(url)
    r.encoding = 'utf-8'

    p = Parse(str(r.text))

    feed = p.f.feed
    feed['description'] = feed['description'][:60] + '...'
    for item in feed['item']:
        item['description'] = item['description'][:60] + '...'
        item['content'] = item['content'][:60] + '...'

    md = '~~~json\n' + pretty_json(feed) + '\n~~~\n'
    html = markdown.markdown(md, extensions = ['fenced_code'])

    return html

