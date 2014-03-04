from django.conf.urls import patterns, url

from 臺灣言語資料庫校對.介面 import 最近改的資料

urlpatterns = patterns('',
	url(r'^.*$', 最近改的資料, name='最近改的資料'),
)