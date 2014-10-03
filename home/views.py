from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext

from django.conf import settings

from spider.weixin import Weixin
from spider.weibo import get_content as get_weibo_content
from spider.zhihu import get_content as get_zhihu_content
from spider.preview import output as get_preview
from spider.full import output as get_full


import re

def index(request):
    return render(request, 'index.html')


def explorer(request):
    pass

def preview(request):
    if request.method == 'POST' and 'rss' in request.POST:
        rss = request.POST['rss']
        #assert False
        error = False
        try:
            feed = get_preview(rss)
        except:
            error = True
        return render(request, 'preview.html', {'feed': feed, 'error': error})
    else:
        return render(request, 'preview.html')

def full(request):
    if request.method == 'GET' and 'url' in request.GET and request.GET['url']:
        url = request.GET['url']
        type_ = request.GET['type']
        tag = request.GET['tag']
        class_ = request.GET['class']
        id_ = request.GET['id']
        # Ajax
        if request.is_ajax():
            if type_ == 'ra':
                content = get_full(url, type_='ra', onlycontent=True)
                return HttpResponse(content)

            elif type_ == 'bs':
                content = get_full(url, type_='bs', onlycontent=True, class_=class_, tag=tag, id_=id_)
                return HttpResponse(content)
        # Render rss
        else:
            if type_ == 'ra':
                content = get_full(url, type_='ra')
                return HttpResponse(content, content_type="text/xml")
            elif type_ == 'bs':
                content = get_full(url, type_='bs', class_=class_, tag=tag, id_=id_)
                return HttpResponse(content, content_type="text/xml")

    return render(request, 'full.html', {})

def full_api(request):

    pass

def weixin(request):

    if request.method == 'POST' and 'name' in request.POST:
        name = request.POST['name']
        try:
            w = Weixin()
            w.search(unicode(name))
            search_result = w.search_result
        except: # TODO:
            search_result = None

        return render(request, 'weixin.html', {'search_result': search_result})

    if request.method == 'GET' and 'openid' in request.GET:
        openid = request.GET['openid']
        try:
            w = Weixin()
            renders = w.build(str(openid), render=True)
            return HttpResponse(renders, content_type="text/xml")
        except: # TODO:
            return HttpResponse('Error 42')

    return render(request, 'weixin.html')

def weibo(request):
    if request.method == 'POST' and 'id' in request.POST:
        userid = request.POST['id']

        return HttpResponseRedirect('/home/template/weibo/?id=' + userid)

    if request.method == 'GET' and 'id' in request.GET:
        userid = request.GET['id']
        content = get_weibo_content(userid)

        return HttpResponse(content, content_type="text/xml")

    return render(request, 'weibo.html')

def zhihu(request):
    if request.method == 'POST' and 'id' in request.POST:
        userid = request.POST['id']

        return HttpResponseRedirect('/home/template/zhihu/?id=' + userid)

    if request.method == 'GET' and 'id' in request.GET:
        userid = request.GET['id']
        content = get_zhihu_content(userid)


        return HttpResponse(content, content_type="text/xml")

    return render(request, 'zhihu.html')
