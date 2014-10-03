from django.conf.urls import patterns, include, url
from django.contrib import admin

from home import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^explorer/$', views.explorer, name='explorer'),
    url(r'^preview/$', views.preview, name='preview'),

    url(r'^template/full/$', views.full, name='full'),


    url(r'^template/weixin/$', views.weixin, name='weixin'),
    url(r'^template/weibo/$', views.weibo, name='weibo'),
    url(r'^template/zhihu/$', views.zhihu, name='zhihu'),

    #API
    url(r'^api/full/$', views.full_api, name='full_api'),


)
